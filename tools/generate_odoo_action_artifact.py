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

    approved_path = latest_approved()
    approved_text = approved_path.read_text(encoding="utf-8")
    task_id = extract(r'^task_id:\s*"([^"]+)"', approved_text)

    artifact_name = f"ODOO_ACTION_{approved_path.stem}.md"
    artifact_path = ARTIFACTS / artifact_name

    content = f"""---
odoo_action_for_approval: "{approved_path.name}"
task_id: "{task_id}"
status: "prepared_after_approval"
created_at: "{iso_now_utc()}"
source: "odoo_action_generator"
execution_target: "odoo"
risk_level: "high"
approval_policy: "strict_hitl"
---

# Odoo Action Artifact

## Linked Approval
- approval_file: "{approved_path.name}"

## Proposed Odoo Action
- action_type: create_customer
- customer_name: HITL Demo Customer
- customer_email: hitl.demo.customer@example.com
- customer_phone: +92-300-0000000

## Control Rule
No Odoo write action is allowed without prior approval.

## Operator Note
This artifact proves the system prepared a real Odoo-side business action after HITL approval.
"""
    artifact_path.write_text(content, encoding="utf-8")

    log_path = LOGS / "odoo_action_generator_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            '{{"ts":"{}","event":"ODOO_ACTION_ARTIFACT_CREATED","approval_file":"{}","artifact_file":"{}","task_id":"{}"}}\n'.format(
                iso_now_utc(), approved_path.name, artifact_path.name, task_id
            )
        )

    print(f"[OK] source approval: {approved_path}")
    print(f"[OK] created Odoo action artifact: {artifact_path}")

if __name__ == "__main__":
    main()
