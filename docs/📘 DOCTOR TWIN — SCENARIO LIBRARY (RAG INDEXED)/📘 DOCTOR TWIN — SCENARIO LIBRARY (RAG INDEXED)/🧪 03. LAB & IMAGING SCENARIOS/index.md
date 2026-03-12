# 🧪 03. LAB & IMAGING SCENARIOS

# 03.1 LAB RESULTS
# 03.1.1 Normal Labs Explanation
SCENARIO ID: LAB-NORMAL-001
BRAIN: Medical Assistant
CHANNEL: Phone / Portal
INTENT: Normal lab notification
RISK: Low
REQUIRES CONFIRMATION: Physician reviewed
CAN EXECUTE: Notify patient
SUCCESS: Patient informed + documented
Trigger
- Lab marked normal
- Physician review completed
Script
“Your recent lab results have been reviewed and are within normal limits.”
“If you have any questions, we’re happy to schedule a follow-up visit.”
Hard Stop
If patient reports new symptoms → route to triage.
Actions
- Notify patient
- Log notification
- No automatic visit required unless physician indicated
# 03.1.2 Mild Abnormal Explanation
SCENARIO ID: LAB-MILD-002
RISK: Moderate
Trigger
- Lab slightly outside reference range
- Physician marked non-critical
Script
“One of your lab values is slightly outside the normal range. The doctor would like to review this with you.”
“It is not urgent, but we recommend scheduling a follow-up visit.”
Avoid giving detailed interpretation beyond physician instructions.
Actions
- Offer scheduling
- Attach lab result to visit
- Log discussion
# 03.1.3 Critical Lab Escalation
SCENARIO ID: LAB-CRIT-003
RISK: High
REQUIRES CONFIRMATION: Immediate physician awareness
Trigger
- Lab flagged critical
Script
“This result requires immediate medical attention.”
“If you are experiencing symptoms such as chest pain, shortness of breath, severe weakness, or confusion, please call 911 immediately.”
Actions
- Notify physician immediately
- Attempt patient contact (3 attempts)
- Send urgent message if unreachable
- Log timestamps
# 03.1.4 Repeat Lab Request
SCENARIO ID: LAB-REPEAT-004
RISK: Low–Moderate
Trigger
- Physician ordered repeat testing
Script
“The doctor would like to repeat this lab to confirm the result.”
“I can help schedule your lab appointment.”
Actions
- Place lab order
- Coordinate lab scheduling
- Send secure lab instructions
# 03.1.5 Lifestyle Counseling Follow-Up
SCENARIO ID: LAB-LIFE-005
RISK: Low
Trigger
- Mild elevation (cholesterol, A1c, liver enzymes)
- Physician recommends lifestyle change
Script
“The doctor recommends lifestyle adjustments such as diet and exercise. We can schedule a follow-up to reassess.”
Keep guidance general unless specific instructions documented.
Actions
- Send educational resources
- Schedule follow-up lab
- Log counseling notification
# 03.1.6 Lab Scheduling Coordination
SCENARIO ID: LAB-SCHED-006
RISK: Low
Script
“I can schedule your lab appointment now.”
“Do you prefer morning or afternoon?”
Actions
- Book lab slot (if in-house)
- Provide lab location details
- Send instructions (fasting if required)
# 03.2 IMAGING RESULTS
# 03.2.1 Normal Imaging Explanation
SCENARIO ID: IMG-NORMAL-001
BRAIN: Medical Assistant
RISK: Low
Trigger
- Imaging report reviewed as normal
Script
“Your imaging study was reviewed and shows no concerning findings.”
“If you have persistent symptoms, we can schedule follow-up.”
Actions
- Notify patient
- Log notification
# 03.2.2 Abnormal but Non-Urgent Imaging
SCENARIO ID: IMG-MILD-002
RISK: Moderate
Trigger
- Imaging shows finding requiring follow-up but not urgent
Script
“The imaging showed findings that are not urgent but require follow-up.”
“The doctor recommends scheduling a visit to discuss next steps.”
Avoid detailed interpretation beyond documented summary.
Actions
- Offer visit scheduling
- Attach report to appointment
- Log patient notified
# 03.2.3 Urgent Imaging Result
SCENARIO ID: IMG-URGENT-003
RISK: High
REQUIRES CONFIRMATION: Physician
Trigger
- Imaging flagged urgent
Script
“This imaging result requires urgent attention.”
“If you are experiencing worsening symptoms, please seek emergency care.”
Actions
- Immediate physician alert
- Contact patient urgently
- Log contact attempts
# 03.2.4 Referral Recommendation
SCENARIO ID: IMG-REF-004
RISK: Moderate
Trigger
- Imaging suggests specialist evaluation
Script
“The doctor recommends evaluation by a specialist.”
“I can assist in coordinating your referral.”
Actions
- Determine insurance type (PPO vs HMO)
- Generate referral (if PPO/Medicare)
- Route to Office Manager (if HMO)
- Log referral initiation
# 03.2.5 Follow-Up Scheduling After Imaging
SCENARIO ID: IMG-FOLLOW-005
RISK: Low–Moderate
Trigger
- Imaging complete
- Follow-up required
Script
“Let’s schedule a follow-up visit to review your imaging results.”
Offer live appointment times.
Actions
- Book appointment
- Send confirmation
- Attach imaging report to visit
# ENGINEERING NOTES FOR LAB & IMAGING RAG
System must:
- Never interpret beyond physician-documented summary
- Never invent diagnoses
- Always escalate critical values
- Always log:
  - Who notified
  - When
  - Outcome
  - Escalation if needed
Each result scenario must include:
- Result classification (Normal / Mild / Critical)
- Physician review status
- Patient contact attempt tracking