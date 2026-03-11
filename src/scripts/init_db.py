#!/usr/bin/env python3
"""
Create pgvector extension and scenario_chunks table, then seed with scenarios
from data/scenarios.json (embed with OpenAI text-embedding-3-small).
Run from repo root or rag_api: python -m scripts.init_db
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Ensure app is importable
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

# Load .env
_env = ROOT / ".env"
if _env.exists():
    for line in _env.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

import psycopg2
from pgvector.psycopg2 import register_vector

from app.core.config import get_settings, SCENARIOS_JSON_PATH
from app.models.scenario import (
    CREATE_EXTENSION_SQL,
    SCENARIOS_TABLE,
    CREATE_TABLE_SQL,
    INSERT_SQL,
)
from app.services.rag import load_scenarios_json, _chunk_text, get_embedding


def create_extension_and_table(conn):
    with conn.cursor() as cur:
        cur.execute(CREATE_EXTENSION_SQL)
        cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    print(f"Extension vector and table {SCENARIOS_TABLE} created.")


def seed_embeddings(conn, scenarios_path: Path):
    from openai import OpenAI
    settings = get_settings()
    if not settings.openai_api_key:
        raise SystemExit("OPENAI_API_KEY is required. Set it in .env")
    client = OpenAI(api_key=settings.openai_api_key)
    model = settings.embedding_model

    if not scenarios_path.exists():
        raise SystemExit(f"Scenarios file not found: {scenarios_path}")
    with open(scenarios_path, encoding="utf-8") as f:
        scenarios = json.load(f)

    register_vector(conn)
    cur = conn.cursor()
    try:
        for i, s in enumerate(scenarios):
            chunk = _chunk_text(s)
            emb = get_embedding(client, chunk, model)
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
                    emb,
                ),
            )
            print(f"  Indexed {s.get('scenario_id', '?')}")
        conn.commit()
        print(f"Seeded {len(scenarios)} scenarios.")
    finally:
        cur.close()


def main():
    settings = get_settings()
    try:
        conn = psycopg2.connect(settings.database_url)
    except Exception as e:
        print(f"Cannot connect to database: {e}")
        print("Create the database first, e.g.: createdb scenario_rag")
        sys.exit(1)
    try:
        create_extension_and_table(conn)
        seed_embeddings(conn, SCENARIOS_JSON_PATH)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
