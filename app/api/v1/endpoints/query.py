"""POST /api/v1/check — flow: Text → Intent → Scenario Retrieval → Safety Check → Action Execution → Response."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Depends

from app.core.config import get_settings
from app.schemas.query import CheckRequest, CheckResponse
from app.services.intent import classify_intent
from app.services.rag import RAGService
from app.services.safety import check_safety

log = logging.getLogger(__name__)
router = APIRouter()


def _get_rag() -> RAGService:
    if not get_settings().openai_api_key:
        raise HTTPException(
            status_code=503,
            detail="RAG service unavailable: OPENAI_API_KEY not configured",
        )
    return RAGService()


def _execute_actions(scenario_id: str, intent: str, brain: str) -> None:
    """Action execution step: log or call EMR/notify in production."""
    log.info("Action execution: scenario_id=%s intent=%s brain=%s", scenario_id, intent, brain)
    # Production: trigger EMR API, send SMS, create task, etc.


@router.post("/check", response_model=CheckResponse)
def check_question(
    body: CheckRequest,
    rag: RAGService = Depends(_get_rag),
) -> CheckResponse:
    """
    Flow:
      1. Intent Detection
      2. Scenario Retrieval (RAG by intent)
      3. Safety Check (override response if emergency)
      4. Action Execution (log / side effects)
      5. Response
    """
    question = body.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question is required")

    # 1) Intent Detection
    intent = classify_intent(question)

    # 2) Scenario Retrieval
    top_k = get_settings().top_k_retrieval
    try:
        results = rag.retrieve(question, top_k=top_k, intent_filter=intent)
    except Exception as e:
        log.exception("RAG retrieve failed: %s", e)
        raise HTTPException(status_code=503, detail="Retrieval failed") from e

    if not results:
        return CheckResponse(
            response="I'm not sure how to help with that. Please call our office and a staff member will assist you.",
        )

    best_scenario, _ = results[0]
    brain = (best_scenario.metadata.get("brain") or "")
    response_text = best_scenario.script
    scenario_id = best_scenario.scenario_id
    intent_out = best_scenario.intent

    # 3) Safety Check (override response if user message contains emergency phrases)
    is_safe, emergency_response = check_safety(question)
    if not is_safe and emergency_response:
        response_text = emergency_response
        # Optionally clear scenario_id/intent/brain for emergency; keeping them for audit is also valid.

    # 4) Action Execution
    _execute_actions(scenario_id, intent_out, brain)

    # 5) Response
    return CheckResponse(
        response=response_text,
        scenario_id=scenario_id,
        intent=intent_out,
        brain=brain,
    )
