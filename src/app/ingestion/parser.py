"""Scenario parsing helpers.

The project’s canonical ingestion source is `data/scenarios.json`.
If you later want to parse markdown into scenarios.json in-app (instead of repo scripts),
put that logic here.
"""
from __future__ import annotations

from typing import Any


def validate_scenario(obj: dict[str, Any]) -> dict[str, Any]:
    """Light validation/sanitization hook for ingestion."""
    if not obj.get("scenario_id"):
        raise ValueError("scenario_id is required")
    if not obj.get("intent"):
        raise ValueError(f"intent is required for scenario_id={obj.get('scenario_id')}")
    return obj

