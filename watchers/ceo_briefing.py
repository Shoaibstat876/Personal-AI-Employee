from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT = REPO_ROOT / "AI_Employee_Vault"

BRIEFINGS_DIR = REPO_ROOT / "Briefings"
LOGS_DIR = VAULT / "Logs"
ACTION_LOG = LOGS_DIR / "gold_action_log.jsonl"

def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

def safe_read(path: Path, limit: int = 4000) -> str:
    try:
        txt = path.read_text(encoding="utf-8-sig")
        return txt[:limit]
    except Exception as e:
        return f"(unreadable: {path.name}; {type(e).__name__})"

def main() -> int:
    BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    run_ts = now_iso()
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    out_path = BRIEFINGS_DIR / f"CEO_Briefing_{stamp}.md"

    business_goals = safe_read(REPO_ROOT / "Business_Goals.md", limit=3000)

    gold_loop_log = safe_read(VAULT / "Logs" / "gold_loop.log.md", limit=2000)
    runtime_state = safe_read(VAULT / "Logs" / "gold_runtime_state.json", limit=2000)

    # Simple local counts (no secrets)
    needs = (VAULT / "Needs_Action")
    inprog = (VAULT / "In_Progress" / "gold")
    completed = (VAULT / "Completed" / "gold")
    artifacts = (VAULT / "Artifacts" / "gold")

    def count_md(p: Path) -> int:
        if not p.exists():
            return 0
        return len([x for x in p.glob("*.md") if x.is_file()])

    stats = {
        "needs_action_md": count_md(needs),
        "in_progress_md": count_md(inprog),
        "completed_md": count_md(completed),
        "artifacts_md": count_md(artifacts),
    }

    body = (
        "# CEO Briefing — Personal AI Employee (Gold Proof)\n\n"
        f"- generated_at: {run_ts}\n"
        "- mode: local_only\n\n"
        "## Summary\n"
        "- This briefing is generated from local repo + vault state.\n"
        "- No external systems were contacted.\n\n"
        "## Current Stats (local)\n"
        + "\n".join([f"- {k}: {v}" for k, v in stats.items()])
        + "\n\n"
        "## Business Goals (snapshot)\n\n"
        f"{business_goals}\n\n"
        "## Gold Loop Log (truncated)\n\n"
        "```text\n"
        f"{gold_loop_log}\n"
        "```\n\n"
        "## Runtime State (truncated)\n\n"
        "```json\n"
        f"{runtime_state}\n"
        "```\n"
    )

    out_path.write_text(body, encoding="utf-8")

    # Append JSONL entry (append-only)
    entry = {
        "ts": run_ts,
        "event": "CEO_BRIEFING_GENERATE",
        "status": "success",
        "actor": "local_generator",
        "output_path": str(out_path),
    }
    with ACTION_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(str(out_path))
    print("JSONL_OK", str(ACTION_LOG))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
