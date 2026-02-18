# FILESYSTEM WATCHER — DEDUP CONTRACT (v1)
Date: 2026-02-18T18:01:54

## Goal
Prevent duplicate task creation if the same file content is dropped multiple times.

## Dedup Key
- dedup_key = SHA256(file_bytes)
- If dedup_key already exists in state index, it is a duplicate.

## State Index
- File: AI_Employee_Vault/Logs/filesystem_watcher_state.json
- Structure:
  {
    "sha256:<hash>": {
      "first_seen": "<ISO>",
      "source_name": "<original filename>",
      "archived_name": "<archived filename>",
      "task_file": "<task md filename>"
    }
  }

## Processing Rules
When a new file is created in dropbox/:
1) Compute SHA256.
2) If hash NOT seen:
   - Create a Needs_Action task file with deterministic naming:
     TASK_drop-<UTCSTAMP>.md
   - Archive original file into dropbox/_processed/:
     <UTCSTAMP>_<originalname>
   - Log: PROCESSED
   - Write state index entry.
3) If hash already seen:
   - Archive into dropbox/_processed/:
     <UTCSTAMP>_DUP_<originalname>
   - Do NOT create new task.
   - Log: DEDUP_SKIP

## Logging
Append-only log file:
AI_Employee_Vault/Logs/watcher_filesystem_log.md

Allowed event labels:
- START
- PROCESSED
- DEDUP_SKIP
- ERROR

## Boundaries
- Watcher only creates tasks and archives files.
- No approvals, no MCP, no Claude invocation, no execution.
