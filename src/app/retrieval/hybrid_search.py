"""Hybrid retrieval: vector + keyword + fusion."""
from __future__ import annotations

from typing import Protocol

from app.repositories.models import (
    ScenarioRow,
    scenario_from_row,
    SELECT_BY_KEYWORD_SQL,
    SELECT_BY_KEYWORD_WITH_INTENT_SQL,
    SELECT_BY_VECTOR_SQL,
    SELECT_BY_VECTOR_WITH_INTENT_SQL,
)

# RRF constant (Reciprocal Rank Fusion): score = 1/(k + rank)
RRF_K = 60


class CursorProtocol(Protocol):
    def execute(self, query: str, params: tuple) -> None: ...

    def fetchall(self) -> list: ...


def rrf_fusion(
    vector_results: list[tuple[ScenarioRow, float]],
    keyword_results: list[tuple[ScenarioRow, float]],
    top_k: int,
) -> list[tuple[ScenarioRow, float]]:
    """
    Reciprocal Rank Fusion: merge ranked lists (vector + keyword).
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
        rows_by_id.setdefault(sid, scenario)

    merged = [
        (rows_by_id[sid], scores[sid])
        for sid, _ in sorted(scores.items(), key=lambda x: -x[1])[:top_k]
    ]
    return merged


def vector_retrieve(
    cur: CursorProtocol,
    query_embedding: list[float],
    top_k: int,
    intent_filter: str | None,
) -> list[tuple[ScenarioRow, float]]:
    """Vector similarity search (pgvector)."""
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


def keyword_retrieve(
    cur: CursorProtocol,
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

