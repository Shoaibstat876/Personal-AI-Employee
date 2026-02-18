# Personal AI Employee — Hackathon 0 (Silver Tier)

**Tagline:** Your life and business on autopilot — local-first, agent-driven, human-in-the-loop.

This repository implements a **Silver-tier** “Digital FTE” architecture using:
- **Obsidian vault (local markdown)** as memory/dashboard
- **Watchers (Python)** as Perception layer
- **Human-in-the-loop approval workflow**
- **Windows Task Scheduler** for background-safe execution

---

## ✅ Tier Declaration
**Target Tier:** Silver  
**Status:** Complete (Perception + Scheduling + Dedup + Logs + HITL workflow)

---

## Architecture (Perception → Reasoning → Action)

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

#### A) Filesystem Watcher (dropbox → Needs_Action)
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
- If the content hash already exists → archive file and log `DEDUP_SKIP` (NO new task)

### 4) Human-in-the-loop approvals
Approval artifacts live in `AI_Employee_Vault/Approved/` and can be:
- `status: approved` + `executed: false` → eligible for execution
- `executed: true` → completed
- `status: revoked` → permanently skipped

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
