from pathlib import Path
from datetime import datetime, timezone
import re

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
VAULT = PROJECT / "AI_Employee_Vault"
NEEDS_ACTION = VAULT / "Needs_Action"
PLANS = VAULT / "Plans"
LOGS = VAULT / "Logs"

def iso_now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def latest_email_task() -> Path:
    files = sorted(
        NEEDS_ACTION.glob("TASK_EMAIL_*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if not files:
        raise SystemExit("STOP: no TASK_EMAIL_*.md found in Needs_Action")
    return files[0]

def extract(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else ""

def main():
    PLANS.mkdir(parents=True, exist_ok=True)
    (VAULT / "Pending_Approval").mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    task_path = latest_email_task()
    task_text = task_path.read_text(encoding="utf-8")

    task_id = extract(r'^task_id:\s*"([^"]+)"', task_text)
    subject = extract(r'^subject:\s*"([^"]+)"', task_text)
    sender = extract(r'^sender:\s*"([^"]+)"', task_text)

    plan_name = f"PLAN_{task_path.stem}.md"
    plan_path = PLANS / plan_name

    plan = f"""---
plan_for_task: "{task_path.name}"
task_id: "{task_id}"
status: "pending_approval"
created_at: "{iso_now_utc()}"
source: "gmail_plan_generator"
---

# Plan.md

## Source Task
- task_file: "{task_path.name}"
- sender: "{sender}"
- subject: "{subject}"

## Reasoning Summary
A new Gmail-derived task has been received and requires human review before any external action.

## Proposed Plan
1. Review the email request and confirm intent.
2. Decide whether the request needs:
   - draft email response
   - Odoo action
   - Slack update
   - GitHub action
3. Prepare the required artifact or action proposal.
4. Wait for explicit human approval.
5. Execute only after approval.

## Approval Requirement
No external side effect is allowed before human approval.

## Suggested Next Human Decision
- Approve for action
- Reject
- Request clarification
"""

    plan_path.write_text(plan, encoding="utf-8")
    pending_path = (VAULT / "Pending_Approval") / plan_name
    pending_path.write_text(plan, encoding="utf-8")

    log_path = LOGS / "gmail_plan_generator_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            '{"ts":"%s","event":"PLAN_CREATED","task_file":"%s","plan_file":"%s","task_id":"%s"}\n'
            % (iso_now_utc(), task_path.name, plan_path.name, task_id)
        )

    print(f"[OK] source task: {task_path}")
    print(f"[OK] created plan: {plan_path}")

if __name__ == "__main__":
    main()
