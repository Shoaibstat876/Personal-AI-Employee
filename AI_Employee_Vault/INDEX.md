## Bronze Logical Contracts (v1)

### TASK_FILE Contract (Needs_Action/)

Required Front-Matter (YAML):

task_id: "<deterministic_id>"
title: "<short_title>"
created_at: "<YYYY-MM-DD>"
created_by: "<human_name>"
priority: "<Low|Medium|High|Critical>"
status: "Needs_Action"
tier: "Bronze"
layer: "Logical"

Rules:
- task_id must be deterministic and never reused.
- status must be "Needs_Action" at creation.
- No execution logic allowed in Bronze.


### PLAN_FILE Contract (Plans/)

Mandatory Structure:

# Plan: <title>

## Metadata
- task_id: <deterministic_id>
- related_task: <task_file_name>
- tier: Bronze
- layer: Logical
- skill_reference: <required_skill_name>

## Objective
## Constraints
## Steps (definition only)
## Risks
## Approval Requirement

Rules:
- skill_reference is mandatory.
- No runtime execution logic.
- Must reference an existing task_id.


### APPROVAL Contract (Pending_Approval/)

Required Fields (YAML):

approval_id: "<deterministic_id>"
task_id: "<related_task_id>"
requested_by: "<agent_or_human>"
requested_at: "<YYYY-MM-DD>"
decision: "<Approved|Rejected|Deferred>"
decided_by: "<human_only>"
decision_date: "<YYYY-MM-DD>"
execution_authorized: "<true|false>"

Rules:
- decided_by must always be a human.
- execution_authorized is flag only (no execution in Bronze).
- No self-approval.


### LOGGING Contract (Logs/)

Rules:
- Append-only. Never edit past entries.
- Each entry must include:
  - timestamp (ISO-8601)
  - task_id
  - event_type
  - actor
  - short note


### CLAIM-BY-MOVE Rule

Movement:
Needs_Action/ → In_Progress/<agent_name>/

Rules:
- Only agent-name subfolders allowed.
- Claim occurs strictly by move (not copy).
- No automation allowed in Bronze.
