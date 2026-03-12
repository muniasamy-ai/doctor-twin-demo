"""
001: Create pgvector extension and scenario_chunks table with IVFFlat index.
"""
from __future__ import annotations

EMBEDDING_DIM = 1536
SCENARIOS_TABLE = "scenario_chunks"


def upgrade(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute(
            f"""
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
            """
        )
        cur.execute(
            f"""
            CREATE INDEX IF NOT EXISTS idx_scenario_chunks_embedding
            ON {SCENARIOS_TABLE}
            USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 10);
            """
        )
    conn.commit()
