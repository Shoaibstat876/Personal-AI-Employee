from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "AI_Employee_Vault"
NEEDS_ACTION = VAULT / "Needs_Action"
PLANS = VAULT / "Plans"
LOGS = VAULT / "Logs"

LOCK_SUFFIX = ".lock"
DONE_SUFFIX = ".done.marker"


def utc_iso() -> str:
    return datetime.now(UTC).isoformat()


def utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def append_log(entry: dict) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    log_path = LOGS / "ralph_wiggum_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def ensure_dirs() -> None:
    NEEDS_ACTION.mkdir(parents=True, exist_ok=True)
    PLANS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)


def eligible_task_files() -> list[Path]:
    files: list[Path] = []
    for p in sorted(NEEDS_ACTION.glob("*")):
        if not p.is_file():
            continue
        if p.name.endswith(LOCK_SUFFIX):
            continue
        if p.name.endswith(DONE_SUFFIX):
            continue
        lock_path = p.with_name(p.name + LOCK_SUFFIX)
        done_path = p.with_name(p.name + DONE_SUFFIX)
        if lock_path.exists() or done_path.exists():
            continue
        files.append(p)
    return files


def process_task(task_path: Path) -> dict:
    lock_path = task_path.with_name(task_path.name + LOCK_SUFFIX)
    done_path = task_path.with_name(task_path.name + DONE_SUFFIX)

    if lock_path.exists() or done_path.exists():
        return {
            "timestamp": utc_iso(),
            "task_file": str(task_path),
            "status": "skipped_already_processed_or_locked",
        }

    lock_path.write_text(f"locked_at={utc_iso()}\n", encoding="utf-8")

    try:
        content = task_path.read_text(encoding="utf-8", errors="replace").strip()
        plan_name = f"PLAN_{task_path.stem}_{utc_stamp()}.md"
        plan_path = PLANS / plan_name

        plan_text = f"""# Ralph Wiggum Auto-Plan

Source task:
{task_path.name}

Generated at:
{utc_iso()}

## Task Summary
{content[:2000]}

## Deterministic Next Step
- Review task content
- Generate approval artifact if required
- Continue until TASK_COMPLETE condition is satisfied

## TASK_COMPLETE
This task is considered complete for loop evidence once a plan file is generated
and a done marker is written for the source task.
"""
        plan_path.write_text(plan_text, encoding="utf-8")
        done_path.write_text(f"done_at={utc_iso()}\nplan={plan_path.name}\n", encoding="utf-8")

        return {
            "timestamp": utc_iso(),
            "task_file": str(task_path),
            "plan_file": str(plan_path),
            "done_marker": str(done_path),
            "status": "processed",
        }

    except Exception as e:
        return {
            "timestamp": utc_iso(),
            "task_file": str(task_path),
            "status": "error",
            "error": str(e),
        }

    finally:
        if lock_path.exists():
            lock_path.unlink()


def main() -> int:
    ensure_dirs()

    append_log({
        "timestamp": utc_iso(),
        "status": "loop_start",
        "queue_path": str(NEEDS_ACTION),
    })

    processed_count = 0

    while True:
        tasks = eligible_task_files()
        if not tasks:
            append_log({
                "timestamp": utc_iso(),
                "status": "queue_empty_stop",
                "processed_count": processed_count,
            })
            break

        for task in tasks:
            result = process_task(task)
            append_log(result)
            if result.get("status") == "processed":
                processed_count += 1

        time.sleep(1)

    append_log({
        "timestamp": utc_iso(),
        "status": "loop_end",
        "processed_count": processed_count,
    })

    print(f"[OK] Ralph Wiggum loop finished. Processed: {processed_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
