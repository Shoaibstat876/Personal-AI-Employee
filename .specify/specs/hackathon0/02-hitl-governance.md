HITL GOVERNANCE SPEC — PERSONAL AI EMPLOYEE (HACKATHON 0)

Purpose

This document defines how Human-in-the-Loop (HITL) control is enforced in the Personal AI Employee system. It ensures that all meaningful actions are reviewed and approved by a human before execution, maintaining safety, control, and accountability.

HITL is not an optional feature. It is a mandatory control boundary that governs all execution.

HITL Definition

Human-in-the-Loop means that the system cannot execute meaningful actions independently. Every action must pass through a human decision point before execution is allowed.

The system can generate tasks and plans, but it cannot act on them without approval.

HITL Position in Workflow

HITL exists between the Planning and Execution stages:

Plan → Pending Approval → Approved → Execution

This ensures that no action moves from planning to execution without explicit human approval.

Approval Requirement

Every plan must be reviewed before execution.

Rules:

no plan can execute without approval
approval must be explicit
approval must generate a record
rejected plans must not execute

Approval is a hard gate. It cannot be bypassed.

Approval Artifacts

Each approval decision must produce a visible artifact in the system.

Approved plans are stored in:

AI_Employee_Vault/Approved/

Rejected plans are stored in:

AI_Employee_Vault/Rejected/

These files serve as proof that a decision was made.

Execution Control

Execution is only allowed when:

a valid approval exists
the plan is present in the Approved state
the task_id matches across all stages

The system must not execute:

from Pending Approval
from Rejected
from any uncontrolled state

Execution authority is strictly controlled.

Human Responsibility

The human operator is responsible for:

reviewing plans
validating actions
approving or rejecting execution
ensuring correctness before execution

The system assists, but the human decides.

System Restrictions

The system must not:

auto-approve plans
execute without approval
override human decisions
perform hidden actions
simulate approvals

All control must remain visible and enforced.

Traceability of Decisions

Every approval decision must be traceable through:

approval files
logs
task_id continuity

A reviewer must be able to follow:

task → plan → approval → execution → logs

without ambiguity.

Rejection Handling

If a plan is rejected:

it must not proceed to execution
it must remain in the Rejected state
it may be revised through a new plan

Rejected plans act as a stop condition.

HITL and Safety

HITL ensures:

no unintended execution
no unsafe actions
no uncontrolled automation
human oversight for all outcomes

This makes the system safe for real-world use.

HITL in Platinum Layer

In the Platinum model:

Cloud proposes and drafts updates
Local system performs approval and execution

Rules:

Cloud cannot execute
Local must approve before execution
all updates must pass through HITL

Execution authority remains local and human-controlled.

HITL Guarantees

The system guarantees that:

all actions are human-approved
all execution is intentional
all decisions are recorded
no hidden execution occurs

This ensures full control and accountability.

Final Understanding

HITL is the core control mechanism of the system. It ensures that AI assists in decision-making but does not replace human authority.

All meaningful actions are reviewed, approved, and executed under human supervision, making the system controlled, auditable, and trustworthy.