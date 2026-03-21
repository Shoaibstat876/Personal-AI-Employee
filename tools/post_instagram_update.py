from __future__ import annotations

import argparse
import json
from datetime import datetime, UTC
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "AI_Employee_Vault"
ARTIFACTS = VAULT / "Artifacts"
LOGS = VAULT / "Logs"

def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

def utc_iso() -> str:
    return datetime.now(UTC).isoformat()

def read_input(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").strip()

def build_post(source_name: str, source_text: str, title: str | None) -> str:
    cleaned = " ".join(source_text.split())
    preview = cleaned[:700]
    heading = title.strip() if title else f"Instagram Caption — {source_name}"
    return f"""# {heading}

Building Personal AI Employee step by step.

{preview}

#AI #Automation #BuildInPublic #Python #Productivity
"""

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--status", default="ready_for_manual_post")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = (ROOT / input_path).resolve()

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    source_text = read_input(input_path)
    artifact_name = f"INSTAGRAM_POST_{utc_stamp()}.md"
    artifact_path = ARTIFACTS / artifact_name
    post_text = build_post(input_path.name, source_text, args.title)
    artifact_path.write_text(post_text, encoding="utf-8")

    with (LOGS / "instagram_execution_log.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": utc_iso(),
            "workflow": "instagram",
            "source_file": str(input_path),
            "artifact_file": str(artifact_path),
            "status": args.status,
            "content_summary": " ".join(post_text.split())[:180],
        }, ensure_ascii=False) + "\n")

    print(f"[OK] Instagram artifact created: {artifact_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
