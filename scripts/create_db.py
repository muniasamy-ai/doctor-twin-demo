#!/usr/bin/env python3
"""
Create PostgreSQL database for Scenario RAG if it does not exist.
Run before init_db.py. Uses DATABASE_URL to derive DB name; connects to 'postgres' to create.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

_env = ROOT / ".env"
if _env.exists():
    for line in _env.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from app.core.config import get_settings


def main():
    settings = get_settings()
    url = settings.database_url
    parsed = urlparse(url)
    db_name = parsed.path.lstrip("/") or "scenario_rag"
    # Connect to default 'postgres' database to create our DB
    base_url = f"{parsed.scheme}://{parsed.netloc}/postgres"
    try:
        conn = psycopg2.connect(base_url)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,),
        )
        if cur.fetchone():
            print(f"Database '{db_name}' already exists.")
        else:
            cur.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Database '{db_name}' created.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Failed to create database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
