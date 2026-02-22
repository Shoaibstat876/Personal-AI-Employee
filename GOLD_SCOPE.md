# GOLD_SCOPE

## What Gold includes (THIS repo state)
Gold is a **safety-first orchestration tier**.

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

## Freeze markers
Tags are the canonical freeze checkpoints:
- `gold-v1` — core Gold loop forensics improvement
- `gold-v1.1` — repo hygiene evidence ignore
- `gold-v1.2` — vault operational folders ignore

Further tags may be added for documentation completion and retry logic proof.

