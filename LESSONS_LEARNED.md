# LESSONS_LEARNED

## 1) Determinism beats “cleverness”
The safest automation is the one that is repeatable:
- scan is read-only
- claim uses a lock (idempotent)
- move establishes ownership (single-writer)

## 2) Stop hooks must exist at multiple checkpoints
A single “stop at start” is not enough.
Gold requires STOP checks at:
START, AFTER_SCAN, BEFORE_CLAIM, BEFORE_LOCK, BEFORE_MOVE

This ensures a human can halt the loop even mid-cycle.

## 3) Resume safety must never guess
If a prior run was interrupted:
- detect `inflight_*`
- verify the referenced task is actually in `In_Progress/gold`
- otherwise exit safely and log why

This prevents “zombie resumes”.

## 4) Forensics need real identifiers
Logs alone are not enough.
Persisting the **real lock path** in runtime state provides a stronger chain of evidence if STOP occurs after claim.

## 5) Evidence packs should not pollute git history
Local proof artifacts belong in local evidence folders and should be ignored by git.
Tags are the canonical freeze points for judge-safe verification.

## 6) “No execution” must be explicit
Gold must state clearly in logs that it does not execute external actions:
`CYCLE_IDLE: no execution`

This prevents accidental Platinum escalation.

