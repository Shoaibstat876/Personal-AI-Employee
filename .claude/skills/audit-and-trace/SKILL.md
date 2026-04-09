---
name: audit-and-trace
description: Provide full traceability and auditability across all system operations.
---

# SKILL: audit-and-trace

## Purpose
Provide full traceability and auditability of all system operations.

---

## Real System Implementation
This skill is implemented through existing system components:

### Core Components
- centralized logging across pipeline

### Vault Mapping
- AI_Employee_Vault/Logs/

### Logs
- watcher_filesystem_log.md
- gold_loop.log.md
- action_log_*.jsonl
- approval_decision_log.jsonl
- execution logs

---

## Source of Execution
Logging is enforced by:

- logging hooks
- orchestrator (gold_loop)
- MCP integrations

This is a **documentation layer only and does not contain runtime logic.**

---

## Inputs
- all system events (intake, planning, approval, execution)

---

## Outputs
- append-only logs
- traceable system history

---

## Workflow Position
Cross-cutting layer across entire system

---

## Safety Boundary
- logs are append-only
- no silent actions
- full visibility maintained
- this skill operates within a controlled HITL workflow and does not bypass approval

---

## Evidence
- AI_Employee_Vault/Logs/
- JSONL logs

---

## Notes
This is the audit backbone ensuring traceability and verification.