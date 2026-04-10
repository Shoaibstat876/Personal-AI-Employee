"""
Personal AI Employee — Hackathon 0

This file implements the Plan → Approval stage of the governed workflow.

Relevant `.specify` alignment:
- workflow definition
- HITL governance
- execution boundaries
- evidence traceability

This stage creates an explicit human decision artifact and must not execute actions directly.
"""

from pathlib import Path
from datetime import datetime, timezone
import re

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
VAULT = PROJECT / "AI_Employee_Vault"
PLANS = VAULT / "Plans"
PENDING = VAULT / "Pending_Approval"
LOGS = VAULT / "Logs"

def iso_now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def latest_plan() -> Path:
    files = sorted(
        PLANS.glob("PLAN_TASK_EMAIL_*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if not files:
        raise SystemExit("STOP: no PLAN_TASK_EMAIL_*.md found in Plans")
    return files[0]

def extract(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else ""

def main():
    PENDING.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    # Select the latest generated plan so approval remains a visible, explicit workflow stage.
    plan_path = latest_plan()
    plan_text = plan_path.read_text(encoding="utf-8")

    # Preserve task_id continuity so the approval artifact stays linked to the same workflow item.
    task_id = extract(r'^task_id:\s*"([^"]+)"', plan_text)
    approval_name = f"APPROVAL_{plan_path.stem}.md"
    approval_path = PENDING / approval_name

    content = f"""---
approval_for_plan: "{plan_path.name}"
task_id: "{task_id}"
status: "awaiting_human_decision"
created_at: "{iso_now_utc()}"
source: "approval_generator"
---

# Approval Request

## Linked Plan
- plan_file: "{plan_path.name}"

## Human Decision Required
Choose exactly one:
- APPROVE
- REJECT
- CLARIFY

## Control Rule
No external side effect is allowed until human approval is recorded.

## Reviewer Notes
- decision:
- reviewer:
- reviewed_at:
- notes:
"""

    # Write the approval request into Pending_Approval without triggering any external execution.
    approval_path.write_text(content, encoding="utf-8")

    # Append-only logging preserves reviewability and audit trace for approval creation.
    log_path = LOGS / "approval_generator_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            '{{"ts":"{}","event":"APPROVAL_CREATED","plan_file":"{}","approval_file":"{}","task_id":"{}"}}\n'.format(
                iso_now_utc(), plan_path.name, approval_path.name, task_id
            )
        )

    print(f"[OK] source plan: {plan_path}")
    print(f"[OK] created approval: {approval_path}")

if __name__ == "__main__":
    main()
