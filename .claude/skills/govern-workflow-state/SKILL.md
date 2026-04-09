---
name: govern-workflow-state
description: Maintain consistent workflow state and enforce lifecycle transitions.
---

# SKILL: govern-workflow-state

## Purpose
Maintain consistent task lifecycle and enforce correct state transitions.

---

## Real System Implementation
This skill is implemented through existing system components:

### Core Components
- gold_loop.py
- watcher coordination logic

### Vault Mapping
- Inbox/
- Needs_Action/
- Plans/
- Pending_Approval/
- Approved/
- Done/

### Logs
- gold_runtime_state.json
- gold_loop.log.md

---

## Source of Execution
State transitions are enforced by:

- gold_loop.py
- watcher coordination
- vault movement rules

This is a **documentation layer only and does not contain runtime logic.**

---

## Inputs
- tasks and plans across workflow

---

## Outputs
- controlled state transitions

---

## Workflow Position
Global control layer across entire system

---

## Safety Boundary
- no step is skipped
- no execution outside workflow
- deterministic transitions enforced
- this skill operates within a controlled HITL workflow and does not bypass approval

---

## Evidence
- AI_Employee_Vault structure
- gold_runtime_state.json
- gold_loop.log.md

---

## Notes
This is the system governor ensuring lifecycle integrity.