# GOLD LOOP CONTRACT v1 (PLANNING ONLY — FROZEN AFTER APPROVAL)

## 0) Tier Boundaries
- Bronze: frozen (bronze-v1)
- Silver: frozen (silver-v1)
- Gold: controlled loop only
- Platinum: LOCKED

## 1) Loop Safety Contract (MANDATORY)
MAX_ITERATIONS = 25
MAX_RUNTIME_SECONDS = 300
STOP_CONDITION = (no eligible tasks found for 3 consecutive scans) OR (manual stop triggered)
FAILURE_EXIT = abort loop immediately, log FAILURE_REASON, exit non-zero
MANUAL_KILL_SWITCH = create file AI_Employee_Vault/STOP

## 2) Ralph Wiggum Stop Hook (Hard Abort)
Stop triggers (ANY true):
- File exists: AI_Employee_Vault/STOP (or STOP.md)
- runtime_flags.json: { "stop": true }
- STOP_REASON.md non-empty

On stop:
- Finish current atomic step only
- Log STOP_REASON + timestamp + task_id (if any)
- Exit cleanly (code 0)

## 3) Completion Promise (Exactly-Once)
Canonical completion marker:
- AI_Employee_Vault/Done/<task_id>.done.json

Rules:
- If done.json exists → never execute again
- If done.json exists but approval missing → STOP + log INCONSISTENT_STATE

## 4) Resume / Crash Safety (Deterministic)
Runtime state file:
- AI_Employee_Vault/Logs/gold_runtime_state.json

On startup:
- If inflight_task_id exists:
  - If done.json exists → clear inflight and continue
  - Else resume from inflight_step (no re-running unsafe steps)

## 5) Idempotency Gates
- Deterministic scan order: lexicographic by task_id
- Claim creates lock file (exclusive create)
- Right-before-execution gate: approval exists + hash matches + done.json absent
- After execution: write done.json (then any moves)

## 6) Logging Discipline (MANDATORY)
Log file (append-only):
- AI_Employee_Vault/Logs/gold_loop.log.md

Log events:
START, EACH ITERATION (#), STOP_REASON, FAILURE_REASON, TOTAL_RUNTIME, TOTAL_ITERATIONS

## 7) External Mutation Guard (MANDATORY)
- No MCP calls.
- No external APIs.
- No network mutation.
- No writes outside AI_Employee_Vault boundary.
Exception ONLY if:
- Explicit approval file exists
- Human execution flag is present
- Action is logged
- Scope is read-only OR mutation contract is defined
Otherwise: ABORT.

## 8) Failure Exit Rules (MANDATORY)
FAILURE_EXIT behavior:
- Write FAILURE_REASON with timestamp + inflight_task_id (if any)
- Exit with non-zero code
- Do NOT create done.json on failure
- Preserve evidence (logs/state) for audit
