🎥 HACKATHON 0 — BRONZE TIER
🔐 EXECUTION VIDEO SCRIPT BOOK (FINAL VERSION)
🟢 BEFORE RECORDING (Preparation – Do This Once)

Close all terminals.

Open one PowerShell.

Run:

cd "D:\Shoaib Project\Personal-AI-Employee"

# Clean dropbox root only
Remove-Item ".\dropbox\*.txt" -Force -ErrorAction SilentlyContinue


Do NOT delete _processed.

Now you are clean.

Start screen recording.

🎬 RECORDING STARTS
0️⃣ INTRODUCTION (20–30 seconds)

Say:

Assalam-o-Alaikum.
I’m Shoaib.
This is my Hackathon 0 project: Personal AI Employee — a Local-First Autonomous Digital FTE architecture.
Today I am demonstrating Bronze Tier only, strictly within teacher guidelines.

1️⃣ BRONZE DECLARATION

Say clearly:

Bronze Tier focuses on deterministic, auditable autonomy with strict boundaries:

No orchestrator

No MCP integrations

No network calls

No background execution loops

No automatic approvals

Bronze includes:

One working Watcher

Vault-based governance

Manual reasoning contracts

Agent Skill implementation

Claude Code read/write integration

Action Layer stub only

Pause 2 seconds.

2️⃣ SHOW PROJECT ROOT

Run:

cd "D:\Shoaib Project\Personal-AI-Employee"
dir


Say:

AI_Employee_Vault is the system of record.
watchers/ contains perception scripts.
dropbox/ acts as the input channel.

Pause.

3️⃣ SHOW VAULT STRUCTURE

Run:

tree ".\AI_Employee_Vault"


Say:

This vault is the contract-based memory and control layer.

Highlight verbally:

Inbox — raw ingested inputs

Needs_Action — task files

Plans — structured planning

Pending_Approval — human gate

Logs — audit layer

skills — Agent Skills

Done — completed artifacts

Pause.

4️⃣ SHOW CONTRACTS

Open:

AI_Employee_Vault\Company_Handbook.md


Scroll slowly.

Say:

Bronze Vault Rules enforce:

Definition-only architecture

No automation in reasoning

Deterministic movement rules

Human approval boundaries

Scroll to:

Bronze Reasoning Layer (Manual Agent Only)

Say:

All reasoning transitions are manual.
No runtime execution.

5️⃣ SHOW AGENT SKILL

Open:

skills\basic_processor\SKILL.md


Say:

Teacher requirement:
All AI functionality must be implemented as Agent Skills.

This skill:

Reads a TASK

Generates structured summary

Writes output to Done

No external execution

This satisfies the Agent Skills requirement.

Pause.

6️⃣ SHOW ACTION LAYER STUB

Open:

Logs\action_layer_stub.md


Say:

Bronze Action Layer is intentionally a stub.
Execution is deferred to Silver and Gold.
This preserves tier discipline.

Pause.

🔥 7️⃣ LIVE PERCEPTION DEMO
7.1 START WATCHER

Run:

cd "D:\Shoaib Project\Personal-AI-Employee"
python "watchers\file_drop_watcher.py"


Pause 2 seconds.

Say:

Watcher is running.

7.2 DROP FILE (Open Second PowerShell Window)

Run:

cd "D:\Shoaib Project\Personal-AI-Employee"
"BRONZE_DEMO_FILE" | Set-Content ".\dropbox\demo_file.txt"


Switch back to watcher window.

Pause until you see:

[OK] task_id=xxxxxxxxxxxxxxxx


Zoom slightly if needed.

Say:

The watcher generated a deterministic task_id based on file hash.

7.3 VERIFY INGESTION

Open third PowerShell OR reuse second:

cd "D:\Shoaib Project\Personal-AI-Employee"

dir ".\AI_Employee_Vault\Inbox" | findstr demo_file
dir ".\AI_Employee_Vault\Needs_Action" | findstr TASK_FILE_
dir ".\dropbox\_processed" | findstr demo_file


Say:

Verified:

Stored in Inbox

TASK created

Moved to _processed

Ingestion is deterministic and replay-safe.

Pause.

🧠 8️⃣ CLAUDE INTEGRATION PROOF

This is the final Bronze requirement.

8.1 OPEN VAULT
cd "D:\Shoaib Project\Personal-AI-Employee\AI_Employee_Vault"

8.2 RUN CLAUDE

Replace <task_id> with the ID shown above.

Example:

claude "You are operating in Bronze tier. Read ./Needs_Action/TASK_FILE_<task_id>.md and apply the skill in ./skills/basic_processor/SKILL.md. Create exactly one file: ./Done/SUMMARY_<task_id>.md in the Output Format defined by the skill. Do not create any other files. Do not modify the TASK file."


When prompted:

Select:

1. Yes, proceed


Then approve:

Done\SUMMARY_<task_id>.md


Pause until Claude finishes.

8.3 SHOW SUMMARY FILE

Run:

Get-Content ".\Done\SUMMARY_<task_id>.md"


Pause.

Say:

Claude read from the vault and wrote back to the vault using the defined Skill.

No orchestrator.
No MCP.
No external execution.

This completes the Bronze integration requirement.

🔒 9️⃣ STOP WATCHER

Return to watcher window.

Press:

CTRL+C


Say:

Bronze does not run unattended.
No background execution loops are active.

🟢 1️⃣0️⃣ FINAL DECLARATION

Say clearly and confidently:

Bronze Tier is:

✔ Structurally complete
✔ Deterministic
✔ Idempotent via task_id
✔ Audit-traceable
✔ Skill-based
✔ Claude-integrated
✔ Human-controlled
✔ Action-safe

This completes Bronze Tier under official hackathon requirements.

Thank you.

Pause 3 seconds.

Stop recording.

🏁 END