"""Ingest scenarios into the RAG database table (scenario_chunks)."""
from __future__ import annotations

from typing import Any

from app.services.rag import RAGService


def ingest_scenarios(scenarios: list[dict[str, Any]] | None = None) -> int:
    """
    Production entrypoint for ingestion.
    - Loads scenarios from data/scenarios.json when scenarios is None.
    - Embeds + upserts into Postgres/pgvector via RAGService.index_scenarios.
    """
    rag = RAGService()
    return rag.index_scenarios(scenarios=scenarios)

