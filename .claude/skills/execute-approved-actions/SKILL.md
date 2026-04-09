---
name: execute-approved-actions
description: Execute approved tasks through controlled integrations with full traceability.
---

# SKILL: execute-approved-actions

## Purpose
Execute approved tasks through controlled integrations with full traceability.

---

## Real System Implementation
This skill is implemented through existing system components:

### Core Components
- MCP integrations (Odoo, Slack, Email, Social, Browser)

### Vault Mapping
- AI_Employee_Vault/Done/
- AI_Employee_Vault/Artifacts/

### Artifacts
- ODOO_ACTION_*.md
- SLACK_ACTION_*.md
- EMAIL_DRAFT_ACTION_*.md

### Logs
- AI_Employee_Vault/Logs/odoo_execution_log.jsonl
- AI_Employee_Vault/Logs/slack_execution_log.jsonl
- AI_Employee_Vault/Logs/draft_execution_log.jsonl

---

## Source of Execution
Execution is handled by:

- MCP integrations
- tools/
- orchestrator (gold_loop)

This is a **documentation layer only and does not contain runtime logic.**

---

## Inputs
- approved plans from:
  - AI_Employee_Vault/Approved/

---

## Outputs
- executed actions
- artifacts stored in:
  - AI_Employee_Vault/Artifacts/
- tasks moved to:
  - AI_Employee_Vault/Done/

---

## Workflow Position
Approved → Execution → Done

---

## Safety Boundary
- execution occurs only after approval
- all actions are logged and traceable
- duplicate execution is prevented
- this skill operates within a controlled HITL workflow and does not bypass approval

---

## Evidence
- AI_Employee_Vault/Done/
- AI_Employee_Vault/Artifacts/
- execution logs

---

## Notes
This is the action layer where approved plans become real-world operations.