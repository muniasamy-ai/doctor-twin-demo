#!/usr/bin/env python3
"""
Run database migrations, then seed scenario_chunks from data/scenarios.json
(embed with OpenAI text-embedding-3-small).
Run from src: python -m scripts.init_db
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
from app.db import run_migrations
from app.repositories.models import INSERT_SQL, SCENARIOS_TABLE
from app.services.rag import _chunk_text, get_embedding, load_scenarios_json


def seed_embeddings(scenarios_path: Path) -> None:
    from openai import OpenAI

    settings = get_settings()
    if not settings.openai_api_key:
        raise SystemExit("OPENAI_API_KEY is required. Set it in .env")
    client = OpenAI(api_key=settings.openai_api_key)
    model = settings.embedding_model

    if not scenarios_path.exists():
        raise SystemExit(f"Scenarios file not found: {scenarios_path}")
    scenarios = load_scenarios_json(scenarios_path)

    conn = psycopg2.connect(settings.database_url)
    register_vector(conn)
    cur = conn.cursor()
    try:
        for s in scenarios:
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
        print(f"Seeded {len(scenarios)} scenarios into {SCENARIOS_TABLE}.")
    finally:
        cur.close()
        conn.close()


def main() -> None:
    settings = get_settings()
    try:
        run_migrations()
    except Exception as e:
        print(f"Migrations failed: {e}")
        print("Create the database first, e.g.: python -m scripts.create_db")
        sys.exit(1)
    seed_embeddings(SCENARIOS_JSON_PATH)


if __name__ == "__main__":
    main()
