from pathlib import Path
from datetime import datetime, timezone
import re

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
VAULT = PROJECT / "AI_Employee_Vault"
ARTIFACTS = VAULT / "Artifacts"
APPROVED = VAULT / "Approved"
LOGS = VAULT / "Logs"

def iso_now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def latest_action_artifact() -> Path:
    files = sorted(
        ARTIFACTS.glob("ACTION_APPROVAL_*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if not files:
        raise SystemExit("STOP: no ACTION_APPROVAL_*.md found in Artifacts")
    return files[0]

def latest_approved() -> Path:
    files = sorted(
        APPROVED.glob("APPROVAL_*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if not files:
        raise SystemExit("STOP: no APPROVAL_*.md found in Approved")
    return files[0]

def extract(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else ""

def main():
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    action_path = latest_action_artifact()
    approved_path = latest_approved()

    approved_text = approved_path.read_text(encoding="utf-8")
    task_id = extract(r'^task_id:\s*"([^"]+)"', approved_text)

    draft_name = f"EMAIL_DRAFT_{action_path.stem}.md"
    draft_path = ARTIFACTS / draft_name

    content = f"""---
draft_for_action_artifact: "{action_path.name}"
task_id: "{task_id}"
status: "draft_prepared"
created_at: "{iso_now_utc()}"
source: "email_draft_generator"
---

# Email Draft Artifact

## Linked Inputs
- approved_file: "{approved_path.name}"
- action_artifact_file: "{action_path.name}"

## Draft Metadata
- to: alerts@ai.shoaib.ink
- subject: Re: CEO System Report - Personal AI Employee

## Draft Body
Hello,

The system-generated CEO report has been reviewed through the HITL workflow.

Status:
- Intake completed
- Plan generated
- Human approval recorded
- Post-approval action artifact prepared

This draft is ready for final review before sending.

Regards,
Personal AI Employee

## Control Rule
This file is a draft artifact only.
No live email sending occurs at this stage.
"""

    draft_path.write_text(content, encoding="utf-8")

    log_path = LOGS / "email_draft_generator_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            '{{"ts":"{}","event":"EMAIL_DRAFT_ARTIFACT_CREATED","action_artifact":"{}","draft_file":"{}","task_id":"{}"}}\n'.format(
                iso_now_utc(), action_path.name, draft_path.name, task_id
            )
        )

    print(f"[OK] source action artifact: {action_path}")
    print(f"[OK] created email draft artifact: {draft_path}")

if __name__ == "__main__":
    main()
