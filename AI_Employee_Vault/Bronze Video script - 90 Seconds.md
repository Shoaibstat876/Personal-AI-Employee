🎥 Hackathon 0 — Bronze Tier
✅ Ultra Simple • Clean • Safe Final Script
⚠️ OPTIONAL CLEAN RESET (SAFE)

This removes demo artifacts only.
It does NOT modify architecture.

Open PowerShell:

cd "D:\Shoaib Project\Personal-AI-Employee"

Remove-Item ".\dropbox\demo.txt" -Force -ErrorAction SilentlyContinue
Remove-Item ".\AI_Employee_Vault\Inbox\demo.txt" -Force -ErrorAction SilentlyContinue
Remove-Item ".\AI_Employee_Vault\Needs_Action\TASK_FILE_*" -Force -ErrorAction SilentlyContinue
Remove-Item ".\AI_Employee_Vault\Done\SUMMARY_*" -Force -ErrorAction SilentlyContinue


✅ Watcher untouched
✅ Contracts untouched
✅ Skills untouched
✅ Action stub untouched
✅ Vault structure untouched

Safe.

🎬 0️⃣ Start Recording

Say clearly:

Assalam-o-Alaikum.
I’m Shoaib.
This is my Hackathon 0 Bronze Tier submission.
Bronze demonstrates deterministic ingestion and Claude vault integration only.

1️⃣ Show Project Root
cd "D:\Shoaib Project\Personal-AI-Employee"
dir


Say:

This is the project root.
It contains the vault, watcher scripts, and dropbox input folder.

2️⃣ Start Watcher (Perception Layer)
python "watchers\file_drop_watcher.py"


Say:

The watcher is running.
It only performs ingestion. No reasoning. No automation.

3️⃣ Drop Demo File (Second Terminal)

Open a second PowerShell window.

Paste:

cd "D:\Shoaib Project\Personal-AI-Employee"
"BRONZE_DEMO" | Set-Content ".\dropbox\demo.txt"


Now look at the watcher window.

You will see something like:

[OK] task_id=dbd710d7a5394584


Say:

The watcher generated a deterministic task_id and created a TASK file.

4️⃣ Stop Watcher

In watcher window press:

CTRL + C


Say:

Bronze does not run unattended. Watcher stopped.

5️⃣ Verify Ingestion

Back in main PowerShell:

cd "D:\Shoaib Project\Personal-AI-Employee"

dir ".\AI_Employee_Vault\Inbox"
dir ".\AI_Employee_Vault\Needs_Action"
dir ".\dropbox\_processed"


Say:

Raw file stored in Inbox.
TASK file created in Needs_Action.
Original moved to _processed.
Ingestion is deterministic and replay-safe.

🟢 6️⃣ Claude Part (SAFE INTERACTIVE METHOD)

⚠️ Do NOT use -p
⚠️ Use normal interactive Claude

Step 6.1 — Enter Vault
cd "D:\Shoaib Project\Personal-AI-Employee\AI_Employee_Vault"

Step 6.2 — Launch Claude
claude


You will see:

❯

Step 6.3 — Paste This Exactly
Bronze tier only. Read the latest TASK file in ./Needs_Action and apply ./skills/basic_processor/SKILL.md. Create exactly one summary file in ./Done. Do not create anything else.


Press Enter.

Step 6.4 — When Claude Asks Permission

If it shows:

Do you trust the files in this folder?

Choose:

1


If it asks to confirm writing the file:

Choose:

1


That’s it.

No other clicks.
No MCP setup.
Ignore any footer message like "1 MCP server failed".

It does NOT affect Bronze.

Step 6.5 — Exit Claude

After Claude says it created the summary:

Type:

/exit


Press Enter.

You are back in PowerShell.

7️⃣ Show Result

Make sure you are inside the vault:

cd "D:\Shoaib Project\Personal-AI-Employee\AI_Employee_Vault"


Now:

dir ".\Done"


You will see something like:

SUMMARY_dbd710d7a5394584.md


Now copy that exact filename and run:

Get-Content ".\Done\SUMMARY_dbd710d7a5394584.md"


(Replace with the real filename shown.)

Say clearly:

Claude read from the vault and wrote back to the vault using an Agent Skill.
No external automation.
No MCP.
No orchestrator.

🔒 8️⃣ Final Line (Very Important)

Say slowly and confidently:

Bronze Tier is deterministic, audit-traceable, skill-based, and strictly within teacher boundaries.
Thank you.