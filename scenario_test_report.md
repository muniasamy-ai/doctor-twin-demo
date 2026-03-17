# Scenario Test Report

**Total Scenarios Tested:** 145
**Passed:** 70 / 145
**Failed:** 75
**Success Rate:** 48.28%

## Failed Scenarios

- **Scenario ID**: `SCH-URGENT-003`
  - **Input:** `Patient reports symptoms requiring same-day evaluation`
  - **Reason:** Expected ID 'SCH-URGENT-003', got 'REC-CALL-005'.

- **Scenario ID**: `SCH-PROC-005`
  - **Input:** `Patient scheduling procedures`
  - **Reason:** Expected ID 'SCH-PROC-005', got 'REC-CALL-001'.

- **Scenario ID**: `SCH-NOSHOW-008`
  - **Input:** `Patient did not arrive for scheduled appointment`
  - **Reason:** Expected ID 'SCH-NOSHOW-008', got 'ADMIN-CONFLICT-002'.

- **Scenario ID**: `SCH-WAITLIST-009`
  - **Input:** `Patient wants earlier appointment but schedule is full`
  - **Reason:** Expected ID 'SCH-WAITLIST-009', got 'SCH-NOSHOW-008'.

- **Scenario ID**: `RX-ROUTINE-001`
  - **Input:** `Chronic medication`
  - **Reason:** Expected ID 'RX-ROUTINE-001', got 'MSG-MED-001'.

- **Scenario ID**: `RX-LABS-002`
  - **Input:** `Labs required for medication monitoring`
  - **Reason:** Expected ID 'RX-LABS-002', got 'LAB-SCHED-006'.

- **Scenario ID**: `RX-VISIT-003`
  - **Input:** `Last visit >12 months`
  - **Reason:** Expected ID 'RX-VISIT-003', got 'MSG-MED-001'.

- **Scenario ID**: `RX-CONTROL-001`
  - **Input:** `I need my Xanax early`
  - **Reason:** Expected ID 'RX-CONTROL-001', got 'REC-RX-002'.

- **Scenario ID**: `RX-BRIDGE-005`
  - **Input:** `Patient out of medication`
  - **Reason:** Expected ID 'RX-BRIDGE-005', got 'REC-RX-003'.

- **Scenario ID**: `RX-DENY-006`
  - **Input:** `Medication inappropriate`
  - **Reason:** Expected ID 'RX-DENY-006', got 'MSG-MED-001'.

- **Scenario ID**: `REC-CALL-009`
  - **Input:** `Patient calls requesting prescription refill`
  - **Reason:** Expected ID 'REC-CALL-009', got 'REC-RX-003'.

- **Scenario ID**: `PA-001`
  - **Input:** `Pharmacy rejection`
  - **Reason:** Expected ID 'PA-001', got 'REC-BILL-001'.

- **Scenario ID**: `ADMIN-COMPLAINT-003`
  - **Input:** `long wait time`
  - **Reason:** Expected ID 'ADMIN-COMPLAINT-003', got 'ADMIN-DISSAT-004'.

- **Scenario ID**: `ADMIN-MEMBER-007`
  - **Input:** `wellness membership`
  - **Reason:** Expected ID 'ADMIN-MEMBER-007', got 'MSG-MED-001'.

- **Scenario ID**: `ADMIN-PRICE-006`
  - **Input:** `“How much does this visit cost?”`
  - **Reason:** Expected ID 'ADMIN-PRICE-006', got 'REC-BILL-001'.

- **Scenario ID**: `ADMIN-STAFF-001`
  - **Input:** `workflow breakdown`
  - **Reason:** Expected ID 'ADMIN-STAFF-001', got 'REC-CALL-001'.

- **Scenario ID**: `BACK-DOC-005`
  - **Input:** `unsigned note`
  - **Reason:** Expected ID 'BACK-DOC-005', got 'MSG-MED-001'.

- **Scenario ID**: `BACK-LAB-002`
  - **Input:** `abnormal lab value`
  - **Reason:** Expected ID 'BACK-LAB-002', got 'MA-LAB-001'.

- **Scenario ID**: `BACK-NURSE-007`
  - **Input:** `medication side effects`
  - **Reason:** Expected ID 'BACK-NURSE-007', got 'MA-RX-002'.

- **Scenario ID**: `BACK-PA-004`
  - **Input:** `CPT code`
  - **Reason:** Expected ID 'BACK-PA-004', got 'REC-BILL-001'.

- **Scenario ID**: `BACK-PHYS-008`
  - **Input:** `medication change request`
  - **Reason:** Expected ID 'BACK-PHYS-008', got 'MSG-MED-001'.

- **Scenario ID**: `BACK-REF-003`
  - **Input:** `referral specialty`
  - **Reason:** Expected ID 'BACK-REF-003', got 'REC-CALL-001'.

- **Scenario ID**: `BACK-SCHED-006`
  - **Input:** `multiple appointments`
  - **Reason:** Expected ID 'BACK-SCHED-006', got 'REC-CALL-001'.

- **Scenario ID**: `BACK-TASK-001`
  - **Input:** `physician instruction`
  - **Reason:** Expected ID 'BACK-TASK-001', got 'MSG-MED-001'.

- **Scenario ID**: `BILL-CPT-003`
  - **Input:** `“What is this CPT code?”`
  - **Reason:** Expected ID 'BILL-CPT-003', got 'MSG-MED-001'.

- **Scenario ID**: `BILL-DENIAL-004`
  - **Input:** `“Why did insurance deny this claim?”`
  - **Reason:** Expected ID 'BILL-DENIAL-004', got 'REC-BILL-001'.

- **Scenario ID**: `BILL-NS-001`
  - **Input:** `Missed appointment`
  - **Reason:** Expected ID 'BILL-NS-001', got 'SCH-NOSHOW-008'.

- **Scenario ID**: `BILL-PPLAN-005`
  - **Input:** `“I can’t pay the full amount right now.”`
  - **Reason:** Expected ID 'BILL-PPLAN-005', got 'REC-BILL-001'.

- **Scenario ID**: `BILL-REFUND-006`
  - **Input:** `“Why did I receive a refund?”`
  - **Reason:** Expected ID 'BILL-REFUND-006', got 'REC-CALL-001'.

- **Scenario ID**: `BILL-STMT-002`
  - **Input:** `“I received a bill and don’t understand it.”`
  - **Reason:** Expected ID 'BILL-STMT-002', got 'REC-BILL-001'.

- **Scenario ID**: `BILL-TECH-007`
  - **Input:** `Portal payment not working`
  - **Reason:** Expected ID 'BILL-TECH-007', got 'REC-BILL-001'.

- **Scenario ID**: `CLIN-CODE-003`
  - **Input:** `Encounter nearing completion`
  - **Reason:** Expected ID 'CLIN-CODE-003', got 'MSG-MED-001'.

- **Scenario ID**: `CLIN-EDU-007`
  - **Input:** `Doctor discussing diagnosis or treatment`
  - **Reason:** Expected ID 'CLIN-EDU-007', got 'MSG-MED-001'.

- **Scenario ID**: `CLIN-FOLLOW-006`
  - **Input:** `Visit nearing completion`
  - **Reason:** Expected ID 'CLIN-FOLLOW-006', got 'CLIN-AVS-009'.

- **Scenario ID**: `CLIN-MEDREC-005`
  - **Input:** `Visit begins or medications discussed`
  - **Reason:** Expected ID 'CLIN-MEDREC-005', got 'MSG-MED-001'.

- **Scenario ID**: `CLIN-ORDER-004`
  - **Input:** `Diagnosis or symptoms discussed during visit`
  - **Reason:** Expected ID 'CLIN-ORDER-004', got 'CLIN-AVS-009'.

- **Scenario ID**: `CLIN-PREVISIT-001`
  - **Input:** `Doctor opens patient chart`
  - **Reason:** Expected ID 'CLIN-PREVISIT-001', got 'MSG-MED-001'.

- **Scenario ID**: `CLIN-SOAP-002`
  - **Input:** `Doctor dictates or enters encounter notes`
  - **Reason:** Expected ID 'CLIN-SOAP-002', got 'ADMIN-COMPLAINT-003'.

- **Scenario ID**: `CLIN-STAFF-008`
  - **Input:** `Doctor requests staff assistance`
  - **Reason:** Expected ID 'CLIN-STAFF-008', got 'BACK-TASK-001'.

- **Scenario ID**: `DOC-FMLA-005`
  - **Input:** `Disability documentation`
  - **Reason:** Expected ID 'DOC-FMLA-005', got 'MSG-MED-001'.

- **Scenario ID**: `DOC-IMMUN-006`
  - **Input:** `School requirement`
  - **Reason:** Expected ID 'DOC-IMMUN-006', got 'REC-REC-001'.

- **Scenario ID**: `DOC-NOTE-004`
  - **Input:** `“I need a work excuse.”`
  - **Reason:** Expected ID 'DOC-NOTE-004', got 'REC-CALL-001'.

- **Scenario ID**: `DOC-PROVREC-002`
  - **Input:** `Hospital requests records`
  - **Reason:** Expected ID 'DOC-PROVREC-002', got 'DOC-PATREC-001'.

- **Scenario ID**: `DOC-ROI-003`
  - **Input:** `New physician`
  - **Reason:** Expected ID 'DOC-ROI-003', got 'SCH-NEWPT-001'.

- **Scenario ID**: `DOC-UPLOAD-007`
  - **Input:** `Outside lab results`
  - **Reason:** Expected ID 'DOC-UPLOAD-007', got 'REC-CALL-003'.

- **Scenario ID**: `IMG-FOLLOW-005`
  - **Input:** `Imaging complete`
  - **Reason:** Expected ID 'IMG-FOLLOW-005', got 'MSG-MED-001'.

- **Scenario ID**: `LAB-CRIT-003`
  - **Input:** `Lab flagged critical`
  - **Reason:** Expected ID 'LAB-CRIT-003', got 'MA-LAB-002'.

- **Scenario ID**: `LAB-LIFE-005`
  - **Input:** `Mild elevation cholesterol A1c liver enzymes`
  - **Reason:** Expected ID 'LAB-LIFE-005', got 'MA-LAB-001'.

- **Scenario ID**: `LANG-ARAB-002`
  - **Input:** `“هل تتكلم العربية؟”`
  - **Reason:** Expected ID 'LANG-ARAB-002', got 'LANG-SPAN-001'.

- **Scenario ID**: `LANG-CLARIFY-004`
  - **Input:** `unclear symptom description`
  - **Reason:** Expected ID 'LANG-CLARIFY-004', got 'MSG-MED-001'.

- **Scenario ID**: `LANG-INTERPRET-005`
  - **Input:** `diagnosis explanation`
  - **Reason:** Expected ID 'LANG-INTERPRET-005', got 'MSG-MED-001'.

- **Scenario ID**: `LANG-SWITCH-003`
  - **Input:** `conversation starts in English`
  - **Reason:** Expected ID 'LANG-SWITCH-003', got 'REC-CALL-001'.

- **Scenario ID**: `MA-INTAKE-001`
  - **Input:** `ma intake 001`
  - **Reason:** Expected ID 'MA-INTAKE-001', got 'MSG-MED-001'.

- **Scenario ID**: `MA-MEDREC-001`
  - **Input:** `Annual visit`
  - **Reason:** Expected ID 'MA-MEDREC-001', got 'SCH-FOLLOW-002'.

- **Scenario ID**: `MSG-ADMIN-006`
  - **Input:** `Work note`
  - **Reason:** Expected ID 'MSG-ADMIN-006', got 'MSG-MED-001'.

- **Scenario ID**: `MSG-FOLLOW-002`
  - **Input:** `I didn't understand the instructions`
  - **Reason:** Expected ID 'MSG-FOLLOW-002', got 'REC-CALL-001'.

- **Scenario ID**: `MSG-REF-005`
  - **Input:** `I need a referral`
  - **Reason:** Expected ID 'MSG-REF-005', got 'REC-CALL-001'.

- **Scenario ID**: `MSG-RESOLVE-008`
  - **Input:** `Issue completed`
  - **Reason:** Expected ID 'MSG-RESOLVE-008', got 'MSG-MED-001'.

- **Scenario ID**: `MSG-RX-004`
  - **Input:** `Did you send my refill`
  - **Reason:** Expected ID 'MSG-RX-004', got 'REC-RX-001'.

- **Scenario ID**: `MSG-TRIAGE-003`
  - **Input:** `I have chest pain`
  - **Reason:** Expected ID 'MSG-TRIAGE-003', got 'SAFE-CHEST-001'.

- **Scenario ID**: `PA-VISIT-001`
  - **Input:** `Visit completed`
  - **Reason:** Expected ID 'PA-VISIT-001', got 'CLIN-AVS-009'.

- **Scenario ID**: `PHARM-005`
  - **Input:** `PA Brain.`
  - **Reason:** Expected ID 'PHARM-005', got 'REC-CALL-001'.

- **Scenario ID**: `RX-DISC-009`
  - **Input:** `“I stopped taking it.”`
  - **Reason:** Expected ID 'RX-DISC-009', got 'MSG-MED-001'.

- **Scenario ID**: `RX-ESC-007`
  - **Input:** `Multiple medications`
  - **Reason:** Expected ID 'RX-ESC-007', got 'MSG-MED-001'.

- **Scenario ID**: `RX-LABS-001`
  - **Input:** `Send 30–90 day refill`
  - **Reason:** Expected ID 'RX-LABS-001', got 'RX-ROUTINE-001'.

- **Scenario ID**: `SAFE-911-008`
  - **Input:** `severe breathing difficulty`
  - **Reason:** Expected ID 'SAFE-911-008', got 'MSG-MED-001'.

- **Scenario ID**: `SAFE-AFTERHOURS-007`
  - **Input:** `route to on-call physician if applicable`
  - **Reason:** Expected ID 'SAFE-AFTERHOURS-007', got 'REC-CALL-001'.

- **Scenario ID**: `SAFE-ALLERGY-003`
  - **Input:** `throat swelling`
  - **Reason:** Expected ID 'SAFE-ALLERGY-003', got 'REC-SYMPTOM-001'.

- **Scenario ID**: `SAFE-LABCRIT-006`
  - **Input:** `dangerously high potassium`
  - **Reason:** Expected ID 'SAFE-LABCRIT-006', got 'LAB-CRIT-003'.

- **Scenario ID**: `SPA-BEFOREAFTER-005`
  - **Input:** `“Can I see before and after results?”`
  - **Reason:** Expected ID 'SPA-BEFOREAFTER-005', got 'MSG-MED-001'.

- **Scenario ID**: `SPA-BOOK-007`
  - **Input:** `facial treatment`
  - **Reason:** Expected ID 'SPA-BOOK-007', got 'REC-CALL-001'.

- **Scenario ID**: `SPA-IV-003`
  - **Input:** `hydration therapy`
  - **Reason:** Expected ID 'SPA-IV-003', got 'MSG-MED-001'.

- **Scenario ID**: `SPA-MEMBER-004`
  - **Input:** `“Do you have membership plans?”`
  - **Reason:** Expected ID 'SPA-MEMBER-004', got 'REC-CALL-001'.

- **Scenario ID**: `SPA-PACKAGE-006`
  - **Input:** `“How much does a package cost?”`
  - **Reason:** Expected ID 'SPA-PACKAGE-006', got 'ADMIN-PRICE-006'.

- **Scenario ID**: `SPA-RECOMMEND-002`
  - **Input:** `“What treatment should I get?”`
  - **Reason:** Expected ID 'SPA-RECOMMEND-002', got 'MSG-MED-001'.
