---
name: manage-human-approval
description: Enforce human approval before any real-world action is executed.
---

# SKILL: manage-human-approval

## Purpose
Enforce Human-In-The-Loop (HITL) control before any real-world action is executed.

---

## Real System Implementation
This skill is implemented through existing system components:

### Core Components
- tools/generate_approval_from_plan.py
- record_approval_decision.py

### Vault Mapping
- AI_Employee_Vault/Pending_Approval/
- AI_Employee_Vault/Approved/
- AI_Employee_Vault/Rejected/

### Artifacts
- APPROVAL_*.md files

### Logs
- AI_Employee_Vault/Logs/approval_decision_log.jsonl

---

## Source of Execution
Approval logic is enforced by:

- tools/
- vault state transitions
- orchestrator (gold_loop)

This is a **documentation layer only and does not contain runtime logic.**

---

## Inputs
- PLAN_*.md files

---

## Outputs
- approved plans → AI_Employee_Vault/Approved/
- rejected plans → AI_Employee_Vault/Rejected/

---

## Workflow Position
Plans → Pending_Approval → Approved / Rejected

---

## Safety Boundary
- no execution without explicit approval
- human decision is mandatory
- system cannot bypass approval logic
- this skill operates within a controlled HITL workflow and does not bypass approval

---

## Evidence
- AI_Employee_Vault/Pending_Approval/
- AI_Employee_Vault/Approved/
- AI_Employee_Vault/Rejected/
- approval_decision_log.jsonl

---

## Notes
This is the primary safety gate controlling all execution.