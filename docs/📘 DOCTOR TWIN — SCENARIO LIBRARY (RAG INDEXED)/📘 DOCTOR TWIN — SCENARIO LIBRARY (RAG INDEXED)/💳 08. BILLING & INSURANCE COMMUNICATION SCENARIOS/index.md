# 💳 08. BILLING & INSURANCE COMMUNICATION SCENARIOS

# 08.1 Copay Explanation
SCENARIO ID: BILL-COPAY-001
BRAIN: Billing Assistant
CHANNEL: Phone / Portal / In-person
INTENT: Explain copay responsibility
RISK: Low
REQUIRES CONFIRMATION: Patient identity
SUCCESS: Patient understands copay responsibility
Trigger
Patient asks:
- “Why do I have to pay a copay?”
- “I thought my insurance covered this visit.”
Verification
Confirm:
- Patient name
- DOB
- Insurance plan
Script (Simple Language)
“A copay is the portion of the visit cost that your insurance requires you to pay at the time of service.”
“The amount is determined by your insurance plan.”
If Copay Type Clarification Needed
Explain categories:
- Primary care visit copay
- Specialist copay
- Telemedicine copay
Actions
- Verify insurance plan benefits
- Confirm copay amount
- Log explanation provided
# 08.2 Statement Clarification
SCENARIO ID: BILL-STMT-002
INTENT: Explain patient statement
Trigger
Patient states:
- “I received a bill and don’t understand it.”
Script
“I’m happy to review the statement with you.”
“This statement shows the services provided, what your insurance paid, and the remaining balance.”
Explanation Structure
Break into 3 components:
1️⃣ Service charge
2️⃣ Insurance payment
3️⃣ Remaining patient responsibility
Actions
- Pull billing statement
- Explain charges line-by-line if needed
- Document explanation
# 08.3 CPT Explanation (Simple Language)
SCENARIO ID: BILL-CPT-003
RISK: Low
Trigger
Patient asks:
- “What is this CPT code?”
- “Why am I charged for this service?”
Script
“CPT codes are standardized codes used to describe medical services provided during your visit.”
Example:
99214
“This code represents an established patient visit that required moderate medical decision-making.”
Important Rule
Do not explain medical diagnosis unless already documented and visible to patient.
Actions
- Identify CPT code
- Provide simple explanation
- Log clarification
# 08.4 Insurance Denial Explanation
SCENARIO ID: BILL-DENIAL-004
RISK: Moderate
Trigger
Patient asks:
- “Why did insurance deny this claim?”
Script
“Your insurance reviewed the claim and determined it was not covered under your current plan.”
Possible reasons:
- Service not covered
- Prior authorization required
- Deductible not met
- Coding issue
Follow-Up
“We can help review the denial and determine the next steps.”
Actions
- Retrieve denial reason
- Explain denial code
- Route to billing specialist if appeal possible
# 08.5 Payment Plan Discussion
SCENARIO ID: BILL-PPLAN-005
RISK: Low
Trigger
Patient states:
- “I can’t pay the full amount right now.”
Script
“We understand medical expenses can be difficult. We may be able to set up a payment plan.”
Plan Options (Example)
- Monthly payment arrangement
- Partial payment today
- Scheduled billing
Compliance Rule
Payment plans must follow practice policy.
Doctor Twin cannot approve special financial arrangements beyond policy.
Actions
- Review outstanding balance
- Offer plan options
- Document payment agreement
# 08.6 Refund Inquiry
SCENARIO ID: BILL-REFUND-006
RISK: Low–Moderate
Trigger
Patient asks:
- “Why did I receive a refund?”
- “Am I owed money back?”
Script
“A refund may occur if your insurance paid more than expected or if an overpayment was made.”
Investigation Steps
Check:
- Insurance adjustments
- Duplicate payment
- Billing correction
Actions
- Verify refund reason
- Confirm refund method
- Log refund explanation
# 08.7 Technical Portal Billing Issue
SCENARIO ID: BILL-TECH-007
RISK: Low
Trigger
Patient reports:
- Portal payment not working
- Unable to view statement
- Payment failed
Script
“I’m sorry you’re experiencing a portal issue. Let’s try to resolve it.”
Troubleshooting Steps
1️⃣ Confirm patient login status
2️⃣ Check portal service status
3️⃣ Offer alternate payment options
Actions
- Reset portal session if needed
- Escalate to technical support
- Log issue
# ENGINEERING RULES FOR BILLING MODULE
Doctor Twin must enforce:
Identity Verification
Before discussing billing details.
Billing Data Sources
Retrieve from:
- Practice management system
- Insurance explanation of benefits (EOB)
- Patient statement ledger
Financial Safety Rules
Doctor Twin must never:
- Modify billing codes
- Promise insurance coverage
- Approve financial waivers
Audit Logging
Log:
- Patient inquiry type
- Explanation given
- Escalation if needed