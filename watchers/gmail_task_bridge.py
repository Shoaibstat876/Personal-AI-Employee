from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import argparse

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
VAULT = PROJECT / "AI_Employee_Vault"
NEEDS_ACTION = VAULT / "Needs_Action"
LOGS = VAULT / "Logs"

def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def iso_now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def safe_text(value: str) -> str:
    return (value or "").replace("\r\n", "\n").strip()

def make_task_id(subject: str, sender: str, body: str) -> str:
    raw = f"{subject}|{sender}|{body}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]

def write_email_task(subject: str, sender: str, body: str) -> Path:
    NEEDS_ACTION.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    subject = safe_text(subject)
    sender = safe_text(sender)
    body = safe_text(body)

    task_id = make_task_id(subject, sender, body)
    stamp = utc_stamp()
    task_name = f"TASK_EMAIL_{stamp}_{task_id}.md"
    task_path = NEEDS_ACTION / task_name

    content = f"""---
task_id: "{task_id}"
title: "Email intake: {subject}"
requested: "{iso_now_utc()}"
requested_by: "gmail_task_bridge"
priority: "medium"
status: "needs_action"
source: "gmail"
sender: "{sender}"
subject: "{subject}"
skill_reference: []
acceptance_criteria:
  - "Email intake task exists in Needs_Action/"
  - "Human review occurs before any external action"
  - "Plan or approval artifact is created if execution is needed"
---

# Email Intake

- source: gmail
- sender: "{sender}"
- subject: "{subject}"

## Body
{body}

## Required Flow
- Review email contents
- Create plan artifact if needed
- Request human approval before any external side effect
- Execute only after approval
"""

    task_path.write_text(content, encoding="utf-8")

    log_path = LOGS / "gmail_task_bridge_log.jsonl"
    event = {
        "ts": iso_now_utc(),
        "event": "EMAIL_TASK_CREATED",
        "task_file": str(task_path),
        "task_id": task_id,
        "sender": sender,
        "subject": subject,
        "source": "gmail"
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    return task_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", default="Demo email request v3")
    parser.add_argument("--sender", default="demo@example.com")
    parser.add_argument("--body", default="Please prepare a draft response and wait for approval.")
    args = parser.parse_args()

    path = write_email_task(args.subject, args.sender, args.body)
    print(f"[OK] created: {path}")

if __name__ == "__main__":
    main()
