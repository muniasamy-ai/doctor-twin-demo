"""Classify user question into scenario intent for accurate retrieval."""
from __future__ import annotations

import json
import logging
from openai import OpenAI

from app.core.config import get_settings

log = logging.getLogger(__name__)

# Intents from scenarios (must match metadata.intent in DB)
INTENTS = [
    "schedule_appointment",
    "reschedule_cancel",
    "symptom_intake_routing",
    "pharmacy_refill_request",
    "controlled_substance_early_refill",
    "patient_medication_refill",
    "routine_refill",
    "refill_overdue_labs",
    "refill_overdue_visit",
    "controlled_substance_refill",
    "controlled_refill_request",
    "short_bridge_refill",
    "denied_refill",
    "pharmacy_change_request",
    "medication_side_effect_report",
    "referral_request_medicare_ppo",
    "referral_request_hmo",
    "billing_question",
    "records_school_form_request",
    "abnormal_lab_callback",
    "critical_lab_result",
    "urgent_symptoms_triage",
    "general_medical_question",
    "lab_result_inquiry",
    "after_hours_call",
    "prescription_refill_request_phone",
    "prior_authorization_required",
    "eligibility_verification",
]


def classify_intent(question: str, api_key: str | None = None) -> str:
    """
    Use OpenAI to pick the single best matching intent for the user question.
    Returns intent string (e.g. schedule_appointment) or general_medical_question as fallback.
    """
    settings = get_settings()
    key = api_key or settings.openai_api_key
    if not key:
        return "general_medical_question"
    client = OpenAI(api_key=key)
    intents_str = ", ".join(INTENTS)
    prompt = f"""You are a medical office intent classifier. Choose the ONE best matching intent. Reply with ONLY the intent string, nothing else.

RULES:
1. SYMPTOM + appointment request (pain, headache, head pain, not feeling well, sick, unwell, dizzy) → symptom_intake_routing
2. Routine booking without symptoms (follow-up, make appointment, see doctor) → schedule_appointment
3. Reschedule or cancel → reschedule_cancel
4. Medication refill - patient specifies med name → routine_refill OR patient_medication_refill (if unclear, use patient_medication_refill)
5. Controlled substance refill (Xanax, pain med, opioid, benzo) → controlled_refill_request or controlled_substance_refill
6. Pharmacy calls for refill → pharmacy_refill_request
7. Change pharmacy → pharmacy_change_request
8. Referral - Medicare/PPO → referral_request_medicare_ppo; HMO → referral_request_hmo; unclear → referral_request_medicare_ppo
9. Billing, invoice, copay, refund → billing_question
10. Records, medical records, school form → records_school_form_request
11. Lab results question → lab_result_inquiry
12. Insurance, eligibility, benefits → eligibility_verification
13. Prior auth, insurance denied med → prior_authorization_required
14. Medication side effects → medication_side_effect_report
15. Urgent symptoms (chest pain, can't breathe, stroke) → urgent_symptoms_triage
16. After hours, office closed → after_hours_call

Available intents: {intents_str}

User: "{question}"
Intent:"""

    try:
        resp = client.chat.completions.create(
            model=settings.chat_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        text = (resp.choices[0].message.content or "").strip().lower()
        # Extract intent: handle "intent_name" or "the intent is intent_name" or just "intent_name"
        for intent in INTENTS:
            if intent in text or text.endswith(intent) or text == intent:
                return intent
        return "general_medical_question"
    except Exception as e:
        log.warning("Intent classification failed: %s", e)
        return "general_medical_question"
