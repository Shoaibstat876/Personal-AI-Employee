# ARCHITECTURE

## What this project is
**Personal AI Employee (Hackathon 0)** is a local-first, file-driven agent system using an Obsidian vault as the control surface.

This repository currently focuses on **Gold Tier orchestration safety**:
- deterministic scan/claim/move loop
- stop-hook checkpoints (manual kill switch)
- resume-safe behavior (no guessing)
- forensic state tracking (run_id + inflight_* pointers)
- human-in-the-loop (HITL) approval artifacts
- audit logs (append-only)

## Core components

### Vault (AI_Employee_Vault)
Primary folders used by the orchestration pattern:

- `Needs_Action/` — incoming actionable files
- `In_Progress/gold/` — claimed work owned by the Gold loop (claim-by-move)
- `Done/` — completed items

Supporting folders for Gold foundation contracts:
- `Pending_Approval/` — approval requests created by the system
- `Approved/` — approvals moved here by human
- `Rejected/` — rejected approvals
- `Plans/` — planning artifacts (optional)
- `Briefings/` — CEO briefings
- `Logs/` — local logs and action logs

> Note: Operational vault folders are ignored by git for repo hygiene.

### Gold loop
`watchers/gold_loop.py` implements a single-cycle orchestrator:

**Cycle phases**
1. SCAN: list tasks in `Needs_Action`
2. CLAIM: acquire lock for a chosen task (idempotent lock file)
3. MOVE: move claimed task into `In_Progress/gold`
4. IDLE: explicitly log that no external execution occurs

**Guarantees**
- Deterministic behavior (no hidden side effects)
- Manual stoppability via STOP file checkpoints
- Resume-safe behavior using runtime state + safe exits
- Forensic continuity by persisting real lock path after claim

### Runtime state + logs
- `AI_Employee_Vault/Logs/gold_runtime_state.json` — single JSON state snapshot (updated each run)
- `AI_Employee_Vault/Logs/gold_loop.log.md` — append-only cycle events
- `AI_Employee_Vault/Logs/action_log_YYYY-MM-DD.jsonl` — append-only structured audit events (JSONL)

## Security posture (Gold)
- No uncontrolled background execution
- Watchers disabled during proof/freeze checkpoints
- HITL required for sensitive actions (approval file flow)
- Platinum autonomy is NOT enabled

---

## HITL Execution Layer (Gold Completion Upgrade)

The system has been extended beyond orchestration safety to include **real-world execution under Human-In-The-Loop (HITL) control**.

This introduces a controlled action pipeline:

Approval → Action Artifact → Execution Bridge → External System → Log

---

## Execution bridges (implemented)

### Email execution bridge
- Source: approval → email action artifact
- Execution: Python script using Resend API
- Result: real email delivered to external inbox
- Logging: execution output + audit trace

### Odoo execution bridge
- Source: approval → Odoo action artifact
- Execution: Python JSON-RPC client
- Action: customer creation (`res.partner`)
- Result: real customer created in Odoo database
- Safety:
  - idempotency guard (no duplicate customers)
  - approval required before execution
- Logging:
  - `Logs/odoo_execution_log.jsonl`

### Slack execution bridge
- Source: approval → Slack action artifact
- Execution: Python Slack API client
- Action: message sent to Slack channel
- Result: real message delivered with timestamp
- Safety:
  - channel validation
  - idempotency guard
- Logging:
  - `Logs/slack_execution_log.jsonl`

---

## Execution guarantees

- No external action occurs without approval
- All executions originate from artifacts
- Each execution is:
  - traceable
  - logged
  - reproducible
- Duplicate execution is prevented (idempotency)

---

## Extended audit system

In addition to orchestration logs:

- Odoo execution logs (JSONL)
- Slack execution logs (JSONL)
- Email execution outputs

Each record includes:
- timestamp
- event type
- artifact reference
- execution result

---

## Architecture evolution

System progression:

1. File-based task system  
2. Deterministic orchestration loop  
3. HITL approval layer  
4. **Execution bridges (Gold completion)**  

This final step transforms the system from:

Passive agent → Controlled executor → **Digital employee capable of real actions**

---

## Final note

Gold Tier is achieved when the system can:

- safely request approval  
- execute real actions  
- maintain full audit trace  

This repository satisfies all three.
