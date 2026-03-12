"""Database connection and schema (engine + models)."""
from __future__ import annotations

from app.repositories.engine import EMBEDDING_DIM, get_connection
from app.repositories.models import (
    ScenarioRow,
    scenario_from_row,
    SCENARIOS_TABLE,
    INSERT_SQL,
    SELECT_BY_VECTOR_SQL,
    SELECT_BY_VECTOR_WITH_INTENT_SQL,
    SELECT_BY_KEYWORD_SQL,
    SELECT_BY_KEYWORD_WITH_INTENT_SQL,
)

__all__ = [
    "EMBEDDING_DIM",
    "get_connection",
    "ScenarioRow",
    "scenario_from_row",
    "SCENARIOS_TABLE",
    "INSERT_SQL",
    "SELECT_BY_VECTOR_SQL",
    "SELECT_BY_VECTOR_WITH_INTENT_SQL",
    "SELECT_BY_KEYWORD_SQL",
    "SELECT_BY_KEYWORD_WITH_INTENT_SQL",
]
