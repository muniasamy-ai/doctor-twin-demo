"""RAG: Hybrid search = Vector + Keyword for accurate retrieval."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from openai import OpenAI

from app.core.config import get_settings, SCENARIOS_JSON_PATH
from app.repositories.engine import get_connection
from app.repositories.models import (
    INSERT_SQL,
    ScenarioRow,
    scenario_from_row,
    SELECT_BY_KEYWORD_SQL,
    SELECT_BY_KEYWORD_WITH_INTENT_SQL,
    SELECT_BY_VECTOR_SQL,
    SELECT_BY_VECTOR_WITH_INTENT_SQL,
)

log = logging.getLogger(__name__)

# RRF constant (Reciprocal Rank Fusion): score = 1/(k + rank)
RRF_K = 60


def _chunk_text(scenario: dict[str, Any]) -> str:
    """
    One chunk = one full scenario (scenario-level chunking).
    Includes all fields for accurate vector + keyword retrieval.
    """
    parts = [
        f"SCENARIO ID: {scenario.get('scenario_id', '')}",
        f"Intent: {scenario.get('intent', '')}",
        f"Risk: {scenario.get('risk', '')}",
        f"Trigger: {scenario.get('trigger', '')}",
        f"Script: {scenario.get('script', '')}",
        f"Actions: {', '.join(scenario.get('actions') or [])}",
    ]
    if scenario.get("hard_stop"):
        parts.append(f"Hard stop: {scenario['hard_stop']}")
    if scenario.get("required_data"):
        parts.append(f"Required data: {', '.join(scenario.get('required_data') or [])}")
    if scenario.get("metadata"):
        m = scenario["metadata"]
        parts.append(
            f"Metadata: intent={m.get('intent')} risk_level={m.get('risk_level')} "
            f"department={m.get('department')} brain={m.get('brain')}"
        )
    return "\n".join(parts)


def load_scenarios_json(path: Path | None = None) -> list[dict[str, Any]]:
    """Load scenarios from JSON file."""
    p = path or SCENARIOS_JSON_PATH
    if not p.exists():
        raise FileNotFoundError(f"Scenarios file not found: {p}")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def get_embedding(client: OpenAI, text: str, model: str) -> list[float]:
    """Get embedding from OpenAI text-embedding-3-small."""
    r = client.embeddings.create(model=model, input=text)
    return r.data[0].embedding


def _rrf_fusion(
    vector_results: list[tuple[ScenarioRow, float]],
    keyword_results: list[tuple[ScenarioRow, float]],
    top_k: int,
) -> list[tuple[ScenarioRow, float]]:
    """
    Reciprocal Rank Fusion: merge vector + keyword results.
    score = sum(1/(k + rank)) over both lists.
    """
    scores: dict[str, float] = {}
    rows_by_id: dict[str, ScenarioRow] = {}

    for rank, (scenario, _) in enumerate(vector_results, start=1):
        sid = scenario.scenario_id
        scores[sid] = scores.get(sid, 0) + 1.0 / (RRF_K + rank)
        rows_by_id[sid] = scenario

    for rank, (scenario, _) in enumerate(keyword_results, start=1):
        sid = scenario.scenario_id
        scores[sid] = scores.get(sid, 0) + 1.0 / (RRF_K + rank)
        if sid not in rows_by_id:
            rows_by_id[sid] = scenario

    merged = [(rows_by_id[sid], scores[sid]) for sid, _ in sorted(scores.items(), key=lambda x: -x[1])[:top_k]]
    return merged


class RAGService:
    """Hybrid RAG: Vector (pgvector) + Keyword (full-text) → RRF fusion."""

    def __init__(self):
        self._settings = get_settings()
        if not self._settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")
        self._client = OpenAI(api_key=self._settings.openai_api_key)
        self._model = self._settings.embedding_model

    def embed(self, text: str) -> list[float]:
        """Embed text using OpenAI text-embedding-3-small."""
        return get_embedding(self._client, text, self._model)

    def _vector_retrieve(
        self,
        cur,
        query_embedding: list[float],
        top_k: int,
        intent_filter: str | None,
    ) -> list[tuple[ScenarioRow, float]]:
        """Vector similarity search."""
        if intent_filter:
            cur.execute(
                SELECT_BY_VECTOR_WITH_INTENT_SQL,
                (query_embedding, intent_filter, query_embedding, top_k),
            )
        else:
            cur.execute(SELECT_BY_VECTOR_SQL, (query_embedding, query_embedding, top_k))
        rows = cur.fetchall()
        out: list[tuple[ScenarioRow, float]] = []
        for row in rows:
            scenario = scenario_from_row(dict(row))
            score = float(row.get("similarity", 0.0))
            out.append((scenario, score))
        return out

    def _keyword_retrieve(
        self,
        cur,
        query: str,
        top_k: int,
        intent_filter: str | None,
    ) -> list[tuple[ScenarioRow, float]]:
        """Keyword full-text search (PostgreSQL tsvector)."""
        q = query.strip()
        if len(q) < 2:
            return []
        try:
            if intent_filter:
                cur.execute(
                    SELECT_BY_KEYWORD_WITH_INTENT_SQL,
                    (q, intent_filter, q, top_k),
                )
            else:
                cur.execute(SELECT_BY_KEYWORD_SQL, (q, q, top_k))
        except Exception:
            return []
        rows = cur.fetchall()
        out: list[tuple[ScenarioRow, float]] = []
        for row in rows:
            scenario = scenario_from_row(dict(row))
            score = float(row.get("kw_score", 0.0))
            out.append((scenario, score))
        return out

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        intent_filter: str | None = None,
        risk_filter: str | None = None,
        hybrid: bool | None = None,
    ) -> list[tuple[ScenarioRow, float]]:
        """
        Hybrid search: Vector + Keyword → RRF fusion.
        Set hybrid=False to use vector-only. Default: config hybrid_search.
        """
        top_k = top_k or self._settings.top_k_retrieval
        use_hybrid = hybrid if hybrid is not None else self._settings.hybrid_search
        query_embedding = self.embed(query)

        with get_connection() as conn:
            cur = conn.cursor()

            vector_results = self._vector_retrieve(cur, query_embedding, top_k, intent_filter)

            if use_hybrid:
                keyword_results = self._keyword_retrieve(cur, query, top_k, intent_filter)
                if keyword_results:
                    results = _rrf_fusion(vector_results, keyword_results, top_k)
                else:
                    results = vector_results
            else:
                results = vector_results

            cur.close()

        if risk_filter:
            results = [(s, sc) for s, sc in results if s.metadata.get("risk_level") == risk_filter]
        return results

    def index_scenarios(self, scenarios: list[dict[str, Any]] | None = None) -> int:
        """Load scenarios, embed each, upsert into pgvector."""
        if scenarios is None:
            scenarios = load_scenarios_json()
        count = 0
        with get_connection() as conn:
            cur = conn.cursor()
            try:
                for s in scenarios:
                    chunk = _chunk_text(s)
                    embedding = self.embed(chunk)
                    cur.execute(
                        INSERT_SQL,
                        (
                            s.get("scenario_id", ""),
                            s.get("intent", ""),
                            s.get("risk", ""),
                            s.get("trigger", ""),
                            s.get("script", ""),
                            json.dumps(s.get("actions") or []),
                            s.get("hard_stop"),
                            json.dumps(s.get("metadata") or {}),
                            chunk,
                            embedding,
                        ),
                    )
                    count += 1
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cur.close()
        log.info("Indexed %s scenarios", count)
        return count
