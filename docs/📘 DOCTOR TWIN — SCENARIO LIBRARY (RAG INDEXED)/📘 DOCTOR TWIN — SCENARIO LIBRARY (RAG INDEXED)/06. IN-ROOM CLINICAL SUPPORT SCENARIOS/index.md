#  06. IN-ROOM CLINICAL SUPPORT SCENARIOS

# 06.1 Pre-Visit Summary Briefing
SCENARIO ID: CLIN-PREVISIT-001
BRAIN: Clinical Assistant
CHANNEL: In-Room / Physician Dashboard
INTENT: Physician briefing before entering room
RISK: Low
REQUIRES CONFIRMATION: None
SUCCESS: Physician receives structured summary
Trigger
Doctor opens patient chart or enters exam room.
Data Sources Retrieved
- Patient demographics
- Problem list
- Last visit summary
- Current medications
- Recent labs / imaging
- Outstanding tasks
Summary Format
Patient Snapshot
Patient: Sarah Johnson
Age: 58
Primary Conditions: Hypertension, Type 2 Diabetes
Last Visit
3 months ago for BP follow-up.
Recent Labs
A1c: 7.5 (slightly elevated)
LDL: 112
Current Medications
- Lisinopril 10 mg
- Metformin 1000 mg BID
Outstanding Items
- Due for diabetic eye exam
- Lifestyle counseling recommended
Actions
- Generate summary panel
- Highlight abnormal labs
- Flag overdue screenings
# 06.2 SOAP Drafting Support
SCENARIO ID: CLIN-SOAP-002
BRAIN: Documentation Assistant
INTENT: Draft structured note during visit
Trigger
Doctor dictates or enters encounter notes.
SOAP Draft Structure
S — Subjective
Patient reports worsening fatigue for 2 weeks.
Denies chest pain or shortness of breath.
O — Objective
BP: 142/88
Pulse: 76
Weight: 180 lbs
A — Assessment
- Hypertension — suboptimal control
- Type 2 diabetes — moderate control
P — Plan
- Adjust BP medication
- Repeat A1c in 3 months
- Lifestyle counseling
Safety Rule
Doctor Twin never finalizes the note.
Physician must review and approve.
Actions
- Auto-populate SOAP template
- Insert structured vitals and labs
- Await physician confirmation
# 06.3 Coding Suggestion (CPT / ICD Support)
SCENARIO ID: CLIN-CODE-003
BRAIN: Billing Intelligence
Trigger
Encounter nearing completion.
Coding Suggestions
Based on documentation:
Visit Level Suggestion
99214 — Established patient, moderate complexity
Diagnosis Codes
E11.9 — Type 2 diabetes
I10 — Hypertension
Safety Rule
Doctor Twin suggests only.
Physician confirms final codes.
Actions
- Analyze documentation
- Suggest CPT + ICD codes
- Flag documentation gaps
# 06.4 Order Suggestion
SCENARIO ID: CLIN-ORDER-004
RISK: Moderate
Trigger
Diagnosis or symptoms discussed during visit.
Example Logic
Condition: Diabetes
Suggested orders:
- Hemoglobin A1c
- Lipid panel
- Microalbumin
Script
“Based on this condition, these labs are typically monitored.”
Safety Rule
Orders appear as suggestions, not auto-submitted.
Actions
- Retrieve evidence-based protocols
- Suggest labs or imaging
- Await physician approval
# 06.5 Medication Reconciliation
SCENARIO ID: CLIN-MEDREC-005
Trigger
Visit begins or medications discussed.
Process
Compare:
- Medication list in chart
- Patient reported medications
- Pharmacy fill history (if available)
Script
“Let’s confirm your current medications.”
Possible Findings
- Duplicate medications
- Discontinued drugs still listed
- Missing medications
Actions
- Highlight discrepancies
- Suggest updates
- Log reconciliation
# 06.6 Follow-Up Plan Suggestion
SCENARIO ID: CLIN-FOLLOW-006
Trigger
Visit nearing completion.
Suggested Plan Structure
Follow-up timeframe:
- 3 months diabetes check
- Repeat labs prior to visit
Script
“A follow-up visit in three months is typically recommended.”
Actions
- Suggest timeline
- Offer scheduling
- Add reminders
# 06.7 Patient Education Scripting
SCENARIO ID: CLIN-EDU-007
Trigger
Doctor discussing diagnosis or treatment.
Example
Condition: Hypertension
Suggested explanation:
“High blood pressure increases the risk of heart disease and stroke. Managing it with medication, diet, and exercise can significantly reduce those risks.”
Safety Rule
Education must match:
- Physician plan
- Verified medical sources
Actions
- Display patient-friendly explanation
- Offer printable education materials
# 06.8 In-Room Staff Instruction
SCENARIO ID: CLIN-STAFF-008
Trigger
Doctor requests staff assistance.
Examples
“Please schedule this patient for labs.”
“Arrange cardiology referral.”
Script
Instruction generated:
“Front desk: schedule follow-up in 3 months.”
Actions
- Send task to staff dashboard
- Track completion
# 06.9 After-Visit Summary Drafting
SCENARIO ID: CLIN-AVS-009
Trigger
Visit completed.
After-Visit Summary Content
Diagnosis
Hypertension
Type 2 Diabetes
Medications
Continue Lisinopril
Continue Metformin
Next Steps
- Complete labs in 3 months
- Follow low-salt diet
- Exercise regularly
Follow-Up
Return visit in 3 months.
Actions
- Generate patient-friendly summary
- Attach to portal/app
- Allow physician edit before sending
# ENGINEERING RULES FOR IN-ROOM CLINICAL BRAIN
Doctor Twin must:
1️⃣ Never diagnose independently
2️⃣ Never override physician decisions
3️⃣ Always present suggestions clearly labeled
4️⃣ Require physician approval for:
- Orders
- Prescriptions
- Coding
- Final notes
Data Sources for Retrieval
- Patient chart
- Practice protocols
- Physician preference templates
- Clinical guidelines
- Prior encounter notes