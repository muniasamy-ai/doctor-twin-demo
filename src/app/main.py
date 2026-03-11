"""FastAPI application — production-grade Scenario RAG API."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.v1 import api_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: validate config. Shutdown: nothing for now."""
    settings = get_settings()
    if not settings.openai_api_key:
        logger.warning("OPENAI_API_KEY not set — /check will return 503")
    yield
    # teardown if needed


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        description="Scenario RAG API: check questions against pgvector-backed scenario knowledge.",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)
    return app


app = create_app()


@app.get("/")
def root():
    """Root: links to health and check API."""
    return {
        "app": "Scenario RAG API",
        "health": "/health",
        "check_question": "POST /api/v1/check",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    """Liveness/readiness."""
    return {"status": "ok"}
