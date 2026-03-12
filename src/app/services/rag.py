"""RAG service: embed + retrieve + index (production service layer)."""
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
)
from app.retrieval.hybrid_search import keyword_retrieve, rrf_fusion, vector_retrieve

log = logging.getLogger(__name__)


def _trigger_string_for_db(scenario: dict[str, Any]) -> str:
    """Normalize trigger/triggers to a single string for DB storage."""
    triggers = scenario.get("triggers")
    if isinstance(triggers, list) and triggers:
        return " | ".join(str(t).strip() for t in triggers if t)
    return str(scenario.get("trigger") or "")


def _chunk_text(scenario: dict[str, Any]) -> str:
    """
    One chunk = one full scenario (scenario-level chunking).
    Includes all fields for accurate vector + keyword retrieval.
    Uses triggers (list) when present so each phrase improves vector search.
    """
    triggers = scenario.get("triggers") or scenario.get("trigger")
    if isinstance(triggers, list):
        trigger_part = "Triggers: " + "; ".join(str(t) for t in triggers if t)
    else:
        trigger_part = f"Trigger: {triggers or ''}"
    parts = [
        f"SCENARIO ID: {scenario.get('scenario_id', '')}",
        f"Intent: {scenario.get('intent', '')}",
        f"Risk: {scenario.get('risk', '')}",
        trigger_part,
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

            vector_results = vector_retrieve(cur, query_embedding, top_k, intent_filter)

            if use_hybrid:
                keyword_results = keyword_retrieve(cur, query, top_k, intent_filter)
                if keyword_results:
                    results = rrf_fusion(vector_results, keyword_results, top_k)
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
                            _trigger_string_for_db(s),
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
