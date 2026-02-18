import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
VAULT = PROJECT / "AI_Employee_Vault"

REQUIRED_FOLDERS = [
    "Inbox",
    "Needs_Action",
    "Plans",
    "In_Progress",
    "Pending_Approval",
    "Approved",
    "Rejected",
    "Done",
    "Logs",
    "Decisions"
]

LOG_FILE = VAULT / "Logs" / "watcher_vault_health_log.md"

def iso_now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def log_line(event, msg):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.touch(exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{iso_now_utc()} | VAULT_HEALTH_WATCHER | {event} | {msg}\n")

def write_task_missing(missing):
    needs = VAULT / "Needs_Action"
    needs.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    task = needs / f"TASK_vault-health-{stamp}.md"

    task.write_text(f"""---
type: vault_health
created_at: "{iso_now_utc()}"
status: "needs_action"
---

## Missing vault folders detected
{chr(10).join([f"- {m}" for m in missing])}

## Required action (manual)
Create missing folders to restore vault contract.
""", encoding="utf-8")

    log_line("TASK_CREATED", f"missing={missing} task={task.name}")

def main():
    log_line("START", f"vault={VAULT}")

    while True:
        missing = []
        for name in REQUIRED_FOLDERS:
            p = VAULT / name
            if not p.exists():
                missing.append(str(p))

        if missing:
            log_line("FAIL", f"missing_count={len(missing)}")
            write_task_missing(missing)
        else:
            log_line("PASS", "all_required_folders_present")

        time.sleep(60)

if __name__ == "__main__":
    main()
