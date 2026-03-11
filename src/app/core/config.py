"""Application configuration — env-based."""
from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

_APP_ROOT = Path(__file__).resolve().parent.parent.parent
_PROJECT_ROOT = _APP_ROOT.parent
SCENARIOS_JSON_PATH = _PROJECT_ROOT / "data" / "scenarios.json"

# Load .env from project root (doctor-twin-demo/.env) then cwd (e.g. src/.env)
_load_env = _PROJECT_ROOT / ".env"
if _load_env.exists():
    load_dotenv(_load_env)
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Scenario RAG API"
    debug: bool = False

    openai_api_key: str = ""  # Set OPENAI_API_KEY in .env only — never hardcode
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"

    database_url: str = "postgresql://localhost:5432/scenario_rag"

    top_k_retrieval: int = 3
    hybrid_search: bool = True  # Combine vector + keyword search for accuracy

    emergency_phrases: str = (
        "chest pain,shortness of breath,stroke,can't breathe,"
        "severe pain,fainting,unconscious,bleeding,suicide,heart attack,emergency,911"
    )

    @property
    def emergency_phrases_list(self) -> list[str]:
        return [p.strip() for p in self.emergency_phrases.split(",") if p.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
