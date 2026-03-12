# 2️⃣SCENARIO:  Refill Request

# 💊 02. MEDICATION & REFILL SCENARIOS
# 02.1 Routine Refill (Eligible for Auto-Approval)
SCENARIO ID: RX-ROUTINE-001
BRAIN: Physician Assistant
CHANNEL: Phone / Portal / Pharmacy
INTENT: Routine refill
RISK: Low
REQUIRES CONFIRMATION: None (if criteria met)
CAN EXECUTE: Send refill
SUCCESS: Refill sent + patient notified
Trigger
- Chronic medication
- Same dose
- Same pharmacy
- Seen within 12 months
- Labs not critically overdue
Silent Safety Checks
- Active medication on list
- No stop/hold flags
- No recent adverse reaction
- Labs acceptable
Script (Patient)
“Your refill has been sent to your pharmacy. Please let us know if you notice any side effects.”
Actions
- Send refill (standard quantity)
- Notify via SMS/email
- Log audit trail
- Passive physician notification
# 02.2 Refill With Overdue Labs (Mildly Overdue)
SCENARIO ID: RX-LABS-002
RISK: Moderate
Trigger
- Labs required for medication monitoring
- Labs overdue but not critical
Script
“I’ve sent a short refill to keep you covered. Please complete your lab work as soon as possible to continue safely.”
Actions
- Send 30–90 day refill
- Place lab order
- Send lab reminder
- Log as short refill due to labs
# 02.3 Refill With Overdue Visit
SCENARIO ID: RX-VISIT-003
RISK: Moderate
Trigger
- Last visit >12 months
- Stable chronic medication
Script
“I’ve sent a short refill and scheduled a reminder for your follow-up visit to keep everything on track.”
Actions
- Send limited refill
- Offer scheduling
- Flag visit overdue
- Log decision
# 02.4 Controlled Substance Refill
SCENARIO ID: RX-CONTROL-004
RISK: High
REQUIRES CONFIRMATION: Physician
Trigger
- Controlled medication
- Opioid, benzodiazepine, stimulant, sleep med
Script
“Controlled medications require direct physician review. I’ve routed your request for prompt attention.”
No timeline guarantees.
Actions
- Create high-priority refill task
- Notify physician
- Do NOT auto-approve
- Log request
# 02.5 Short Bridge Refill (Continuity Priority)
SCENARIO ID: RX-BRIDGE-005
RISK: Moderate
Trigger
- Patient out of medication
- Follow-up pending
- Condition high-risk (HTN, CAD, DM, thyroid)
Script
“I’ve sent a short refill to prevent interruption. Let’s schedule your follow-up to review your care plan.”
Actions
- Send 30-day refill
- Auto-schedule reminder
- Flag continuity safeguard
- Log bridge refill
# 02.6 Denied Refill With Explanation
SCENARIO ID: RX-DENY-006
RISK: Variable
Trigger
- Medication inappropriate
- Labs critically overdue
- Visit severely overdue
- Controlled early refill
Script
“This refill requires physician review to ensure safety. We’ll follow up with next steps.”
If inappropriate:
“This medication cannot be refilled without an updated evaluation.”
Actions
- Escalate to physician
- Offer visit scheduling
- Log denial reason
# 02.7 Refill Requiring Escalation (Complex Case)
SCENARIO ID: RX-ESC-007
RISK: High
Trigger
- Multiple medications
- Polypharmacy concern
- Drug interaction warning
- Significant side effects reported
Script
“This refill needs careful review to ensure safety. I’m escalating this to the doctor.”
Actions
- Clinical escalation
- Flag drug interaction
- Create high-priority review task
# 02.8 Pharmacy Change Request
SCENARIO ID: RX-PHARM-008
RISK: Low
Trigger
- “I changed pharmacies.”
- Pharmacy closure
Script
“Thank you for the update. I’ll send your prescription to the new pharmacy.”
Required Data
- New pharmacy name
- Address or store number
- Phone number
Actions
- Update pharmacy in EMR
- Resend prescription
- Log change
# 02.9 Medication Discontinued Discussion
SCENARIO ID: RX-DISC-009
RISK: Moderate–High
Trigger
- “I stopped taking it.”
- “I don’t want this medication anymore.”
Script
“I understand. May I ask why you stopped the medication?”
If side effects → route to clinical review
If preference → schedule discussion
If high-risk med → urgent escalation
Actions
- Flag medication status
- Notify physician
- Offer visit
- Log discontinuation report
# Optional Advanced Edge Scenarios (Recommended Additions)
# 02.10 Refill Too Early (Non-Controlled)
Script:
“This refill appears earlier than expected. I’ll confirm eligibility and follow up shortly.”
Action:
Check last fill date before approval.
# 02.11 Duplicate Pharmacy Requests
Script:
“We’ve received multiple refill requests for the same medication. I’ll confirm which one should proceed.”
Prevent duplicate processing.
# 02.12 Refill During Hospitalization
Script:
“I see you were recently hospitalized. The doctor may need to review this medication before refilling.”
Escalate automatically.
# 02.13 Insurance Requires Prior Authorization
Script:
“This medication requires insurance authorization. We’ve started the process and will update you.”
Trigger PA Brain.
# 02.14 Patient Requests Dose Change
Script:
“Dose adjustments require physician review. I’ll forward this to the doctor.”
Escalation only.
# Engineering Summary (Section 02)
Refill Engine must evaluate:
1. Medication classification
1. Visit recency
1. Lab recency
1. Dose consistency
1. Controlled status
1. Interaction flags
1. Adverse reaction history
1. Hospitalization status
Every refill logs:
- Decision type (auto / bridge / denied / escalated)
- Data sources checked
- Timestamp
- User initiating request
- Physician confirmation (if required)
SCENARIO ID: RX-CONTROL-001
BRAIN: Receptionist → Physician Assistant
CHANNEL: Phone / Portal
INTENT: Controlled refill request
RISK LEVEL: High
REQUIRES CONFIRMATION: Physician
CAN EXECUTE: Create task only
SUCCESS CRITERIA: Routed without promise
Trigger
- “I need my Xanax early.”
- “Can you refill my pain medication?”
Script
“For controlled medications, the doctor must review each request individually. I’ll route this for review right away.”
No promise. No timing guarantees.
Actions
- Create High-Priority Refill Task
- Tag as Controlled
- Notify physician queue
# 2️⃣2️⃣ SCENARIO: Medication Side Effect Report
SCENARIO ID: MA-RX-002
BRAIN: Medical Assistant
INTENT: Side effect triage
RISK LEVEL: Moderate–High
Script
“I’m sorry you’re experiencing that. When did this start?”
“Are you having trouble breathing, severe swelling, chest pain, or fainting?”
If severe → emergency escalation
If mild →
“I’ll notify the doctor so we can advise you safely.”
Actions
- Create urgent clinical task
- Flag medication in chart
# SCENARIO: Medication Refill – Labs Overdue
SCENARIO ID: RX-LABS-001
BRAIN: Physician Assistant
RISK: Moderate
REQUIRES CONFIRMATION: None (short refill allowed per policy)
Trigger
Refill requested + labs mildly overdue
Script
“I’ve sent a short refill and scheduled a reminder for your lab work to keep everything safe.”
Actions
- Send 30–90 day refill
- Create lab order task
- Notify patient of lab requirement
- Log decision