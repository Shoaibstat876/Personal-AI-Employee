"""
Personal AI Employee — Hackathon 0

This file implements controlled email sending from an approved draft artifact.

Relevant `.specify` alignment:
- workflow definition
- HITL governance
- execution boundaries
- evidence traceability

This stage performs real external email delivery only after prior approval and must preserve auditability and idempotency.
"""

import os
import re
from pathlib import Path
from datetime import datetime, timezone

import resend
from dotenv import load_dotenv

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
VAULT = PROJECT / "AI_Employee_Vault"
ARTIFACTS = VAULT / "Artifacts"
LOGS = VAULT / "Logs"

def iso_now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def latest_email_draft_artifact() -> Path:
    files = sorted(
        ARTIFACTS.glob("EMAIL_DRAFT_ACTION_APPROVAL_*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if not files:
        raise SystemExit("STOP: no EMAIL_DRAFT_ACTION_APPROVAL_*.md found in Artifacts")
    return files[0]

def extract(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else ""

def extract_body(text: str) -> str:
    marker = "## Draft Body"
    end_marker = "## Control Rule"
    if marker not in text:
        return ""
    part = text.split(marker, 1)[1]
    if end_marker in part:
        part = part.split(end_marker, 1)[0]
    return part.strip()

def already_sent(text: str) -> bool:
    return 'status: "sent"' in text or "## Send Record" in text

def update_status(text: str, new_status: str) -> str:
    return re.sub(r'^status:\s*"[^"]+"', f'status: "{new_status}"', text, flags=re.MULTILINE)

def append_send_record(text: str, to_email: str, subject: str, result: str) -> str:
    return text + f"""

## Send Record
- sent_at: {iso_now_utc()}
- to: {to_email}
- subject: {subject}
- delivery_result: {result}
"""

def log_event(event_name: str, draft_file: str, to_email: str, subject: str, result: str) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    log_path = LOGS / "draft_execution_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            '{{"ts":"{}","event":"{}","draft_file":"{}","to":"{}","subject":"{}","result":"{}"}}\n'.format(
                iso_now_utc(),
                event_name,
                draft_file,
                to_email,
                subject,
                result.replace('"', "'")
            )
        )

def main():
    load_dotenv()
    resend.api_key = os.getenv("RESEND_API_KEY")

    from_email = os.getenv("FROM_EMAIL")
    if not from_email:
        raise SystemExit("STOP: FROM_EMAIL missing in .env")

    LOGS.mkdir(parents=True, exist_ok=True)

    # Select the latest prepared email draft artifact from the post-approval execution stage.
    draft_path = latest_email_draft_artifact()
    draft_text = draft_path.read_text(encoding="utf-8")

    to_email = extract(r'^\- to:\s*(.+)$', draft_text)
    subject = extract(r'^\- subject:\s*(.+)$', draft_text)
    body = extract_body(draft_text)

    if not to_email or not subject or not body:
        raise SystemExit("STOP: could not extract to/subject/body from draft artifact")

    # Idempotency guard prevents duplicate email sending for the same approved draft artifact.
    if already_sent(draft_text):
        msg = "already_sent_idempotency_guard"
        log_event("SKIP_ALREADY_SENT", draft_path.name, to_email, subject, msg)
        print(f"[SKIP] draft already sent: {draft_path}")
        print(f"[SKIP] to: {to_email}")
        print(f"[SKIP] subject: {subject}")
        return

    html = "<br>".join(body.splitlines())

    # Construct a controlled send payload from the approved draft artifact without changing its intent.
    params = {
        "from": from_email,
        "to": [to_email],
        "subject": subject,
        "html": html,
    }

    result = resend.Emails.send(params)
    result_text = str(result)

    updated = update_status(draft_text, "sent")
    updated = append_send_record(updated, to_email, subject, result_text)
    draft_path.write_text(updated, encoding="utf-8")

    # Append-only execution logging preserves delivery traceability for audit and review.
    log_event("EMAIL_DRAFT_SENT", draft_path.name, to_email, subject, result_text)

    print(f"[OK] source draft artifact: {draft_path}")
    print(f"[OK] sent to: {to_email}")
    print(f"[OK] subject: {subject}")
    print(result)

if __name__ == "__main__":
    main()
