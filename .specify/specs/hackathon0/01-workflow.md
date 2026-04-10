WORKFLOW SPEC — PERSONAL AI EMPLOYEE (HACKATHON 0)
Purpose

This document defines the complete operational workflow of the Personal AI Employee system. It describes how tasks move through the system from intake to completion while maintaining full control, traceability, and verifiable evidence.

The workflow ensures that every action is structured, approved, executed, and logged in a deterministic and auditable manner.

Workflow Overview

The system follows a strict, deterministic lifecycle:

Intake → Task → Plan → Pending Approval → Approved → Execution → Logs → Done

Each stage is represented through filesystem state and file transitions. No stage is hidden, skipped, or implicitly executed.

Stage 1 — Intake
Sources

Tasks enter the system through:

filesystem watcher
email bridge
Behavior
incoming data is detected automatically
input is converted into a structured task file
task is prepared for processing
Output

Tasks are placed in:

AI_Employee_Vault/Needs_Action/

Stage 2 — Task Creation
Behavior
raw input is normalized into a structured task format
a unique task_id is assigned
task metadata is prepared
Requirements
each task must be uniquely identifiable
task must be stored as a file
task must be ready for planning
Stage 3 — Planning
Behavior
task is processed by the planning system
a structured plan is generated from task content
plan defines actionable steps
Output

Plans are stored in:

AI_Employee_Vault/Plans/

Requirements
plan must reference the original task_id
plan must be complete and review-ready
plan must not trigger execution
Stage 4 — Pending Approval
Behavior
generated plan is moved to approval stage
system waits for human decision
Output

Plans are moved to:

AI_Employee_Vault/Pending_Approval/

Requirements
no execution occurs at this stage
plan must remain unchanged
system must wait for explicit approval
Stage 5 — Approval Decision
Behavior

Human operator reviews the plan and decides:

approve → move to Approved
reject → move to Rejected
Output Locations

Approved plans:

AI_Employee_Vault/Approved/

Rejected plans:

AI_Employee_Vault/Rejected/

Requirements
decision must be explicit
approval must generate an artifact
rejected plans must never execute
Stage 6 — Execution
Behavior
only approved plans are executed
execution is triggered in a controlled manner
Examples
creating records (Odoo)
Slack actions
email drafting
social content generation
Requirements
execution must reference the same task_id
execution must produce logs
execution must produce artifacts
no execution without approval
Stage 7 — Logging
Behavior
all system activity is recorded
execution results are captured
Log Types
execution logs (JSONL)
workflow logs (markdown)
approval logs
briefing logs
Requirements
logs must be append-only
logs must reflect real execution
logs must include timestamps and context
logs must not be modified after creation
Stage 8 — Completion (Done)
Behavior
task is finalized after execution and logging
system marks workflow as complete
Output

Completed tasks are stored in:

AI_Employee_Vault/Done/

Requirements
task must have full lifecycle trace
all stages must be completed
logs and artifacts must exist
Task Identity Continuity

The task_id must remain consistent across all stages:

Needs_Action
Plans
Pending_Approval
Approved
Execution logs
Done

This ensures full traceability of each task throughout the system.

State Transition Rules
tasks must move forward only
no stage may be skipped
transitions must be visible in the filesystem
no hidden or implicit transitions are allowed
Deterministic Behavior

For the same input:

workflow path remains consistent
outputs remain predictable
transitions remain traceable

No randomness or hidden branching is allowed in execution.

Error Handling
all failures must be logged
retry logic must be explicit
system must not fail silently
partial execution must be visible
Platinum Workflow Extension

The Platinum layer introduces an additional update flow:

Updates/Incoming → Updates/Claimed → Updates/Processed → Bridge to Gold Workflow

Rules
updates must be claimed before processing
claim-by-move establishes ownership
execution cannot occur directly from Updates
all execution must pass through the main workflow
Workflow Guarantees

This workflow guarantees that:

all actions are human-controlled
all steps are visible and auditable
all outputs are backed by logs and artifacts
all tasks follow a consistent lifecycle
Final Summary

The workflow defines a controlled system where tasks are transformed into approved and executed actions through a structured pipeline. Every step is traceable, every action is verified, and every result is recorded.

This ensures a system that is deterministic, auditable, evidence-driven, and safe for real-world operation.