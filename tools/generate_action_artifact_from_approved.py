from pathlib import Path
from datetime import datetime, timezone
import re

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
VAULT = PROJECT / "AI_Employee_Vault"
APPROVED = VAULT / "Approved"
ARTIFACTS = VAULT / "Artifacts"
LOGS = VAULT / "Logs"

def iso_now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

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

    approval_path = latest_approved()
    approval_text = approval_path.read_text(encoding="utf-8")

    task_id = extract(r'^task_id:\s*"([^"]+)"', approval_text)
    plan_file = extract(r'^approval_for_plan:\s*"([^"]+)"', approval_text)

    artifact_name = f"ACTION_{approval_path.stem}.md"
    artifact_path = ARTIFACTS / artifact_name

    content = f"""---
action_for_approval: "{approval_path.name}"
task_id: "{task_id}"
status: "prepared_after_approval"
created_at: "{iso_now_utc()}"
source: "approved_action_generator"
---

# Approved Action Artifact

## Linked Approval
- approval_file: "{approval_path.name}"
- linked_plan_file: "{plan_file}"

## Execution Readiness
Human approval has been recorded.
This artifact represents the action package prepared after approval.

## Proposed Next Execution Options
- Draft/send email response
- Create Odoo record
- Post Slack update
- Create GitHub item

## Control Rule
External execution must follow the approved plan and remain auditable.

## Operator Note
This artifact proves the system reached the post-approval stage safely.
"""

    artifact_path.write_text(content, encoding="utf-8")

    log_path = LOGS / "approved_action_generator_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            '{{"ts":"{}","event":"ACTION_ARTIFACT_CREATED","approval_file":"{}","artifact_file":"{}","task_id":"{}"}}\n'.format(
                iso_now_utc(), approval_path.name, artifact_path.name, task_id
            )
        )

    print(f"[OK] source approval: {approval_path}")
    print(f"[OK] created action artifact: {artifact_path}")

if __name__ == "__main__":
    main()
