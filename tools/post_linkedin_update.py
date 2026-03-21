from __future__ import annotations

import argparse
import json
from datetime import datetime, UTC
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "AI_Employee_Vault"
ARTIFACTS = VAULT / "Artifacts"
LOGS = VAULT / "Logs"


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def utc_iso() -> str:
    return datetime.now(UTC).isoformat()


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_") or "update"


def read_input_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    return path.read_text(encoding="utf-8", errors="replace").strip()


def build_linkedin_post(source_name: str, source_text: str, title: str | None) -> str:
    cleaned = " ".join(source_text.split())
    preview = cleaned[:700].strip()
    heading = title.strip() if title else f"Project Update — {source_name}"

    post = f"""# {heading}

Excited to share a progress update from my Personal AI Employee project.

Key progress in this cycle:
- Continued building structured, file-based AI workflows
- Improved human-in-the-loop execution and approval handling
- Strengthened logging, artifacts, and operational traceability
- Focused on deterministic execution with evidence-first validation

Current update summary:
{preview}

This project is being developed with a strong focus on reliability, auditability, and practical AI operations.

#AI #Automation #Engineering #Python #MCP #Productivity #SoftwareDevelopment
"""
    return post.strip() + "\n"


def append_log(log_path: Path, entry: dict) -> None:
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate LinkedIn post artifact and execution log.")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to approved plan, summary, or source file.",
    )
    parser.add_argument(
        "--title",
        default="",
        help="Optional LinkedIn post heading.",
    )
    parser.add_argument(
        "--status",
        default="generated",
        help="Execution status to log. Example: generated / simulated_post / ready_for_manual_post",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = (ROOT / input_path).resolve()

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    source_text = read_input_file(input_path)
    source_name = input_path.name
    post_text = build_linkedin_post(source_name, source_text, args.title)

    ts = utc_stamp()
    artifact_name = f"LINKEDIN_POST_{ts}.md"
    artifact_path = ARTIFACTS / artifact_name
    artifact_path.write_text(post_text, encoding="utf-8")

    summary = " ".join(post_text.split())[:180]

    log_entry = {
        "timestamp": utc_iso(),
        "workflow": "linkedin_posting",
        "source_file": str(input_path),
        "artifact_file": str(artifact_path),
        "artifact_name": artifact_name,
        "content_summary": summary,
        "status": args.status,
    }
    append_log(LOGS / "linkedin_execution_log.jsonl", log_entry)

    print(f"[OK] LinkedIn artifact created: {artifact_path}")
    print(f"[OK] Log updated: {LOGS / 'linkedin_execution_log.jsonl'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())