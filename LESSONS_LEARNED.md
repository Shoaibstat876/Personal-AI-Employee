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

---

## 7) Execution requires strict control, not autonomy

Initial Gold design avoided all execution for safety.

However, a complete system requires:
- real-world interaction
- business system integration
- communication capability

The solution is **HITL-controlled execution**, not autonomy.

---

## 8) MCP is access, not execution

MCP servers provide:
- tools
- connectivity

But they do NOT perform actions by themselves.

Execution requires:
- dedicated execution bridges
- explicit scripts
- controlled invocation after approval

---

## 9) Artifact-driven execution ensures auditability

Every action follows:

Approval → Action Artifact → Execution → Log

This ensures:
- traceability
- reproducibility
- verifiable proof

Artifacts act as the contract between planning and execution.

---

## 10) Idempotency is critical for real systems

Without idempotency:
- duplicate customers (Odoo)
- repeated messages (Slack)
- repeated emails

Solution:
- check before execution
- mark artifact as executed
- prevent re-run

---

## 11) Logs are proof, not just debugging

Logs serve three purposes:
- debugging
- auditing
- judge verification

Structured logs (JSONL) make the system:
- inspectable
- verifiable
- reliable

---

## 12) Final system evolution

System progression:

Stage 1 → File-based task system  
Stage 2 → Deterministic orchestration  
Stage 3 → HITL approval layer  
Stage 4 → Controlled execution (Gold completion)

---

## Final insight

The system becomes a **true AI employee** only when it can:

- plan work  
- request approval  
- execute real actions  
- maintain full audit trace  

Gold Tier represents the transition from:

Safe system → Useful system → **Operational system**