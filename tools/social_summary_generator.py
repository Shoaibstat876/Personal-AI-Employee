from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "AI_Employee_Vault"
ARTIFACTS = VAULT / "Artifacts"
LOGS = VAULT / "Logs"

PATTERNS = ("FACEBOOK_POST_", "INSTAGRAM_POST_", "TWITTER_POST_")


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def utc_iso() -> str:
    return datetime.now(UTC).isoformat()


def collect_social_posts() -> list[Path]:
    posts: list[Path] = []
    for p in ARTIFACTS.glob("*.md"):
        if any(p.name.startswith(prefix) for prefix in PATTERNS):
            posts.append(p)
    return sorted(posts, key=lambda x: x.stat().st_mtime, reverse=True)


def main() -> int:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    posts = collect_social_posts()
    if not posts:
        print("[ERROR] No social post artifacts found.")
        return 1

    sections: list[str] = []
    for post in posts[:20]:
        text = post.read_text(encoding="utf-8", errors="replace").strip()
        preview = " ".join(text.split())[:300]
        sections.append(f"## {post.name}\n{preview}\n")

    summary_text = f"""# Social Summary

Generated at:
{utc_iso()}

## Summary
This file summarizes generated social posting artifacts across Facebook, Instagram, and Twitter/X.

## Total Artifacts
{len(posts)}

## Content Overview
""" + "\n".join(sections)

    artifact_name = f"SOCIAL_SUMMARY_{utc_stamp()}.md"
    artifact_path = ARTIFACTS / artifact_name
    artifact_path.write_text(summary_text, encoding="utf-8")

    log_entry = {
        "timestamp": utc_iso(),
        "workflow": "social_summary",
        "artifact_file": str(artifact_path),
        "artifact_name": artifact_name,
        "total_social_artifacts": len(posts),
        "status": "generated",
    }

    with (LOGS / "social_summary_log.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    print(f"[OK] Social summary created: {artifact_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
