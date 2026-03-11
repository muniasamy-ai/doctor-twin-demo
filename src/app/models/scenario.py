"""Scenario model: DB row <-> scenario dict."""
from __future__ import annotations

import json
from typing import Any

from app.core.database import EMBEDDING_DIM


class ScenarioRow:
    """Represents a scenario row from the database (with embedding)."""

    __slots__ = (
        "id",
        "scenario_id",
        "intent",
        "risk",
        "trigger",
        "script",
        "actions",
        "hard_stop",
        "metadata",
        "chunk_text",
        "created_at",
    )

    def __init__(
        self,
        id: int,
        scenario_id: str,
        intent: str,
        risk: str,
        trigger: str,
        script: str,
        actions: list[str],
        hard_stop: str | None,
        metadata: dict[str, Any],
        chunk_text: str,
        created_at: Any = None,
    ):
        self.id = id
        self.scenario_id = scenario_id
        self.intent = intent
        self.risk = risk
        self.trigger = trigger
        self.script = script
        self.actions = actions or []
        self.hard_stop = hard_stop
        self.metadata = metadata or {}
        self.chunk_text = chunk_text
        self.created_at = created_at

def scenario_from_row(row: dict) -> ScenarioRow:
    """Build ScenarioRow from DB row (RealDictCursor)."""
    actions = row.get("actions")
    if isinstance(actions, str):
        try:
            actions = json.loads(actions) if actions else []
        except json.JSONDecodeError:
            actions = []
    metadata = row.get("metadata") or {}
    if isinstance(metadata, str):
        try:
            metadata = json.loads(metadata) if metadata else {}
        except json.JSONDecodeError:
            metadata = {}
    return ScenarioRow(
        id=row["id"],
        scenario_id=row["scenario_id"],
        intent=row.get("intent") or "",
        risk=row.get("risk") or "",
        trigger=row.get("trigger") or "",
        script=row.get("script") or "",
        actions=actions,
        hard_stop=row.get("hard_stop"),
        metadata=metadata,
        chunk_text=row.get("chunk_text") or "",
        created_at=row.get("created_at"),
    )


# SQL: table and index for similarity search
SCENARIOS_TABLE = "scenario_chunks"
CREATE_EXTENSION_SQL = "CREATE EXTENSION IF NOT EXISTS vector;"
CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {SCENARIOS_TABLE} (
    id SERIAL PRIMARY KEY,
    scenario_id TEXT UNIQUE NOT NULL,
    intent TEXT NOT NULL,
    risk TEXT NOT NULL,
    trigger TEXT,
    script TEXT NOT NULL,
    actions JSONB DEFAULT '[]',
    hard_stop TEXT,
    metadata JSONB DEFAULT '{{}}',
    chunk_text TEXT NOT NULL,
    embedding vector({EMBEDDING_DIM}) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_scenario_chunks_embedding
ON {SCENARIOS_TABLE}
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 10);
"""

INSERT_SQL = f"""
INSERT INTO {SCENARIOS_TABLE}
(scenario_id, intent, risk, trigger, script, actions, hard_stop, metadata, chunk_text, embedding)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (scenario_id) DO UPDATE SET
    intent = EXCLUDED.intent,
    risk = EXCLUDED.risk,
    trigger = EXCLUDED.trigger,
    script = EXCLUDED.script,
    actions = EXCLUDED.actions,
    hard_stop = EXCLUDED.hard_stop,
    metadata = EXCLUDED.metadata,
    chunk_text = EXCLUDED.chunk_text,
    embedding = EXCLUDED.embedding,
    created_at = NOW();
"""

SELECT_BY_VECTOR_SQL = f"""
SELECT id, scenario_id, intent, risk, trigger, script, actions, hard_stop, metadata, chunk_text, created_at,
       1 - (embedding <=> %s::vector) AS similarity
FROM {SCENARIOS_TABLE}
ORDER BY embedding <=> %s::vector
LIMIT %s;
"""

SELECT_BY_VECTOR_WITH_INTENT_SQL = f"""
SELECT id, scenario_id, intent, risk, trigger, script, actions, hard_stop, metadata, chunk_text, created_at,
       1 - (embedding <=> %s::vector) AS similarity
FROM {SCENARIOS_TABLE}
WHERE (metadata->>'intent') = %s
ORDER BY embedding <=> %s::vector
LIMIT %s;
"""

# Keyword search: PostgreSQL full-text search on chunk_text
SELECT_BY_KEYWORD_SQL = f"""
SELECT id, scenario_id, intent, risk, trigger, script, actions, hard_stop, metadata, chunk_text, created_at,
       ts_rank(to_tsvector('english', chunk_text), plainto_tsquery('english', %s)) AS kw_score
FROM {SCENARIOS_TABLE}
WHERE to_tsvector('english', chunk_text) @@ plainto_tsquery('english', %s)
ORDER BY kw_score DESC
LIMIT %s;
"""

SELECT_BY_KEYWORD_WITH_INTENT_SQL = f"""
SELECT id, scenario_id, intent, risk, trigger, script, actions, hard_stop, metadata, chunk_text, created_at,
       ts_rank(to_tsvector('english', chunk_text), plainto_tsquery('english', %s)) AS kw_score
FROM {SCENARIOS_TABLE}
WHERE (metadata->>'intent') = %s
  AND to_tsvector('english', chunk_text) @@ plainto_tsquery('english', %s)
ORDER BY kw_score DESC
LIMIT %s;
"""
