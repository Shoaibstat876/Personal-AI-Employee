---
name: generate-execution-plan
description: Transform tasks into deterministic execution plans before action.
---

# SKILL: generate-execution-plan

## Purpose
Transform structured tasks into deterministic, reviewable execution plans before any action is taken.

---

## Real System Implementation
This skill is implemented through existing system components:

### Core Components
- tools/generate_plan_from_email_task.py
- bridge_inprogress_to_plan.py

### Vault Mapping
- AI_Employee_Vault/Plans/

### Artifacts
- PLAN_*.md files

### Logs
- plan generation traces in workflow logs
- AI_Employee_Vault/Logs/gold_loop.log.md

---

## Source of Execution
All runtime behavior for this capability resides in the core system:

- tools/
- watcher-triggered processing
- orchestrator (gold_loop)

This is a **documentation layer only and does not contain runtime logic.**

---

## Inputs
- TASK_*.md files from:
  - AI_Employee_Vault/Needs_Action/
  - AI_Employee_Vault/In_Progress/

---

## Outputs
- PLAN_*.md files
- plans moved to:
  - AI_Employee_Vault/Pending_Approval/

---

## Workflow Position
Needs_Action → Plans → Pending_Approval

---

## Safety Boundary
- plans define intent but do not execute actions
- execution requires explicit human approval
- prevents direct task-to-execution flow
- this skill operates within a controlled HITL workflow and does not bypass approval

---

## Evidence
- AI_Employee_Vault/Plans/
- AI_Employee_Vault/Pending_Approval/
- PLAN_*.md files
- gold_loop.log.md

---

## Notes
This skill represents the reasoning layer, converting raw tasks into structured execution intent.