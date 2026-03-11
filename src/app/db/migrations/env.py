"""
Migration environment: runs pending versioned migrations in order.
Tracks applied migrations in schema_migrations table.
"""
from __future__ import annotations

import importlib.util
import logging
from pathlib import Path

import psycopg2

from app.core.config import get_settings

log = logging.getLogger(__name__)

MIGRATIONS_TABLE = "schema_migrations"
VERSIONS_DIR = Path(__file__).resolve().parent / "versions"


def _ensure_migrations_table(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE} (
                version VARCHAR(255) PRIMARY KEY,
                applied_at TIMESTAMPTZ DEFAULT NOW()
            );
            """
        )
    conn.commit()


def _applied_versions(conn) -> set[str]:
    with conn.cursor() as cur:
        cur.execute(f"SELECT version FROM {MIGRATIONS_TABLE}")
        return {row[0] for row in cur.fetchall()}


def _discover_versions() -> list[str]:
    """Return sorted list of version ids (001_..., 002_..., etc.)."""
    if not VERSIONS_DIR.is_dir():
        return []
    names = []
    for p in VERSIONS_DIR.iterdir():
        if p.suffix == ".py" and p.name != "__init__.py" and p.name.startswith("0"):
            names.append(p.stem)
    return sorted(names)


def _run_version(version_id: str, conn) -> None:
    """Load and run upgrade() for a single version module."""
    path = VERSIONS_DIR / f"{version_id}.py"
    if not path.is_file():
        raise FileNotFoundError(f"Migration file not found: {path}")
    spec = importlib.util.spec_from_file_location(f"migrations.versions.{version_id}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load migration: {version_id}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "upgrade"):
        raise AttributeError(f"Migration {version_id} must define upgrade(conn)")
    mod.upgrade(conn)
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO {MIGRATIONS_TABLE} (version) VALUES (%s)",
            (version_id,),
        )
    conn.commit()
    log.info("Applied migration: %s", version_id)


def run_migrations(database_url: str | None = None) -> None:
    """
    Run all pending migrations. Uses DATABASE_URL from config if database_url not provided.
    """
    settings = get_settings()
    url = database_url or settings.database_url
    conn = psycopg2.connect(url)
    try:
        _ensure_migrations_table(conn)
        applied = _applied_versions(conn)
        for version_id in _discover_versions():
            if version_id in applied:
                continue
            _run_version(version_id, conn)
    finally:
        conn.close()
