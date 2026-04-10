# Platinum Cloud / Local Rules

## Core Rule
Platinum prepares → Gold executes

This rule enforces strict separation between **draft generation (Platinum)** and **controlled execution (Gold)**, as defined in the `.specify` governance layer.

---

## Folder Used
AI_Employee_Vault/Updates/

- Incoming = new drafts from cloud
- Claimed = local is reviewing
- Processed = review finished

These folders implement an **asynchronous, claim-based workflow**, ensuring clear ownership and no concurrent execution conflicts.

---

## Flow

Cloud → Updates/Incoming → Local Claim → Review → Processed → Gold System

This flow reflects the governed lifecycle defined in `.specify`, where:

- Cloud produces non-executable drafts  
- Local system assumes ownership via claim  
- Gold system executes only after approval  

---

## Important Rules

1. Nothing executes from Updates  
2. Local must move file before working (Claim-by-Move)  
3. Only Local can approve and execute  
4. Gold system is still main execution system  

These rules enforce:

- execution boundary control  
- human-in-the-loop (HITL) governance  
- single-writer system ownership  

---

## Execution Boundary (CRITICAL)

- Updates folder = **non-executable layer**  
- Gold system = **only execution layer**  

At no point can:

- Cloud trigger execution  
- Updates bypass approval  
- Drafts directly perform actions  

👉 This guarantees zero autonomous behavior.

---

## Meaning

Cloud only suggests work  
Local decides  
Gold executes safely  

This ensures the system remains:

- controlled  
- auditable  
- deterministic  

---

## Governance Alignment

This rule set is formally aligned with `.specify`, including:

- workflow lifecycle definition  
- HITL enforcement rules  
- execution boundaries  
- traceability model  

Important:

- Platinum does NOT modify Gold logic  
- Platinum does NOT execute actions  
- Platinum only improves visibility and coordination  

---

## Final Guarantee

This architecture ensures:

- No hidden execution  
- No cloud-side control  
- No bypass of human approval  
- Full traceability across all layers  

👉 Platinum enhances clarity  
👉 Gold guarantees safe execution