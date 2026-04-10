# GOLD_SCOPE

## What Gold includes (THIS repo state)
Gold is a **safety-first orchestration tier**.

The scope defined here aligns with the governed system behavior formalized in the `.specify` layer, including workflow control, HITL governance, execution boundaries, and evidence traceability.

✅ Included:
- Deterministic scan/claim/move loop (`watchers/gold_loop.py`)
- STOP hook checkpoints: START, AFTER_SCAN, BEFORE_CLAIM, BEFORE_LOCK, BEFORE_MOVE
- Resume-safe behavior:
  - Detect prior inflight state
  - If the referenced task is not in `In_Progress/gold`, exit safely (no guessing)
- Forensic state continuity:
  - persist `inflight_task_id`, `inflight_step`, and **real lock path** (`inflight_lock_id`)
- Human-in-the-loop folder contracts:
  - `Pending_Approval/`, `Approved/`, `Rejected/`
- Audit logging:
  - append-only `action_log_YYYY-MM-DD.jsonl`
  - schema document in `AI_Employee_Vault/Logs/AUDIT_LOG_SCHEMA.md`
- Weekly CEO briefing generator:
  - `scripts/generate_ceo_briefing.py` (local-only inputs)
  - outputs to `AI_Employee_Vault/Briefings/`

## What Gold explicitly does NOT include
❌ Not included (Platinum or out-of-scope):
- Autonomous external actions (email send, payments, social posting)
- Always-on cloud deployment
- Multi-agent delegation
- Banking integration, WhatsApp automation, social media automation
- Odoo integration
- Background watchdog/process manager

These exclusions reflect the execution boundaries defined in `.specify`.

## Freeze markers
Tags are the canonical freeze checkpoints:
- `gold-v1` — core Gold loop forensics improvement
- `gold-v1.1` — repo hygiene evidence ignore
- `gold-v1.2` — vault operational folders ignore

Further tags may be added for documentation completion and retry logic proof.

---

## Gold Completion Upgrade (Execution Layer Added)

The system has been extended beyond orchestration safety to include **controlled real-world execution under HITL**.

This does NOT introduce autonomy.  
All actions remain strictly approval-driven.

This extension remains consistent with the `.specify` execution boundary and HITL governance rules.

---

## Newly included in Gold (final state)

### HITL-controlled execution systems

#### Email (Resend)
- Draft → Approval → Send
- Real email delivery confirmed
- Execution recorded via logs/output

#### Odoo (Business system)
- Action: customer creation
- Triggered only after approval
- Uses JSON-RPC API
- Safety:
  - idempotency guard (no duplicate records)
- Logs:
  - `Logs/odoo_execution_log.jsonl`

#### Slack (Communication system)
- Action: message send
- Triggered only after approval
- Uses Slack API
- Safety:
  - channel validation
  - idempotency guard
- Logs:
  - `Logs/slack_execution_log.jsonl`

---

## Execution model (Gold)

Approval → Action Artifact → Execution Bridge → External System → Log

Properties:
- No execution without approval
- All executions are artifact-driven
- All actions are logged and traceable
- Duplicate execution prevented

This model directly reflects the workflow and execution constraints defined in `.specify`.

---

## Updated scope clarification

Gold **now includes**:

- Controlled external execution (HITL only)
- Business system interaction (Odoo)
- Communication systems (Email, Slack)
- Execution bridges with logging

Gold still **does NOT include**:

- Autonomous execution (no approval)
- Always-on cloud runtime
- Multi-agent systems
- Financial/banking automation

---

## Final scope statement

Gold Tier is achieved when the system:

- Plans tasks
- Requests approval
- Executes real-world actions safely
- Maintains full audit logs

This repository now satisfies all Gold requirements.

All guarantees and boundaries described here are consistent with the `.specify` governance layer and backed by real system behavior.