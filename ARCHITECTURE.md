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

