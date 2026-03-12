#!/usr/bin/env python3
"""
Run pending database migrations only (no seed).
Use when deploying or when schema is managed separately from data.
Run from src: python -m scripts.run_migrations
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

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

from app.db import run_migrations


def main() -> None:
    try:
        run_migrations()
        print("Migrations completed.")
    except Exception as e:
        print(f"Migrations failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
