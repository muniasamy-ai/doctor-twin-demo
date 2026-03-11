#!/usr/bin/env python3
"""
Export or import the full database (schema + data) for migration.
Uses pg_dump (export) and psql (import); requires PostgreSQL client tools on PATH.

Usage:
  python -m scripts.migrate_db export [output_file]
  python -m scripts.migrate_db import <input_file>

Default export file: migration_backup.sql
"""
from __future__ import annotations

import logging
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

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

from app.core.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger(__name__)


def _parse_db_url(url: str) -> tuple[str, int, str, str, str]:
    """Return (host, port, user, password, dbname). Handles percent-encoded password."""
    parsed = urlparse(url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 5432
    path = (parsed.path or "").strip("/") or "scenario_rag"
    user = (unquote(parsed.username) if parsed.username else None) or os.environ.get("USER", "postgres")
    password = unquote(parsed.password) if parsed.password else ""
    return host, port, user, password, path


def cmd_export(out_path: str) -> int:
    settings = get_settings()
    host, port, user, password, dbname = _parse_db_url(settings.database_url)
    env = os.environ.copy()
    if password:
        env["PGPASSWORD"] = password
    out_file = Path(out_path)
    if out_file.exists():
        log.warning("Output file already exists and will be overwritten: %s", out_path)
    try:
        subprocess.run(
            [
                "pg_dump",
                "-h", host,
                "-p", str(port),
                "-U", user,
                "-d", dbname,
                "--no-owner",
                "--no-acl",
                "-f", out_path,
            ],
            env=env,
            check=True,
        )
        log.info("Exported to %s", out_path)
        return 0
    except FileNotFoundError:
        log.error(
            "pg_dump not found. Install PostgreSQL client tools (e.g. postgresql-client)."
        )
        return 1
    except subprocess.CalledProcessError as e:
        log.error("pg_dump failed with exit code %s", e.returncode)
        return 1


def cmd_import(in_path: str) -> int:
    settings = get_settings()
    host, port, user, password, dbname = _parse_db_url(settings.database_url)
    env = os.environ.copy()
    if password:
        env["PGPASSWORD"] = password
    in_file = Path(in_path)
    if not in_file.is_file():
        log.error("File not found or not a file: %s", in_path)
        return 1
    try:
        subprocess.run(
            [
                "psql",
                "-h", host,
                "-p", str(port),
                "-U", user,
                "-d", dbname,
                "--single-transaction",
                "-v", "ON_ERROR_STOP=1",
                "-f", in_path,
            ],
            env=env,
            check=True,
        )
        log.info("Imported from %s", in_path)
        return 0
    except FileNotFoundError:
        log.error(
            "psql not found. Install PostgreSQL client tools (e.g. postgresql-client)."
        )
        return 1
    except subprocess.CalledProcessError as e:
        log.error(
            "psql import failed. Ensure target DB exists and is empty or compatible; "
            "check stderr above for details."
        )
        return 1


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.migrate_db export [output_file]", file=sys.stderr)
        print("       python -m scripts.migrate_db import <input_file>", file=sys.stderr)
        return 1
    action = sys.argv[1].lower()
    if action == "export":
        out = sys.argv[2] if len(sys.argv) > 2 else "migration_backup.sql"
        return cmd_export(out)
    if action == "import":
        if len(sys.argv) < 3:
            print("Usage: python -m scripts.migrate_db import <input_file>", file=sys.stderr)
            return 1
        return cmd_import(sys.argv[2])
    print("Unknown action. Use 'export' or 'import'.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
