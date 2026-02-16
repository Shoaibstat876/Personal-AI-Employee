## Bronze Vault Rules (v1)

### Definition-Only Stage
Bronze phase defines contracts only.  
No runtime logic.  
No watchers.  
No orchestration.  
No automation.

### Automation Prohibition
No scripts.  
No background processing.  
No execution loops.  
No hidden state.

### Naming Discipline
Folder names must match canonical casing.  
Deterministic IDs required.  
No ad-hoc naming.

### Movement Rules Summary
- Tasks begin in Needs_Action/
- Claimed by moving to In_Progress/<agent_name>/
- Approvals stored in Pending_Approval/
- Logs stored in Logs/
- Completion moves to Done/

### Approval Authority Boundary
Human decision required before execution in higher tiers.  
Agents cannot self-authorize.  
Bronze does not execute.


## Bronze Reasoning Layer (Manual Agent Only)

### Purpose
The Bronze Reasoning Layer defines how a human or local agent manually processes tasks through structured thinking and controlled state transitions.

This layer introduces no automation, no persistent loops, and no execution engine.

It is purely procedural.

### Scope
Applies only to movement between:

Needs_Action/  
Plans/  
Pending_Approval/

No other folders are involved in Bronze Reasoning.

### 1️⃣ Manual Planning Procedure
When a TASK_FILE exists in Needs_Action/:

Agent reads TASK_FILE.

Agent claims task using Claim-by-Move Rule:

Needs_Action/ → In_Progress/<agent>/

Agent creates a corresponding PLAN file in Plans/.

No automation performs these steps.

### 2️⃣ PLAN Creation Rule
A PLAN file must:

Reside in Plans/  
Reference the same task_id  
Follow the PLAN_FILE Contract  
Include at least one skill_reference  
Define objective, scope, steps, inputs, outputs, validation  

PLAN files define intent only.  
They do not execute actions.

### 3️⃣ Approval Request Creation Rule
Once PLAN is complete:

Agent creates an Approval file in Pending_Approval/

Approval must comply strictly with the APPROVAL File Contract (E.2 boundaries enforced)

Human must review and decide.

No auto-approval allowed.

### 4️⃣ Movement Rules
State transitions are manual:

Needs_Action/ → In_Progress/<agent>/ (claim)  
In_Progress/<agent>/ → Pending_Approval/ (request approval)  
Pending_Approval/ → Approved/ or Rejected/ (human decision)  
Approved/ → Done/ (after execution in future tiers)

No other transitions are permitted.

### 5️⃣ Failure Handling Rule
If:

PLAN is invalid  
Required fields missing  
Approval rejected  

Then:

Task returns to Needs_Action/  
Agent must revise PLAN  

No silent correction allowed.  
All corrections must be explicit and deterministic.

### Bronze Boundary Enforcement
The Bronze Reasoning Layer:

Does not invoke Claude  
Does not trigger execution  
Does not create automation  
Does not modify business records  
Does not write outside defined vault folders  

It is a controlled manual reasoning protocol only.
