"""Optional re-ranking utilities (e.g., intent boost)."""
from __future__ import annotations

from app.repositories.models import ScenarioRow


def intent_boost(
    results: list[tuple[ScenarioRow, float]],
    intent: str | None,
    boost: float = 0.15,
) -> list[tuple[ScenarioRow, float]]:
    """
    Apply a small score bonus to results whose metadata.intent matches `intent`.
    This is useful when you retrieve without a strict intent filter and want robustness.
    """
    if not intent:
        return results
    out: list[tuple[ScenarioRow, float]] = []
    for row, score in results:
        m_intent = (row.metadata or {}).get("intent")
        out.append((row, score + boost if m_intent == intent else score))
    out.sort(key=lambda x: x[1], reverse=True)
    return out

