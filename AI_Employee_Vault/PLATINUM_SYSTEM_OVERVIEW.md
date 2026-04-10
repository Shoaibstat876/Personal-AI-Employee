# Platinum System Overview

## Purpose
This document defines runtime ownership, system boundaries, and visibility for the Platinum layer.

The core execution system (Gold) is already complete and unchanged.  
This layer adds **observability, coordination, and clarity only**, as defined in the `.specify` governance layer.

---

## Cloud Responsibilities
- Draft creation  
- Update generation  
- Writing into /Updates/Incoming/  

Cloud operates in a **strict draft-only role**.

Cloud NEVER:
- executes actions  
- modifies system state directly  
- bypasses HITL  

---

## Local Responsibilities
- Claim updates (claim-by-move)  
- Perform HITL review  
- Process updates  
- Create Gold bridge artifacts  
- Execute via MCP (only after approval)  
- Maintain Dashboard  

Local is the **single execution authority** in the system.

---

## Core Rules

### Single-Writer Dashboard
Dashboard is **LOCAL ONLY**.  
No cloud-side modification is allowed.

---

### Cloud Never Executes
Cloud produces **non-executable drafts only**.

---

### Local Always Approves
All execution is controlled via **Human-In-The-Loop (HITL)**.

No approval → No execution  

---

### Determinism
Platinum introduces **zero changes** to:

- Gold scripts  
- HITL flow  
- MCP integrations  
- Execution logic  

System behavior remains **fully deterministic and reproducible**.

---

## Lifecycle

Incoming → Claimed → Processed → Bridged → Gold → Done  

This lifecycle reflects a **governed, state-driven workflow** where:

- ownership is explicit  
- transitions are traceable  
- execution occurs only in Gold  

---

## Identity Model

source: cloud_draft  
claimed_by: local_system  
processed_by: local_system  

This ensures:

- clear ownership  
- no ambiguity  
- full traceability  

---

## Execution Boundary (CRITICAL)

- Platinum layer = **non-executing observability layer**  
- Gold layer = **only execution layer**  

At no point can:

- Cloud trigger execution  
- Updates bypass approval  
- Platinum modify execution logic  

👉 This enforces strict system safety and control.

---

## Demo Value
- Clear system ownership  
- Clear lifecycle tracking  
- Production-grade visibility  
- Judge-friendly architecture clarity  

---

## Safety
- Additive only  
- Reversible  
- Non-executing  
- Fully deterministic  

---

## Governance Alignment

This layer is fully aligned with `.specify`, including:

- workflow lifecycle definition  
- HITL governance rules  
- execution boundaries  
- traceability model  

Important:

- Platinum does NOT alter Gold behavior  
- Platinum does NOT introduce autonomy  
- Platinum only improves system visibility and coordination  

---

## Final Guarantee

The system ensures:

- No hidden execution  
- No cloud-side control  
- No approval bypass  
- Full lifecycle traceability  

👉 Platinum explains and tracks  
👉 Gold executes safely