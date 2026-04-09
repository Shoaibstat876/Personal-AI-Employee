PHASE 1 — COMMAND TESTING BEFORE RECORDING
Run these first, in order, before you record.
If all run cleanly, then record.
# 1) Confirm all MCP integrations are connected
claude mcp list

# 2) Confirm you are on the final demo branch
git branch --show-current

# 3) Confirm repo is clean and demo-safe
git status

# 4) Show project structure at root level
dir

# 5) Show core vault structure
dir AI_Employee_Vault

# 6) Show task intake layer
dir AI_Employee_Vault\Needs_Action

# 7) Show planning layer
dir AI_Employee_Vault\Plans

# 8) Show approval gate
dir AI_Employee_Vault\Pending_Approval

# 9) Show approved state
dir AI_Employee_Vault\Approved

# 10) Show completed state
dir AI_Employee_Vault\Done

# 11) Show log inventory
Get-ChildItem AI_Employee_Vault\Logs

# 12) Show execution proof from one real integration
Get-Content AI_Employee_Vault\Logs\odoo_execution_log.jsonl -Tail 3

# 13) Show reporting layer
dir AI_Employee_Vault\Briefings

# 14) Show Gold evidence layer
dir evidence\gold

# 15) Show Platinum evidence pack
dir AI_Employee_Vault\Artifacts\PLATINUM_EVIDENCE_PACK
If any command looks noisy, keep it out of the recorded video.
But based on your current state, this set is strong.
________________________________________
PHASE 2 — FINAL VIDEO SCRIPT (80–90 SECONDS)
Scene 1 — Identity
Time: 0:00–0:06
Show: Dashboard
Say:
“This is my Personal AI Employee, a Human-in-the-Loop AI system for controlled execution, approval, and audit logging.”
________________________________________
Scene 2 — Workflow overview
Time: 0:06–0:12
Show: Dashboard workflow section
Say:
“It converts incoming work into structured tasks, plans, approvals, execution, and traceable logs.”
________________________________________
Scene 3 — Live MCP proof
Time: 0:12–0:19
Run:
claude mcp list
Say:
“All major MCP integrations are connected live, including filesystem, Gmail, Slack, GitHub, Odoo, Playwright, and calendar.”
________________________________________
Scene 4 — Final branch and clean state
Time: 0:19–0:25
Run:
git branch --show-current
git status
Say:
“This is the final demo branch, and the working tree is clean.”
________________________________________
Scene 5 — Project structure
Time: 0:25–0:31
Run:
dir
Say:
“The project is organized into workflow, tools, UI, logs, and evidence layers.”
________________________________________
Scene 6 — Vault as workflow engine
Time: 0:31–0:37
Run:
dir AI_Employee_Vault
Say:
“The vault acts as the system memory and state machine.”
________________________________________
Scene 7 — Task to plan to approval
Time: 0:37–0:47
Run:
dir AI_Employee_Vault\Needs_Action
dir AI_Employee_Vault\Plans
dir AI_Employee_Vault\Pending_Approval
Say:
“This shows the controlled lifecycle from task intake to AI planning to approval gating.”
________________________________________
Scene 8 — Approved to done
Time: 0:47–0:55
Run:
dir AI_Employee_Vault\Approved
dir AI_Employee_Vault\Done
Say:
“No sensitive action proceeds without approval, and completed work is preserved in final state.”
________________________________________
Scene 9 — Audit log proof
Time: 0:55–1:03
Run:
Get-ChildItem AI_Employee_Vault\Logs
Get-Content AI_Employee_Vault\Logs\odoo_execution_log.jsonl -Tail 3
Say:
“All important actions are logged, making the system auditable and verifiable.”
________________________________________
Scene 10 — CEO reporting
Time: 1:03–1:09
Run:
dir AI_Employee_Vault\Briefings
Say:
“The system also generates executive summaries and reporting outputs.”
________________________________________
Scene 11 — Platinum evidence
Time: 1:09–1:18
Run:
dir AI_Employee_Vault\Artifacts\PLATINUM_EVIDENCE_PACK
Say:
“The Platinum layer adds visibility, control clarity, and presentation-ready validation without changing Gold execution logic.”
________________________________________
Scene 12 — Final close
Time: 1:18–1:30
Show: Dashboard again
Say:
“This project proves that AI systems can be structured, human-controlled, and fully auditable for real-world workflow operations.”
________________________________________
PHASE 3 — COMMAND PACK FOR THE RECORDED VIDEO
Use this exact pack in the video if your dry run looks clean:
# Live MCP health proof
claude mcp list

# Final demo branch and clean state
git branch --show-current
git status

# Root project architecture
dir

# Vault state machine
dir AI_Employee_Vault

# Task intake
dir AI_Employee_Vault\Needs_Action

# Planning layer
dir AI_Employee_Vault\Plans

# Approval gate
dir AI_Employee_Vault\Pending_Approval

# Human-approved state
dir AI_Employee_Vault\Approved

# Final completed state
dir AI_Employee_Vault\Done

# Audit log inventory
Get-ChildItem AI_Employee_Vault\Logs

# Real execution proof
Get-Content AI_Employee_Vault\Logs\odoo_execution_log.jsonl -Tail 3

# Reporting proof
dir AI_Employee_Vault\Briefings

# Platinum evidence pack
dir AI_Employee_Vault\Artifacts\PLATINUM_EVIDENCE_PACK
________________________________________
PHASE 4 — ONE-GO COMMAND BLOCK FOR PRACTICE
Use this for rehearsal before recording:
claude mcp list
git branch --show-current
git status
dir
dir AI_Employee_Vault
dir AI_Employee_Vault\Needs_Action
dir AI_Employee_Vault\Plans
dir AI_Employee_Vault\Pending_Approval
dir AI_Employee_Vault\Approved
dir AI_Employee_Vault\Done
Get-ChildItem AI_Employee_Vault\Logs
Get-Content AI_Employee_Vault\Logs\odoo_execution_log.jsonl -Tail 3
dir AI_Employee_Vault\Briefings
dir AI_Employee_Vault\Artifacts\PLATINUM_EVIDENCE_PACK
________________________________________
PHASE 5 — PROFESSIONAL DELIVERY TIPS
Keep terminal zoom around 125% to 140%.
Pause one second after each command.
When a command finishes, say one sentence only.
Best speaking rhythm:
•	show 
•	explain 
•	move 
Do not narrate every folder name.
Do not mention tiny UI issues.
Do not say “I think” or “maybe.”
Say:
•	“This proves...” 
•	“This shows...” 
•	“This layer enforces...” 
•	“This output confirms...” 
________________________________________
FINAL JUDGE-SAFE POSITIONING
Your strongest message is:
“Gold proves real execution. Platinum adds visibility and control clarity.”
