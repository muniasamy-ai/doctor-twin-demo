"""PostgreSQL + pgvector connection (production engine)."""
from __future__ import annotations

from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector

from app.core.config import get_settings

EMBEDDING_DIM = 1536


@contextmanager
def get_connection():
    """Yield a DB connection with pgvector registered."""
    settings = get_settings()
    conn = psycopg2.connect(
        settings.database_url,
        cursor_factory=RealDictCursor,
    )
    register_vector(conn)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
