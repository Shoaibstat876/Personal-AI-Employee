## SILVER (NON-INTERACTIVE) — SINGLE RUN

You are running scheduled NON-INTERACTIVE. Assume NO permission prompts can be granted.

Inputs:
- approval_file_path: {{APPROVAL_FILE_PATH}}
- task_id: {{TASK_ID}}
- action_id: {{ACTION_ID}}

HARD RULES:
- Proceed ONLY if approval file has: status: approved AND executed: false
- Do NOT modify any fields except:
  - executed: true
  - executed_at: "<ISO-8601 now>"
- If you cannot complete the approved request in NON-INTERACTIVE mode, DO NOT set executed=true.

TASK:
1) Read approval_file_path and confirm status=approved and executed=false. If not, print: NO_WORK_OR_NOT_APPROVED and stop.

2) Determine tool from the approval file field `requested`:
   - If `requested` contains "Context7" → use Context7 MCP (read-only) and return a short proof result (what you looked up + 1-2 key lines).
   - If `requested` contains "Playwright" → try Playwright MCP read-only ONLY if it runs without any permission prompts; otherwise print: BLOCKED_BY_PERMISSION and stop.

3) If (and only if) step 2 succeeded, edit approval_file_path and set:
   executed: true
   executed_at: "<ISO-8601 now>"
   Do not change anything else.

OUTPUT (exactly 3 lines):
RESULT: <one-line proof summary>
EXECUTED_SET: true
EXECUTED_AT: <timestamp you wrote>
