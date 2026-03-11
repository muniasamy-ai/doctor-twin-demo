# 🏢 09. OFFICE MANAGER / ADMINISTRATIVE SCENARIOS

# 09.1 Staff Escalation
SCENARIO ID: ADMIN-STAFF-001
BRAIN: Office Manager
CHANNEL: Internal staff communication
INTENT: Escalate operational issue to leadership
RISK: Moderate
SUCCESS: Issue routed to correct authority
Trigger
Staff reports:
- workflow breakdown
- unresolved patient issue
- scheduling conflict
- billing problem requiring supervisor
Script
“Thank you for bringing this to attention. I will escalate this to the appropriate supervisor so it can be reviewed promptly.”
Actions
- Identify responsible department
- Create escalation task
- Notify office manager or physician
- Log escalation event
# 09.2 Internal Conflict Resolution
SCENARIO ID: ADMIN-CONFLICT-002
RISK: Moderate
Trigger
Staff disagreement or workflow dispute.
Examples:
- scheduling disagreement
- billing responsibility dispute
- front/back office coordination issue
Script
“Let’s review the situation so we can resolve it constructively.”
“Our goal is to ensure the best patient care and team collaboration.”
Resolution Steps
1️⃣ Clarify roles
2️⃣ Review practice policy
3️⃣ Suggest resolution path
Actions
- Document issue
- Escalate to office manager if unresolved
- Log resolution attempt
# 09.3 Service Complaint
SCENARIO ID: ADMIN-COMPLAINT-003
RISK: Reputation management
Trigger
Patient expresses dissatisfaction about service.
Examples:
- long wait time
- staff behavior
- scheduling difficulty
Script
“I’m sorry that your experience did not meet expectations.”
“We truly value your feedback and want to address this appropriately.”
Resolution Logic
Gather information:
- date of visit
- nature of complaint
- desired resolution
Actions
- Document complaint
- Notify office manager
- Initiate service recovery process
# 09.4 Patient Dissatisfaction
SCENARIO ID: ADMIN-DISSAT-004
Trigger
Patient expresses frustration but not formal complaint.
Examples:
- unhappy with care
- confusion about treatment
- negative experience
Script
“I understand your concern, and we want to make sure your experience improves.”
“Let’s see how we can help address this.”
Resolution Options
- offer follow-up visit
- clarify misunderstanding
- escalate to physician if clinical
Actions
- document concern
- route to appropriate department
# 09.5 Policy Explanation
SCENARIO ID: ADMIN-POLICY-005
Trigger
Patient asks about clinic rules.
Examples:
- cancellation policy
- no-show fees
- refill policy
- late arrival policy
Script
“Our practice policies are designed to ensure fair scheduling and patient care.”
Then explain policy clearly.
Example:
“If an appointment is missed without notice, a fee may apply because that time was reserved for your care.”
Actions
- reference official practice policy
- send policy document if needed
- log explanation
# 09.6 Pricing Explanation
SCENARIO ID: ADMIN-PRICE-006
Trigger
Patient asks:
- “How much does this visit cost?”
- “What is the price of this service?”
Script
“I can provide an estimate based on the service type.”
Explain:
- visit cost range
- insurance variability
- possible additional services
Important Rule
Never guarantee final cost.
Actions
- retrieve service fee schedule
- provide estimate
- document conversation
# 09.7 Membership Questions
SCENARIO ID: ADMIN-MEMBER-007
Trigger
Patient asks about membership plans.
Examples:
- wellness membership
- concierge medicine
- MedSpa subscription
Script
“Our membership plans are designed to provide enhanced services and benefits.”
Explain:
- monthly cost
- included services
- appointment priority if applicable
Actions
- provide membership brochure
- offer enrollment instructions
- log interest
# 09.8 VIP / Concierge Patient Handling
SCENARIO ID: ADMIN-VIP-008
RISK: Reputation / relationship management
Trigger
VIP or concierge patient interaction.
Examples:
- high-profile patient
- concierge membership patient
- executive care
Script
“Thank you for reaching out. We will make every effort to assist you promptly.”
Priority Handling
- faster scheduling
- direct physician communication if needed
- concierge workflow
Actions
- flag VIP status
- route request to priority queue
- notify physician if needed
# ENGINEERING RULES FOR OFFICE MANAGER MODULE
The AI must enforce:
Neutral Communication
Always professional and calm.
Never blame:
- patient
- staff
- insurance
Escalation Path
Issues escalate to:
1️⃣ department supervisor
2️⃣ office manager
3️⃣ physician (if clinical)
Documentation
All administrative interactions must log:
- issue type
- response provided
- escalation status
- resolution outcome