---
name: process-inbox
description: Convert incoming inputs into structured tasks within the system.
---

# SKILL: process-inbox

## Purpose
Convert incoming inputs into structured, trackable tasks inside the system.

---

## Real System Implementation
This skill is implemented through existing system components:

### Core Components
- filesystem watcher
- gmail bridge
- intake normalization logic

### Vault Mapping
- AI_Employee_Vault/Needs_Action/

### Artifacts
- TASK_*.md files

### Logs
- AI_Employee_Vault/Logs/watcher_filesystem_log.md
- AI_Employee_Vault/Logs/gmail_task_bridge_log.jsonl

---

## Source of Execution
All runtime behavior for this capability resides in the core system:

- watchers/
- tools/
- orchestrator logic
- MCP-connected workflow components

This is a **documentation layer only and does not contain runtime logic.**

---

## Inputs
- incoming files
- email-based task intake
- watcher-triggered ingestion events

---

## Outputs
- TASK_*.md files
- structured entries in:
  - AI_Employee_Vault/Needs_Action/

---

## Workflow Position
Inbox → Needs_Action → (next: generate-execution-plan)

---

## Safety Boundary
- this stage performs no execution
- only task creation and structuring are allowed
- downstream action requires planning and approval
- this skill operates within a controlled HITL workflow and does not bypass approval

---

## Evidence
- AI_Employee_Vault/Needs_Action/
- AI_Employee_Vault/Logs/watcher_filesystem_log.md
- AI_Employee_Vault/Logs/gmail_task_bridge_log.jsonl
- TASK_*.md files in vault

---

## Notes
This skill represents the intake layer of the system. It structures work for downstream planning and execution without performing actions itself.