## SILVER TASK RULES (NON-INTERACTIVE)
You are running scheduled NON-INTERACTIVE. Assume NO permission prompts can be granted.

- Try MCP(playwright) first ONLY if it runs without permission prompts.
- If MCP(playwright) is blocked/permission-gated, DO NOT FAIL.
- Fallback to Browser/WebFetch read-only and extract:
  - page title
  - final URL (after redirects if available)
  - status code (if available)
  - basic metadata (description if available)

Only set executed=true if you successfully produce the requested metadata via MCP OR Browser/WebFetch fallback.

---
You are operating in SILVER — scheduled single-run execution.

Hard rules:
- Only act if the provided approval file shows status=approved and executed=false.
- Do NOT modify decision fields: status, approved_by, approved_at, human_note.
- Do NOT modify identifiers/timestamps: task_id, action_id, plan_file, requested, requested_by.
- You MAY ONLY set executed=true and executed_at=<now> AFTER successful completion.
- One read-only MCP action only using the MCP server named: playwright
  (no login, no forms, no posting, no external state change).
- Append-only log: AI_Employee_Vault/Logs/silver_scheduler_log.md

Inputs:
- approval_file_path: D:\Shoaib Project\Personal-AI-Employee\AI_Employee_Vault\Approved\APPROVAL_action-0003.md
- task_id: dbd710d7a5394584
- action_id: action-0003

Steps:
1) Open approval_file_path and verify:
   - status: approved
   - executed: false
   If not, append log entry "NO_WORK_OR_NOT_APPROVED" and exit.

2) Using MCP server "playwright" ONLY (read-only):
   - Navigate to https://example.com
   - Extract page title and any safe metadata you can read without interaction.

3) Append ONE log entry to:
   AI_Employee_Vault/Logs/silver_scheduler_log.md
   Include: ISO timestamp, task_id, action_id, URL, MCP server name (playwright), title/metadata summary,
   and a note: "read-only".

4) Update approval_file_path:
   - set executed: true
   - set executed_at: <ISO-8601 now>
   Do not change anything else.

Output:
- Print a short summary indicating title + executed flags set.


