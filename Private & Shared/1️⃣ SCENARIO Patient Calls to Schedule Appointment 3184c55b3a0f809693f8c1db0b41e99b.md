# 1️⃣ SCENARIO: Patient Calls to Schedule Appointment

SCENARIO ID: REC-SCHED-001

BRAIN: Receptionist

CHANNEL: Phone

INTENT: Schedule appointment

RISK LEVEL: Low (unless symptoms escalate)

REQUIRES CONFIRMATION: None

CAN EXECUTE: Book appointment directly

SUCCESS CRITERIA: Appointment booked + confirmation sent

**1) When to Use**

- “I need to see the doctor.”
- “I want to make an appointment.”
- “I need a follow-up.”

**2) Required Data**

- Full name
- DOB
- Callback number
- Reason for visit
- Preferred days/times

**3) Hard Stops**

If patient mentions:

- Chest pain
- Shortness of breath
- Stroke symptoms
→
“I’m concerned this may be urgent. Please call 911 or go to the nearest emergency room.”

**4) Script Pack**

Opening:

“Of course — I can help schedule that. Is this for a new concern or a follow-up?”

Clarify reason:

“What is the main reason for the visit?”

Offer real slots (live availability):

“I have availability on Tuesday at 10:30 AM or Thursday at 2:00 PM. Which works better for you?”

Confirm:

“Perfect — I’ve scheduled you for Tuesday at 10:30 AM.”

Closing:

“You’ll receive a confirmation message shortly. If anything changes, you can reply ‘RESCHEDULE’ or call us.”

**5) Actions**

- Book via EMR API
- Trigger SMS/email confirmation
- Schedule reminder (24h + optional 2h)

**6) Disposition Note**

Patient scheduled for [visit type] on [date/time]. Confirmation sent.

# **2️⃣ SCENARIO: Reschedule or Cancel Appointment**

SCENARIO ID: REC-SCHED-002

INTENT: Reschedule/Cancel

**Trigger**

- “I can’t make it.”
- “I need to change my appointment.”

**Script**

“No problem — would you like to reschedule or cancel?”

If reschedule → same live scheduling logic.

If cancel → remove appointment + confirm.

**Actions**

- Modify EMR schedule
- Send confirmation update

# **3️⃣ SCENARIO: Patient Says “I’m Not Feeling Well”**

SCENARIO ID: REC-SYMPTOM-001

INTENT: Symptom intake routing

RISK: Variable

**Script**

“I’m sorry you’re not feeling well. Can you describe what’s happening in one sentence?”

“When did it start?”

“Are you having chest pain, shortness of breath, severe pain, weakness, or fainting?”

If no red flags →

“I can schedule you for evaluation.”

If red flag → emergency script.

**Action**

Route to triage queue OR urgent scheduling slot.

# **4️⃣ SCENARIO: Pharmacy Calls for Routine Refill**

SCENARIO ID: REC-RX-001

INTENT: Pharmacy refill request

RISK: Low unless controlled

**Required Data**

- Pharmacy name
- NPI/store number
- Patient name + DOB
- Medication name

**Script**

“Thank you — I’ll process this request. You’ll receive confirmation once reviewed.”

**Action**

- Send to refill engine
- Create refill task
- Log pharmacy request

# **5️⃣ SCENARIO: Controlled Substance Early Refill**

SCENARIO ID: REC-RX-002

RISK: High

REQUIRES CONFIRMATION: Physician

**Script**

“For controlled medications, the physician must review early refill requests. I’ll route this for review.”

**Action**

Escalate to physician queue immediately.

# **6️⃣ SCENARIO: Patient Requests Medication Refill (Portal or Call)**

SCENARIO ID: REC-RX-003

**Script**

“Which medication are you requesting?”

“Which pharmacy should we send it to?”

If eligible (per refill logic) → auto-approve

If not → route to physician

**Action**

Run refill safety validation engine.

# **7️⃣ SCENARIO: Referral Request (Medicare/PPO)**

SCENARIO ID: REC-REF-001

CAN EXECUTE: Generate referral document

**Script**

“May I ask which specialist you’d like to see and the reason for referral?”

If Medicare/PPO →

“I’ll generate your referral and send it to you securely.”

**Action**

- Generate referral PDF
- Send to patient
- Log as completed

# **8️⃣ SCENARIO: Referral Request (HMO)**

SCENARIO ID: REC-REF-002

CAN EXECUTE: Create task only

**Script**

“HMO referrals require insurance authorization. I’ll submit this for processing and notify you once approved.”

**Action**

- Create referral task for Office Manager
- Status: Pending Authorization

# **9️⃣ SCENARIO: Billing Question**

SCENARIO ID: REC-BILL-001

**Script**

“Are you calling about an invoice, copay/deductible, or a refund?”

“What was the date of service?”

**Action**

Route to Biller Brain queue.

# **🔟 SCENARIO: Records / School Form Request**

SCENARIO ID: REC-REC-001

**Script**

“I can help with that. Would you like this sent through the secure portal?”

If school/work form → verify identity.

**Action**

- Send secure upload link
- Create records request task
- Track completion

# **1️⃣1️⃣ SCENARIO: Abnormal Lab Result (Non-Critical)**

SCENARIO ID: MA-LAB-001

BRAIN: Medical Assistant

CHANNEL: Phone / Portal Message

INTENT: Abnormal lab callback

RISK LEVEL: Moderate

REQUIRES CONFIRMATION: Physician reviewed result

CAN EXECUTE: Notify + schedule follow-up

SUCCESS CRITERIA: Patient informed + follow-up arranged 

**Trigger**

- Lab marked abnormal but not critical
- Physician marked “OK to notify”

**Script**

“Hi, this is calling from Soliman Care. Your recent lab results showed some values slightly outside the normal range.”

“The doctor recommends a follow-up visit to review and discuss next steps.”

If patient asks details:

“The doctor will review everything with you during the appointment.”

**Hard Stop**

If patient reports new severe symptoms → escalate.

**Actions**

- Offer appointment
- Document patient notified
- Attach lab result to visit

# **1️⃣2️⃣ SCENARIO: Critical Lab Result**

SCENARIO ID: MA-LAB-002

RISK LEVEL: High

REQUIRES CONFIRMATION: Immediate physician awareness

**Trigger**

- Lab flagged critical

**Script**

“This is urgent. The doctor needs to speak with you immediately.”

If unreachable:

- Call x3
- Send urgent SMS: “Please contact the office immediately.”

If symptoms present →

“Please go to the nearest emergency room.”

**Actions**

- Notify physician immediately
- Log attempt times
- Mark as high-priority task

# **1️⃣3️⃣ SCENARIO: Prior Authorization Required (New Detection)**

SCENARIO ID: PA-001

BRAIN: Physician Assistant

INTENT: Medication requires PA

**Trigger**

- Pharmacy rejection
- CoverMyMeds alert

**Script to patient**

“Your medication requires insurance authorization. We are working on this and will keep you updated.”

**Actions**

- Pull chart data (ICD-10, prior meds, labs)
- Pre-fill CoverMyMeds
- Create PA task
- Status: Submitted

# **1️⃣4️⃣ SCENARIO: PA Denied – Appeal Draft**

SCENARIO ID: PA-002

RISK: Moderate

REQUIRES CONFIRMATION: Physician signature

**Script to patient**

“Your insurance has denied the medication. We are preparing an appeal on your behalf.”

**Actions**

- Generate appeal letter draft
- Attach chart evidence
- Route to MD for approval
- Update status: Appeal Pending

# **1️⃣5️⃣ SCENARIO: Pre-Visit Intake (Adult)**

SCENARIO ID: MA-INTAKE-001

CHANNEL: Portal / In-room

INTENT: Visit preparation

**Required Fields**

- Chief complaint
- Duration
- Medication list
- Allergies
- New symptoms

**Script**

“To help the doctor prepare, what is the main reason for today’s visit?”

“How long has this been going on?”

**Hard Stop**

If red flags appear → alert physician.

**Action**

Generate “Doctor Brief” summary.

# **1️⃣6️⃣ SCENARIO: Medication Reconciliation Workflow**

SCENARIO ID: MA-MEDREC-001

**Trigger**

- Annual visit
- Hospital follow-up

**Script**

“Are you still taking Lisinopril 10 mg daily?”

“Have there been any changes or side effects?”

**Action**

- Update med list
- Flag discrepancies
- Save reconciliation note

# **1️⃣7️⃣ SCENARIO: Eligibility Verification Intake**

SCENARIO ID: REC-ELIG-001

BRAIN: Receptionist

**Required Data**

- Insurance carrier
- Member ID
- Group number
- Subscriber DOB (if different)

**Script**

“To verify your benefits, I’ll need the insurance member ID and group number.”

“May I send a secure link for you to upload a photo of your insurance card?”

**Action**

- Create eligibility task
- Notify staff queue

# **1️⃣8️⃣ SCENARIO: Imaging Result Abnormal (Non-Critical)**

SCENARIO ID: MA-IMG-001

**Script**

“Your imaging results have been reviewed. The doctor would like to schedule a visit to discuss the findings.”

If patient anxious:

“The doctor will explain everything in detail and answer your questions.”

**Action**

- Offer appointment
- Log patient notified

# **1️⃣9️⃣ SCENARIO: No-Show Appointment Workflow**

SCENARIO ID: BILL-NS-001

BRAIN: Biller

**Trigger**

- Missed appointment

**Script**

“We noticed you missed your appointment today. Would you like to reschedule?”

If policy applies:

“A no-show fee may apply per office policy.”

**Action**

- Apply fee (if policy)
- Offer reschedule
- Log contact

# **2️⃣0️⃣ SCENARIO: Visit Summary Draft (Post Visit)**

SCENARIO ID: PA-VISIT-001

BRAIN: Physician Assistant

**Trigger**

- Visit completed

**Output Structure**

- Diagnosis list
- Medication changes
- Orders placed
- Follow-up timeline

**Script to patient (portal)**

“Your visit summary is now available in your portal.”

**Action**

- Generate structured summary
- Await physician approval
- Publish to portal

- Post-visit flow

# **📞 01.1 PATIENT INCOMING CALLS**

# **SCENARIO: General Medical Question**

SCENARIO ID: REC-CALL-001

BRAIN: Receptionist

INTENT: General medical question

RISK: Variable

CAN EXECUTE: Route only

**Trigger**

- “I have a question about my condition.”
- “Can I ask the doctor something?”

**Script**

“I’m happy to help route your question. May I confirm your full name and date of birth?”

“Can you briefly describe your question?”

If purely administrative → route to correct department

If clinical →

“I’ll send this to the clinical team for review.”

**Action**

Create clinical message task.

# **SCENARIO: Medication Side Effects (Phone)**

SCENARIO ID: REC-CALL-002

**Script**

“I’m sorry you’re experiencing that. When did this start?”

“Are you having trouble breathing, swelling, chest pain, or fainting?”

If yes → emergency escalation

If no →

“I’ll notify the doctor so we can review this safely.”

**Action**

Urgent clinical task.

# **SCENARIO: Lab Result Inquiry**

SCENARIO ID: REC-CALL-003

**Script**

“I’ll check whether your results have been reviewed.”

If reviewed & non-critical:

“The doctor has reviewed them. I can schedule a visit to discuss.”

If pending:

“Your results are still pending review.”

**Action**

Check result status → schedule if needed.

# **SCENARIO: Imaging Result Inquiry**

SCENARIO ID: REC-CALL-004

**Script**

“I’ll confirm whether your imaging report has been received.”

If received:

“The doctor will review and we’ll follow up shortly.”

If abnormal:

Offer visit scheduling.

# **SCENARIO: Urgent Symptoms Triage**

SCENARIO ID: REC-CALL-005

RISK: High

**Script**

“Please describe what’s happening.”

If chest pain, SOB, stroke symptoms:

“This may be an emergency. Please call 911 immediately.”

If non-emergent:

Offer urgent same-day visit.

# **SCENARIO: After-Hours Call**

SCENARIO ID: REC-CALL-006

**Script**

“Our office is currently closed. If this is a medical emergency, call 911.”

If non-emergent:

“I’ll forward this to the on-call provider.”

**Action**

Create after-hours task.

# **SCENARIO: Insurance Question**

SCENARIO ID: REC-CALL-007

**Script**

“Are you calling about eligibility, coverage, or authorization?”

Collect insurance details.

**Action**

Route to eligibility queue.

# **SCENARIO: Billing Question (Phone)**

SCENARIO ID: REC-CALL-008

**Script**

“May I have the date of service?”

“Is this about a copay, deductible, or statement?”

**Action**

Route to Biller Brain.

# **SCENARIO: Prescription Refill Request (Phone)**

SCENARIO ID: REC-CALL-009

**Script**

“Which medication and which pharmacy?”

Run refill safety logic.

# **📞 01.2 PHARMACY CALLS**

# **SCENARIO: Standard Refill Verification**

SCENARIO ID: PHARM-001

**Script**

“May I confirm the patient name and date of birth?”

“Which medication are you verifying?”

**Action**

Check EMR → confirm or route.

# **SCENARIO: Early Refill Request**

SCENARIO ID: PHARM-002

**Script**

“Early refills require physician review. I’ll route this immediately.”

# **SCENARIO: Controlled Substance Request**

SCENARIO ID: PHARM-003

**Script**

“Controlled substances require direct physician approval.”

Immediate escalation.

# **SCENARIO: Dose Clarification**

SCENARIO ID: PHARM-004

**Script**

“I’ll confirm the dosage and return your call promptly.”

Create physician clarification task.

# **SCENARIO: Insurance Rejection (Pharmacy)**

SCENARIO ID: PHARM-005

**Script**

“Thank you for informing us. We’ll initiate the prior authorization process.”

Trigger PA Brain.

# **SCENARIO: Drug Interaction Inquiry**

SCENARIO ID: PHARM-006

**Script**

“I’ll notify the physician to review this interaction.”

Immediate clinical task.

# **SCENARIO: Missing Prescription**

SCENARIO ID: PHARM-007

**Script**

“I’ll verify whether it was transmitted and resend if necessary.”

Check EMR send status.

# **SCENARIO: DEA / Controlled Policy Discussion**

SCENARIO ID: PHARM-008

**Script**

“Controlled medication policies are determined by the prescribing physician.”

Route to MD if needed.

# **📞 01.3 INSURANCE COMPANY CALLS**

# **SCENARIO: Eligibility Verification (Insurance Rep)**

SCENARIO ID: INS-001

**Script**

“May I confirm which patient and date of service?”

Provide minimum necessary info.

# **SCENARIO: Prior Auth Follow-Up**

SCENARIO ID: INS-002

**Script**

“I’ll check the status and confirm whether additional documentation is needed.”

Route to PA Brain.

# **SCENARIO: Denial Explanation**

SCENARIO ID: INS-003

**Script**

“Thank you for explaining the denial. We will review and determine next steps.”

Log denial.

# **SCENARIO: Peer-to-Peer Request**

SCENARIO ID: INS-004

RISK: High

**Script**

“I’ll coordinate directly with the physician to schedule the peer-to-peer discussion.”

Escalate to physician immediately.

# **SCENARIO: Documentation Request**

SCENARIO ID: INS-005

**Script**

“Please send the request via secure fax or portal.”

Create documentation task.

# **📞 01.4 SPECIALIST / HOSPITAL CALLS**

# **SCENARIO: Discharge Follow-Up Coordination**

SCENARIO ID: HOSP-001

**Script**

“Thank you for the update. We’ll schedule a follow-up within the recommended timeframe.”

Create discharge follow-up task.

# **SCENARIO: Lab/Imaging Clarification (Hospital)**

SCENARIO ID: HOSP-002

**Script**

“I’ll confirm with the physician and return your call.”

Immediate clinical task.

# **SCENARIO: Referral Update**

SCENARIO ID: HOSP-003

**Script**

“Thank you. I’ll update the referral status in our system.”

Update referral tracker.

# **SCENARIO: Urgent Findings Notification**

SCENARIO ID: HOSP-004

RISK: Critical

**Script**

“Thank you for notifying us. I’m alerting the physician immediately.”

Immediate physician alert + patient contact.