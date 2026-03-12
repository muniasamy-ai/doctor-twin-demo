"""Schemas for the /check endpoint."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CheckRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class CheckResponse(BaseModel):
    response: str = ""
    scenario_id: str = ""
    intent: str = ""
    brain: str = ""

