from pathlib import Path
from datetime import datetime, timezone
import argparse
import re

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
VAULT = PROJECT / "AI_Employee_Vault"
PENDING = VAULT / "Pending_Approval"
APPROVED = VAULT / "Approved"
REJECTED = VAULT / "Rejected"
LOGS = VAULT / "Logs"

def iso_now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def latest_pending() -> Path:
    files = sorted(
        PENDING.glob("APPROVAL_*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if not files:
        raise SystemExit("STOP: no APPROVAL_*.md found in Pending_Approval")
    return files[0]

def replace_status(text: str, new_status: str) -> str:
    return re.sub(r'^status:\s*"[^"]+"', f'status: "{new_status}"', text, flags=re.MULTILINE)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision", required=True, choices=["APPROVE", "REJECT", "CLARIFY"])
    parser.add_argument("--reviewer", default="Shoaib")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    APPROVED.mkdir(parents=True, exist_ok=True)
    REJECTED.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    approval_path = latest_pending()
    text = approval_path.read_text(encoding="utf-8")

    if args.decision == "APPROVE":
        new_status = "approved"
        dest = APPROVED / approval_path.name
    elif args.decision == "REJECT":
        new_status = "rejected"
        dest = REJECTED / approval_path.name
    else:
        new_status = "clarification_requested"
        dest = REJECTED / approval_path.name

    text = replace_status(text, new_status)

    text += f"""

## Decision Record
- decision: {args.decision}
- reviewer: {args.reviewer}
- reviewed_at: {iso_now_utc()}
- notes: {args.notes}
"""

    dest.write_text(text, encoding="utf-8")
    approval_path.unlink()

    log_path = LOGS / "approval_decision_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            '{{"ts":"{}","event":"APPROVAL_DECIDED","decision":"{}","file":"{}","reviewer":"{}","status":"{}"}}\n'.format(
                iso_now_utc(), args.decision, dest.name, args.reviewer, new_status
            )
        )

    print(f"[OK] moved to: {dest}")
    print(f"[OK] decision: {args.decision}")
    print(f"[OK] status: {new_status}")

if __name__ == "__main__":
    main()
