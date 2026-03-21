import json
import argparse
import subprocess
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    args = parser.parse_args()

    json_path = Path(args.json)
    if not json_path.exists():
        print(f"[ERROR] JSON file not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(json_path.read_text(encoding="utf-8-sig"))

    sender = str(data.get("sender", "")).strip()
    subject = str(data.get("subject", "")).strip()

    body = str(data.get("body", "")).strip()
    if not body:
        body_lines = data.get("body_lines", [])
        if isinstance(body_lines, list):
            body = "\n".join(str(x) for x in body_lines).strip()

    if not sender or not subject or not body:
        print("[ERROR] JSON must contain sender, subject, and body or body_lines", file=sys.stderr)
        sys.exit(1)

    cmd = [
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-File", r".\scripts\create_gmail_task.ps1",
        "-Sender", sender,
        "-Subject", subject,
        "-Body", body,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
