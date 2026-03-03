# Gold Audit Log Spec — Personal AI Employee

## File
- canonical: AI_Employee_Vault/Logs/gold_action_log.jsonl
- evidence snapshots only: evidence/gold/** (committed)

## Format
- JSON Lines (one JSON object per line)
- Append-only (never rewrite history)
- No secrets (no tokens, passwords, API keys)

## Required Fields (minimum)
- ts (ISO 8601 with timezone)
- event (string)
- status (string: attempt|success|fail|idle)
- actor (string)

## Optional Fields (recommended)
- task_id / request_path / approved_path
- mode
- output_path(s)
- error (safe message only)

## Acceptance Criteria
- File exists and contains multiple real events across phases
- Every line is valid JSON
- Every line contains required fields
- Evidence includes:
  - snapshot of JSONL (small tail)
  - validator output showing PASS
