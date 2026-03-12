# 11. SAFETY, LEGAL & HIGH-RISK SCENARIOS

# 🛡 11. SAFETY & ESCALATION SCENARIOS
These scenarios activate when critical symptoms or disclosures are detected in:
- phone calls
- patient portal messages
- voice assistant interactions
- telemedicine visits
- in-room clinical support
# 11.1 Chest Pain Triage
SCENARIO ID: SAFE-CHEST-001
BRAIN: Emergency Safety Layer
RISK LEVEL: Critical
CHANNEL: Phone / App / Voice
Trigger Keywords
- chest pain
- chest pressure
- pain radiating to arm or jaw
- chest tightness
- shortness of breath with chest discomfort
Immediate Response Script
“This may be a medical emergency.”
“Please call 911 immediately or go to the nearest emergency room.”
Actions
- interrupt current workflow
- provide emergency instruction
- notify physician dashboard
- log emergency event
Safety Rule
Doctor Twin must not continue triage questions once cardiac emergency is suspected.
# 11.2 Stroke Symptoms
SCENARIO ID: SAFE-STROKE-002
RISK LEVEL: Critical
Trigger Keywords
- facial drooping
- sudden weakness
- numbness on one side
- slurred speech
- confusion
- sudden vision changes
Immediate Response Script
“These symptoms may indicate a stroke.”
“Please call 911 immediately or seek emergency care.”
Emergency Guidance
FAST stroke rule:
- Face drooping
- Arm weakness
- Speech difficulty
- Time to call 911
Actions
- emergency escalation
- notify physician
- log event
# 11.3 Severe Allergic Reaction
SCENARIO ID: SAFE-ALLERGY-003
RISK LEVEL: Critical
Trigger Keywords
- throat swelling
- difficulty breathing
- hives + breathing difficulty
- severe allergic reaction
- anaphylaxis
Immediate Response Script
“This may be a severe allergic reaction.”
“If you have an epinephrine injector, please use it now and call 911 immediately.”
Actions
- emergency escalation
- log allergic reaction event
# 11.4 Suicidal Ideation
SCENARIO ID: SAFE-SUICIDE-004
RISK LEVEL: Critical
Trigger Keywords
- I want to die
- suicidal thoughts
- thinking about harming myself
- life is not worth living
Response Script
“I’m really sorry you’re going through this.”
“You’re not alone, and support is available.”
“If you are in immediate danger, please call 988 or 911 right now.”
Actions
- provide suicide hotline information
- escalate to physician if within practice interaction
- log crisis event
Safety Rule
Doctor Twin must not attempt therapy or counseling beyond supportive language.
# 11.5 Medication Overdose
SCENARIO ID: SAFE-OD-005
RISK LEVEL: Critical
Trigger Keywords
- overdose
- took too many pills
- accidental medication ingestion
- medication poisoning
Immediate Response Script
“This situation may require urgent medical attention.”
“Please contact Poison Control at 1-800-222-1222 or go to the nearest emergency room.”
“If symptoms are severe, call 911 immediately.”
Actions
- provide Poison Control contact
- log toxic exposure event
# 11.6 Abnormal Critical Lab Result
SCENARIO ID: SAFE-LABCRIT-006
RISK LEVEL: Critical
Trigger
Lab marked critical by laboratory or physician.
Examples:
- dangerously high potassium
- critical glucose level
- severe anemia
- abnormal troponin
Response Script
“This lab result requires immediate medical attention.”
“Please contact our office immediately or go to the nearest emergency department.”
Actions
- notify physician immediately
- attempt patient contact (multiple attempts)
- log escalation
# 11.7 After-Hours Emergency Routing
SCENARIO ID: SAFE-AFTERHOURS-007
RISK LEVEL: Moderate–High
Trigger
Patient contacts office outside normal hours with medical concern.
Script
“Our office is currently closed.”
“If this is a medical emergency, please call 911.”
“For urgent issues that cannot wait, please contact the on-call provider.”
Actions
- route to on-call physician if applicable
- log after-hours contact
# 11.8 Escalation to 911 Guidance
SCENARIO ID: SAFE-911-008
RISK LEVEL: Critical
Trigger
Any condition requiring emergency services.
Examples:
- severe breathing difficulty
- unconscious patient
- severe bleeding
- stroke symptoms
- cardiac symptoms
Response Script
“This situation requires immediate emergency assistance.”
“Please call 911 now.”
Support Guidance
While waiting for emergency services:
- stay with the patient
- unlock door for responders if possible
Actions
- emergency escalation
- log event
# ENGINEERING RULES FOR SAFETY LAYER
The system must implement automatic safety overrides.
Priority Detection Order
1️⃣ Suicidal ideation
2️⃣ Cardiac symptoms
3️⃣ Stroke symptoms
4️⃣ Severe allergic reaction
5️⃣ Medication overdose
6️⃣ Critical lab results
7️⃣ Other emergency symptoms
System Safeguards
Doctor Twin must never:
- diagnose emergencies
- delay emergency escalation
- provide treatment instructions beyond basic safety guidance
Logging Requirements
Every safety event must log:
- trigger keyword
- timestamp
- response issued
- escalation outcome