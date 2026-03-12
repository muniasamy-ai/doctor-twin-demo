# 📋 07. MEDICAL RECORDS & DOCUMENTATION SCENARIOS

# 07.1 Records Request from Patient
SCENARIO ID: DOC-PATREC-001
BRAIN: Records Assistant
CHANNEL: Portal / Phone / In-person
INTENT: Patient requesting their own medical records
RISK: Moderate (HIPAA controlled)
REQUIRES CONFIRMATION: Identity verification
SUCCESS: Secure records delivery
Trigger
Patient states:
- “I need a copy of my medical records.”
- “Can you send me my chart?”
- “I want my lab results and notes.”
Identity Verification
Confirm:
- Full name
- Date of birth
- Address or phone number
- Patient portal identity if digital request
Script
“I can help you obtain a copy of your medical records.”
“For security purposes, we’ll need to verify your identity and confirm how you would like to receive the records.”
Delivery Options
- Secure portal download
- Encrypted email
- Printed copy
- Secure transfer to another provider
Actions
- Verify patient identity
- Generate records export
- Send secure delivery
- Log records release
# 07.2 Records Request from Outside Provider
SCENARIO ID: DOC-PROVREC-002
RISK: Moderate–High
Trigger
- Hospital requests records
- Specialist requests chart
- Transfer of care
Required Verification
Confirm:
- Requesting provider identity
- Medical facility
- Authorization on file
Script
“Thank you for your request. We will process the records once a valid authorization form is received.”
Required Document
HIPAA Release of Information (ROI) authorization.
Actions
- Verify provider credentials
- Confirm patient authorization
- Send records securely
- Log transfer
# 07.3 Release of Information Workflow
SCENARIO ID: DOC-ROI-003
Trigger
Patient requests records sent to another party.
Examples:
- New physician
- Legal representative
- Insurance company
Script
“To release your records, we need a signed authorization form specifying the recipient.”
Required Elements
ROI form must include:
- Patient name
- DOB
- Recipient organization
- Specific records requested
- Patient signature
- Date
Actions
- Provide ROI form
- Verify signature
- Process release
- Document disclosure
# 07.4 School / Work Note Request
SCENARIO ID: DOC-NOTE-004
RISK: Low
Trigger
Patient states:
- “I need a work excuse.”
- “My child needs a school note.”
Script
“I can prepare a medical note confirming your visit.”
Note may include:
- Visit date
- Return-to-work/school recommendation
Restrictions
Notes must not disclose diagnoses unless patient authorizes.
Actions
- Generate note template
- Physician review if required
- Deliver via portal
# 07.5 Disability / FMLA Form Request
SCENARIO ID: DOC-FMLA-005
RISK: Moderate
Trigger
Patient requests:
- Disability documentation
- FMLA paperwork
- Work limitation forms
Script
“These forms typically require physician review. Please upload the paperwork through the secure portal.”
Required Data
- Employer form
- Patient signature section completed
- Supporting medical information
Actions
- Upload form to chart
- Assign to physician task queue
- Track completion timeline
- Notify patient when ready
# 07.6 Immunization Record Export
SCENARIO ID: DOC-IMMUN-006
RISK: Low
Trigger
Patient requests vaccination history.
Examples:
- School requirement
- Travel requirement
- Employment verification
Script
“I can provide a copy of your immunization record.”
“You’ll receive a downloadable document through the patient portal.”
Actions
- Retrieve vaccine history
- Generate standardized immunization report
- Send secure file
# 07.7 Document Upload Handling
SCENARIO ID: DOC-UPLOAD-007
RISK: Low–Moderate
Trigger
Patient uploads documents:
- Outside lab results
- Imaging reports
- Insurance cards
- Referral letters
Script
“Your document has been received and added to your medical record.”
“If physician review is required, we will notify you.”
Processing Steps
Classify uploaded document:
- Lab result
- Imaging report
- Insurance document
- Other clinical records
Actions
- Store document in patient chart
- Tag document type
- Notify physician if clinical relevance detected
# ENGINEERING RULES FOR RECORDS MODULE
The system must enforce:
1️⃣ Identity Verification
No record release without patient verification.
2️⃣ Authorization Validation
Records to third parties require:
- Signed authorization
- Recipient details
- Specific records listed
3️⃣ Secure Delivery Methods
Allowed:
- Patient portal
- Encrypted email
- Secure provider exchange
Not allowed:
- Unencrypted email
- SMS file transfer
4️⃣ Audit Logging
Every release must log:
- Requestor identity
- Authorization type
- Records released
- Timestamp