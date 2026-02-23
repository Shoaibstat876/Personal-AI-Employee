# Personal AI Employee — Hackathon 0 (Silver + Gold)

**Tagline:** Local-first, agent-driven, human-in-the-loop Digital FTE.

---

## Tier Status

- **Silver:** Watchers + Scheduling + Dedup + HITL artifacts ✅
- **Gold:** Deterministic orchestration + STOP checkpoints + resume safety + audit logs + CEO briefing ✅

---

## Silver Tier (Perception Layer)

# Personal AI Employee â€” Hackathon 0 (Silver Tier)

**Tagline:** Your life and business on autopilot â€” local-first, agent-driven, human-in-the-loop.

This repository implements a **Silver-tier** â€œDigital FTEâ€ architecture using:
- **Obsidian vault (local markdown)** as memory/dashboard
- **Watchers (Python)** as Perception layer
- **Human-in-the-loop approval workflow**
- **Windows Task Scheduler** for background-safe execution

---

## âœ… Tier Declaration
**Target Tier:** Silver  
**Status:** Complete (Perception + Scheduling + Dedup + Logs + HITL workflow)

---

## Architecture (Perception â†’ Reasoning â†’ Action)

### 1) Memory / GUI: Obsidian Vault
Vault: `AI_Employee_Vault/`

Core folders:
- `Inbox/`
- `Needs_Action/`
- `Plans/`
- `In_Progress/`
- `Pending_Approval/`
- `Approved/`
- `Rejected/`
- `Done/`
- `Logs/`
- `Decisions/`

### 2) Perception Layer (Silver)
Two background-safe watchers:

#### A) Filesystem Watcher (dropbox â†’ Needs_Action)
- Watches: `dropbox/`
- Archives into: `dropbox/_processed/`
- Writes tasks into: `AI_Employee_Vault/Needs_Action/`
- Logs to: `AI_Employee_Vault/Logs/watcher_filesystem_log.md`
- Dedup state: `AI_Employee_Vault/Logs/filesystem_watcher_state.json`

#### B) Vault Health Watcher (contract enforcement)
- Verifies required vault folders exist
- Logs to: `AI_Employee_Vault/Logs/watcher_vault_health_log.md`
- If folders are missing, creates a Needs_Action task requesting manual repair

### 3) Dedup Contract (Silver requirement)
Decision doc:
`AI_Employee_Vault/Decisions/FILESYSTEM_WATCHER_DEDUP_CONTRACT.md`

Rule:
- Dedup key = `SHA256(file_bytes)`
- If the content hash already exists â†’ archive file and log `DEDUP_SKIP` (NO new task)

### 4) Human-in-the-loop approvals
Approval artifacts live in `AI_Employee_Vault/Approved/` and can be:
- `status: approved` + `executed: false` â†’ eligible for execution
- `executed: true` â†’ completed
- `status: revoked` â†’ permanently skipped

### 5) Scheduling (Silver requirement)
Watchers run on login via Windows Task Scheduler:
- `PersonalAIEmployee_Watcher_Filesystem`
- `PersonalAIEmployee_Watcher_VaultHealth`

Wrapper CMDs avoid space-path issues:
- `D:\PAIE_RUN\fs.cmd`
- `D:\PAIE_RUN\vh.cmd`

---

## Quick Start (Windows)

### Prereqs
- Python 3.12+ installed at `C:\Python312\python.exe`
- `pip install watchdog`

### Run watchers manually (foreground)
```powershell
cd "D:\Shoaib Project\Personal-AI-Employee"
py .\watchers\filesystem_watcher.py
py .\watchers\vault_health_watcher.py



---

## Gold Tier (Orchestration + Audit)

# Personal AI Employee â€” Hackathon 0 (Gold Tier)

**Tagline:** Local-first, agent-driven, human-in-the-loop Digital FTE.

---

## 1. Overview

This repository implements a **Gold-tier Personal AI Employee** based on a deterministic, local-first architecture.

The system is designed around:

- File-driven orchestration
- Deterministic task ownership
- Human-in-the-loop (HITL) safeguards
- Structured audit logging
- Resume-safe crash handling
- Weekly CEO briefing automation

The implementation prioritizes safety, reproducibility, and clear tier boundaries.

---

## 2. Tier Declaration

**Target Tier:** Gold  
**Status:** Complete  

Gold includes deterministic orchestration, resume safety, STOP checkpoints, HITL enforcement, and structured audit logging.

---

## 3. System Architecture

The architecture follows:

**Perception â†’ Reasoning â†’ Action â†’ Audit**

### 3.1 Memory Layer (Obsidian Vault)

Vault root:

AI_Employee_Vault/

Primary folders:

- Inbox/
- Needs_Action/
- In_Progress/
- Pending_Approval/
- Approved/
- Rejected/
- Done/
- Briefings/
- Logs/
- Decisions/

Operational folders are ignored via `.gitignore`.

---

### 3.2 Perception Layer (Watchers)

Two watchers provide Silver foundation functionality:

**Filesystem Watcher**
- Monitors dropbox/
- Deduplicates via SHA256(file_bytes)
- Writes tasks into Needs_Action/
- Logs activity into Logs/

**Vault Health Watcher**
- Verifies required vault folders exist
- Logs health status
- Generates repair tasks if structure breaks

---

### 3.3 Reasoning Layer (Gold Loop)

File: `watchers/gold_loop.py`

Implements deterministic single-cycle orchestration:

Cycle phases:
1. SCAN
2. CLAIM (lock-based)
3. MOVE (ownership established)
4. IDLE (no external execution)

Key guarantees:
- Deterministic execution
- Lock-based exclusivity
- Manual STOP checkpoints
- Resume-safe restart logic
- No guessing after interruption
- Forensic continuity via persisted lock path

Runtime state:
AI_Employee_Vault/Logs/gold_runtime_state.json

---

### 3.4 Human-in-the-Loop (HITL)

Sensitive actions require manual approval.

Workflow:

Pending_Approval/ â†’ Approved/ â†’ Execution â†’ Done/

All approval events are logged.

Gold operates in draft-only mode for external actions.

---

### 3.5 Audit Logging

Append-only structured log:

AI_Employee_Vault/Logs/action_log_YYYY-MM-DD.jsonl

Each entry contains:
- timestamp
- actor
- event
- risk_level
- structured details

Example events:
- APPROVAL_CREATED
- APPROVAL_APPROVED
- MCP_DRAFT_EXECUTED
- CEO_BRIEFING_GENERATED

---

## 4. Weekly CEO Briefing (Gold Feature)

Generates a business summary from local vault data.

Output location:
AI_Employee_Vault/Briefings/

Run command:

python scripts/generate_ceo_briefing.py

Audit event logged as:
CEO_BRIEFING_GENERATED

---

## 5. Security Model (Gold)

- No autonomous external execution
- No hidden background processes during freeze
- STOP checkpoints at multiple phases
- Resume-safe crash detection
- Structured forensic state
- Vault operational folders ignored via git

Gold explicitly excludes:
- Real email sending
- Payment automation
- Social media automation
- Cloud deployment
- Multi-agent delegation

Those belong to Platinum tier.

---

## 6. Quick Start (Windows)

Prerequisites:
- Python 3.12+
- pip install watchdog

Run watchers manually:

cd "D:\Shoaib Project\Personal-AI-Employee"
py watchers\filesystem_watcher.py
py watchers\vault_health_watcher.py

Generate CEO briefing:

python scripts\generate_ceo_briefing.py

---

## 7. Repository Hygiene

Operational vault folders are ignored:
- Pending_Approval/
- Approved/
- Rejected/
- Done/
- Logs/
- Briefings/

Gold freeze tags:
- gold-v1
- gold-v1.1
- gold-v1.2
- gold-v1.3
- gold-v1.4
- gold-v1.5

---

## 8. Judge Notes

This implementation emphasizes:

- Determinism over autonomy
- Safety over automation
- Auditability over convenience
- Clear Gold vs Platinum boundaries

Gold tier is complete, reproducible, and audit-safe.


