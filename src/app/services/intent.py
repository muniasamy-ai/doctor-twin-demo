"""Classify user question into scenario intent for accurate RAG retrieval."""
from __future__ import annotations

import json
import logging
from pathlib import Path

from openai import OpenAI

from app.core.config import get_settings, SCENARIOS_JSON_PATH

log = logging.getLogger(__name__)

# Load intents from scenarios.json so classifier and RAG stay in sync (must match metadata.intent in DB)
def _load_intents() -> list[str]:
    path = SCENARIOS_JSON_PATH
    if not path.exists():
        log.warning("Scenarios file not found at %s; using default intents", path)
        return [
            "schedule_appointment",
            "reschedule_cancel",
            "symptom_intake_routing",
            "general_medical_question",
        ]
    try:
        with open(path, encoding="utf-8") as f:
            scenarios = json.load(f)
    except Exception as e:
        log.warning("Failed to load scenarios for intents: %s", e)
        return ["schedule_appointment", "reschedule_cancel", "general_medical_question"]
    intents = set()
    for s in scenarios:
        intent = (s.get("metadata") or {}).get("intent") or s.get("intent")
        if intent:
            intents.add(intent)
    # Stable order, with common fallback last
    fallback = "general_medical_question"
    ordered = sorted(intents)
    if fallback in ordered:
        ordered.remove(fallback)
        ordered.append(fallback)
    return ordered


INTENTS = _load_intents()

_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "intent_classifier.txt"


def _load_prompt_template() -> str:
    if _PROMPT_PATH.exists():
        return _PROMPT_PATH.read_text(encoding="utf-8")
    return ""


def classify_intent(question: str, api_key: str | None = None) -> str:
    """
    Use OpenAI to pick the single best matching intent for the user question.
    Intent is the main driver for routing and RAG retrieval — accuracy here is critical.
    Returns intent string (e.g. schedule_appointment) or general_medical_question as fallback.
    """
    settings = get_settings()
    key = api_key or settings.openai_api_key
    if not key:
        return "general_medical_question"
    client = OpenAI(api_key=key)
    intents_str = ", ".join(INTENTS)
    template = _load_prompt_template()
    if template:
        prompt = (
            template.replace("{INTENTS}", intents_str).replace("{QUESTION}", question)
        )
    else:
        prompt = f"""You are a medical office intent classifier. Choose the ONE best matching intent. Reply with ONLY the intent string.

Available intents: {intents_str}

User: \"{question}\"
Intent:"""

    try:
        resp = client.chat.completions.create(
            model=settings.chat_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        text = (resp.choices[0].message.content or "").strip().lower()
        for intent in INTENTS:
            if intent in text or text.endswith(intent) or text == intent:
                return intent
        return "general_medical_question"
    except Exception as e:
        log.warning("Intent classification failed: %s", e)
        return "general_medical_question"
