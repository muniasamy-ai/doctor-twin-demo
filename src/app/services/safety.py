"""Safety check: emergency guardrails before RAG response."""
from __future__ import annotations

from app.core.config import get_settings

EMERGENCY_SCRIPT = (
    "I'm concerned this may be urgent. Please call 911 or go to the nearest emergency room."
)


def is_emergency(message: str) -> bool:
    """True if message contains any configured emergency phrase."""
    lower = message.lower().strip()
    phrases = get_settings().emergency_phrases_list
    return any(phrase in lower for phrase in phrases)


def check_safety(message: str) -> tuple[bool, str | None]:
    """
    Returns (is_safe, emergency_response_if_any).
    If not safe, return the emergency script; caller should not run normal RAG flow.
    """
    if is_emergency(message):
        return False, EMERGENCY_SCRIPT
    return True, None
