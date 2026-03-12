# 📩 04. PATIENT MESSAGING SCENARIOS (PORTAL / APP)

# 04.1 Medical Question Reply (Non-Urgent)
SCENARIO ID: MSG-MED-001
BRAIN: Physician Assistant
CHANNEL: Portal/App
INTENT: General medical question
RISK: Low–Moderate
REQUIRES CONFIRMATION: Physician (if clinical advice given)
CAN EXECUTE: Draft reply
SUCCESS: Safe, documented response
Trigger
- “I have a question about my blood pressure.”
- “Is this medication safe?”
- “What does this result mean?”
Safety Check (Silent)
- Does the message contain emergency keywords?
  - Chest pain
  - Shortness of breath
  - Severe pain
  - Suicidal ideation
If yes → escalate (see 04.7)
Draft Response Template
“Thank you for your message. I understand your concern.”
Provide response ONLY if:
- Answer exists in documented visit plan
- Or informational clarification (non-diagnostic)
If uncertain:
“I’ll review this with the doctor and follow up shortly.”
Actions
- Draft response
- Route to physician if medical interpretation required
- Log message category
# 04.2 Follow-Up Clarification
SCENARIO ID: MSG-FOLLOW-002
INTENT: Clarify previous instructions
Trigger
- “I didn’t understand the instructions.”
- “Can you explain what you meant?”
Script
“Thank you for reaching out. Let me clarify.”
Restate documented plan only.
Do not create new diagnosis or change treatment.
If unclear:
“I’ll confirm with the doctor and update you.”
Actions
- Reference last visit note
- Provide clarification
- Log clarification sent
# 04.3 Symptom Triage via Message
SCENARIO ID: MSG-TRIAGE-003
RISK: Variable
Trigger
- “I have chest pain.”
- “My stomach hurts.”
- “I feel dizzy.”
Step 1: Emergency Filter
If message includes:
- Chest pain
- Shortness of breath
- Stroke symptoms
- Severe bleeding
- Suicidal thoughts
Immediate Response:
“This may be urgent. Please call 911 or go to the nearest emergency room immediately.”
No delay.
Step 2: Non-Emergent Symptoms
“I’m sorry you’re experiencing that. When did this start?”
“Are you having fever, severe pain, or worsening symptoms?”
Actions
- If mild → offer scheduling
- If moderate → route to clinical queue
- Log triage category
# 04.4 Prescription Question
SCENARIO ID: MSG-RX-004
Trigger
- “Did you send my refill?”
- “Can I change the pharmacy?”
- “Is this dose correct?”
Script
“I’m reviewing your medication request.”
If refill status known:
“Your refill was sent on [date] to [pharmacy].”
If pharmacy change:
“Please confirm the new pharmacy details.”
Actions
- Check refill engine
- Update pharmacy if needed
- Log medication message
# 04.5 Referral Request (Portal)
SCENARIO ID: MSG-REF-005
Trigger
- “I need a referral.”
- “Can you send me to a cardiologist?”
Script
“Thank you. May I ask the reason for the referral?”
Determine insurance type:
If PPO/Medicare:
“I’ll generate your referral and send it securely.”
If HMO:
“This requires insurance authorization. We’ll notify you once processed.”
Actions
- Route by insurance logic
- Generate referral OR create task
- Log referral message
# 04.6 Administrative Request
SCENARIO ID: MSG-ADMIN-006
Trigger
- Work note
- School form
- Records copy
- Insurance card update
Script
“I can help with that. I’ll send a secure upload link if additional information is needed.”
Actions
- Send secure link
- Create admin task
- Log request type
# 04.7 Escalation to Urgent Care / ER (Message-Based)
SCENARIO ID: MSG-ER-007
RISK: High
Trigger
Emergency keywords detected.
Immediate Script
“Your symptoms may require urgent evaluation. Please call 911 or go to the nearest emergency room immediately.”
No follow-up questions.
No delay.
Actions
- Flag urgent
- Notify physician
- Log emergency escalation
# 04.8 Mark Resolved + Documentation
SCENARIO ID: MSG-RESOLVE-008
Trigger
Issue completed.
Script
“I’m glad we were able to address your concern. Please let us know if you need anything further.”
Actions
- Mark task as resolved
- Attach final response to chart
- Close message thread
- Log disposition summary
# ENGINEERING NOTES FOR MESSAGE SCENARIOS
Message workflows must:
1. Run emergency keyword detection first.
1. Never provide diagnosis outside documented plan.
1. Never change medication without physician confirmation.
1. Always log:
  - Message category
  - Risk level
  - Response time
  - Escalation (if any)
1. Allow “Awaiting Physician Review” state.
1. Maintain audit trail of:
  - Draft created
  - Edited
  - Approved
  - Sent