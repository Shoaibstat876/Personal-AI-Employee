PHASE 2 — FINAL VIDEO SCRIPT (80–90 SECONDS)
Scene 1 — Identity

Time: 0:00–0:06
Show: Dashboard
Say:
“This is my Personal AI Employee, a Human-in-the-Loop AI system for controlled execution, approval, and audit logging.”

Scene 2 — Workflow overview

Time: 0:06–0:12
Show: Dashboard workflow section
Say:
“It converts incoming work into structured tasks, plans, approvals, execution, and traceable logs.”

Scene 3 — Live MCP proof

Time: 0:12–0:19
Run:

claude mcp list

Say:
“All major MCP integrations are connected live, including filesystem, Gmail, Slack, GitHub, Odoo, Playwright, and calendar.”

Scene 4 — Final branch and clean state

Time: 0:19–0:25
Run:

git branch --show-current
git status

Say:
“This is the final demo branch, and the working tree is clean.”

Scene 5 — Project structure

Time: 0:25–0:31
Run:

dir

Say:
“The project is organized into workflow, tools, UI, logs, and evidence layers.”

Scene 6 — Vault as workflow engine

Time: 0:31–0:37
Run:

dir AI_Employee_Vault

Say:
“The vault acts as the system memory and state machine.”

Scene 7 — Task to plan to approval

Time: 0:37–0:47
Run:

dir AI_Employee_Vault\Needs_Action
dir AI_Employee_Vault\Plans
dir AI_Employee_Vault\Pending_Approval

Say:
“This shows the controlled lifecycle from task intake to AI planning to approval gating.”

Scene 8 — Approved to done

Time: 0:47–0:55
Run:

dir AI_Employee_Vault\Approved
dir AI_Employee_Vault\Done

Say:
“No sensitive action proceeds without approval, and completed work is preserved in final state.”

Scene 9 — Audit log proof

Time: 0:55–1:03
Run:

Get-ChildItem AI_Employee_Vault\Logs
Get-Content AI_Employee_Vault\Logs\odoo_execution_log.jsonl -Tail 3

Say:
“All important actions are logged, making the system auditable and verifiable.”

Scene 10 — CEO reporting

Time: 1:03–1:09
Run:

dir AI_Employee_Vault\Briefings

Say:
“The system also generates executive summaries and reporting outputs.”

Scene 11 — Platinum evidence

Time: 1:09–1:18
Run:

dir AI_Employee_Vault\Artifacts\PLATINUM_EVIDENCE_PACK

Say:
“The Platinum layer adds visibility, control clarity, and presentation-ready validation without changing Gold execution logic.”

Scene 12 — Final close

Time: 1:18–1:30
Show: Dashboard again
Say:
“This project proves that AI systems can be structured, human-controlled, and fully auditable for real-world workflow operations.”