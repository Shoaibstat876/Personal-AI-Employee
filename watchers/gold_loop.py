from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from gold_stop_hook import should_stop
from gold_scan import list_needs_action_tasks
from gold_lock import try_acquire_lock


REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT_ROOT = REPO_ROOT / "AI_Employee_Vault"
LOG_FILE = VAULT_ROOT / "Logs" / "gold_loop.log.md"
STATE_FILE = VAULT_ROOT / "Logs" / "gold_runtime_state.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def append_log(event: str, details: Dict[str, Any] | None = None) -> None:
    details = details or {}
    line = f"- {now_iso()} | {event} | {json.dumps(details, ensure_ascii=False)}"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_state() -> Dict[str, Any]:
    if not STATE_FILE.exists():
        return {
            "inflight_task_id": None,
            "inflight_step": None,
            "inflight_lock_id": None,
            "last_scan_time": None,
            "updated_at": None,
        }
    raw = STATE_FILE.read_text(encoding="utf-8-sig")
    return json.loads(raw)


def save_state(state: Dict[str, Any]) -> None:
    state["updated_at"] = now_iso()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_once() -> int:
    stop, reason = should_stop()
    if stop:
        append_log("STOP_REQUESTED", {"reason": reason})
        return 0

    tasks = list_needs_action_tasks()
    append_log("SCAN_RESULT", {"count": len(tasks), "tasks": tasks})

    # Claim first task only (deterministic). No moves. No execution.
    if tasks:
        task0 = tasks[0]
        append_log("CLAIM_ATTEMPT", {"task": task0})
        res = try_acquire_lock(task0, lock_id=now_iso())
        if res.acquired:
            append_log("CLAIM_ACQUIRED", {"task": task0, "lock_path": res.lock_path})
        else:
            append_log("CLAIM_SKIPPED_LOCK_EXISTS", {"task": task0, "reason": res.reason, "lock_path": res.lock_path})

    state = load_state()
    state["last_scan_time"] = now_iso()
    save_state(state)

    append_log("CYCLE_IDLE", {"note": "claim integrated; no moves/execution"})
    return 0


if __name__ == "__main__":
    raise SystemExit(run_once())


