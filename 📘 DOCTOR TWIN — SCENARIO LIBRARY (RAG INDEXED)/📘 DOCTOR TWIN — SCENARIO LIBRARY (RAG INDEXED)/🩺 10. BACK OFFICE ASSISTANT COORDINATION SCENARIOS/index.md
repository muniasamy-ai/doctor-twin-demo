# 🩺 10. BACK OFFICE ASSISTANT COORDINATION SCENARIOS

# 10.1 Task Delegation
SCENARIO ID: BACK-TASK-001
BRAIN: Workflow Coordinator
CHANNEL: Internal staff system
INTENT: Assign operational task
RISK: Low
SUCCESS: Task routed to correct staff member
Trigger
Task generated from:
- physician instruction
- patient request
- lab result workflow
- referral process
Script
“I’m assigning this task so it can be completed promptly.”
Task Information
Task must include:
- patient name
- task description
- priority level
- responsible staff role
- due date
Actions
- create task ticket
- assign to correct department
- track completion status
- notify responsible staff
# 10.2 Lab Follow-Up Task
SCENARIO ID: BACK-LAB-002
RISK: Moderate
Trigger
Lab results require follow-up action.
Examples:
- abnormal lab value
- repeat lab needed
- physician requested follow-up
Script
“Please contact the patient to schedule follow-up labs or appointment as instructed.”
Actions
- generate follow-up task
- assign to medical assistant
- attach lab result reference
- track completion
# 10.3 Referral Coordination Task
SCENARIO ID: BACK-REF-003
Trigger
Referral ordered by physician.
Required Steps
Confirm:
- referral specialty
- insurance requirements
- preferred specialist
Script
“Please coordinate the referral and notify the patient once scheduled.”
Actions
- verify insurance rules
- prepare referral documentation
- send referral to specialist office
- notify patient
# 10.4 Prior Authorization Routing
SCENARIO ID: BACK-PA-004
RISK: Moderate
Trigger
Medication, imaging, or procedure requires prior authorization.
Script
“This request requires insurance authorization before proceeding.”
Required Information
- CPT code
- diagnosis code
- clinical notes
- supporting documentation
Actions
- route task to authorization specialist
- attach necessary documentation
- track authorization status
# 10.5 Missing Documentation Reminder
SCENARIO ID: BACK-DOC-005
Trigger
Incomplete documentation detected.
Examples:
- unsigned note
- missing lab order justification
- incomplete referral form
Script
“A required document appears incomplete. Please review and complete the documentation.”
Actions
- notify responsible staff
- link incomplete document
- log reminder
# 10.6 Scheduling Coordination with Staff
SCENARIO ID: BACK-SCHED-006
Trigger
Complex scheduling case.
Examples:
- multiple appointments
- procedure + follow-up
- coordination with outside provider
Script
“Please coordinate scheduling to ensure the patient receives all required services.”
Actions
- assign task to scheduling team
- confirm availability
- notify patient once scheduled
# 10.7 Escalation to Nurse
SCENARIO ID: BACK-NURSE-007
RISK: Moderate
Trigger
Clinical issue requiring nursing review.
Examples:
- medication side effects
- wound care question
- symptom assessment
Script
“I’m routing this message to the nursing team for clinical review.”
Actions
- assign to nurse queue
- attach patient message
- mark priority level
# 10.8 Escalation to Physician
SCENARIO ID: BACK-PHYS-008
RISK: Moderate–High
Trigger
Issue requires physician decision.
Examples:
- medication change request
- abnormal result interpretation
- patient complaint involving care plan
Script
“This matter requires physician review. I will forward it to the doctor.”
Actions
- notify physician dashboard
- attach related documentation
- track physician response
# ENGINEERING RULES FOR BACK OFFICE MODULE
The system must enforce:
Clear Role Routing
Tasks routed to:
- Front desk
- Medical assistant
- Nurse
- Billing department
- Physician