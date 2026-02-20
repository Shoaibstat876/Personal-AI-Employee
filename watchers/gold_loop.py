from __future__ import annotations

import json
import os
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
    # Always return a state dict containing the required schema keys.
    default: Dict[str, Any] = {
        "run_id": None,
        "inflight_task_id": None,
        "inflight_step": None,
        "inflight_lock_id": None,
        "last_scan_time": None,
        "updated_at": None,
    }

    if not STATE_FILE.exists():
        return default

    raw = STATE_FILE.read_text(encoding="utf-8-sig")
    data = json.loads(raw)

    # Merge defaults so missing keys are safely added without deleting existing keys.
    if isinstance(data, dict):
        merged = {**default, **data}
        return merged

    # If file is corrupted/unexpected structure, fall back to default.
    return default


def save_state(state: Dict[str, Any]) -> None:
    state["updated_at"] = now_iso()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_once() -> int:
    # Stable RUN_ID per run_once() for crash-safe forensic + idempotent locking.
    RUN_ID = now_iso() + "|" + str(os.getpid())

    stop, reason = should_stop()
    if stop:
        append_log("STOP_REQUESTED", {"reason": reason})
        return 0

    # Crash-safe resume guard (minimal, deterministic, zero-guessing)
    prev = load_state()
    prev_step = prev.get("inflight_step")
    prev_task = prev.get("inflight_task_id")
    if prev_step and prev_task and prev_step not in ("MOVED_TO_IN_PROGRESS", "RESUME_CONFIRMED_IN_PROGRESS"):
        append_log("RESUME_DETECTED", {"prev_step": prev_step, "task": prev_task})
        in_prog = (VAULT_ROOT / "In_Progress" / "gold" / str(prev_task)).exists()
        prev["run_id"] = RUN_ID
        prev["inflight_task_id"] = prev_task
        if in_prog:
            prev["inflight_step"] = "RESUME_CONFIRMED_IN_PROGRESS"
            append_log("RESUME_OK_TASK_IN_PROGRESS", {"task": prev_task})
            save_state(prev)
        else:
            prev["inflight_step"] = "RESUME_REQUIRED_TASK_NOT_IN_PROGRESS"
            append_log("RESUME_STOP_TASK_NOT_IN_PROGRESS", {"task": prev_task})
            save_state(prev)
            return 0

    tasks = list_needs_action_tasks()

    # Idempotency guard: exclude tasks already present in In_Progress/gold
    filtered = []
    for t in tasks:
        if not (VAULT_ROOT / "In_Progress" / "gold" / t).exists():
            filtered.append(t)

    tasks = filtered
    append_log("SCAN_RESULT", {"count": len(tasks), "tasks": tasks})

    # State update after scan
    state = load_state()
    state["run_id"] = RUN_ID
    state["last_scan_time"] = now_iso()
    save_state(state)

    # Claim first task only (deterministic). Move is allowed (audit only).
    if tasks:
        task0 = tasks[0]

        # Before claim attempt: inflight mark
        state = load_state()
        state["run_id"] = RUN_ID
        state["inflight_task_id"] = task0
        state["inflight_step"] = "CLAIM_ATTEMPT"
        state["inflight_lock_id"] = None
        save_state(state)

        append_log("CLAIM_ATTEMPT", {"task": task0})

        # Use stable RUN_ID as lock_id (not time-based per attempt)
        res = try_acquire_lock(task0, lock_id=RUN_ID)

        append_log(
            "CLAIM_RESULT",
            {
                "task": task0,
                "acquired": res.acquired,
                "reason": res.reason,
                "lock_path": res.lock_path,
            },
        )

        # After claim result: write inflight lock + step
        state = load_state()
        state["run_id"] = RUN_ID
        state["inflight_task_id"] = task0
        state["inflight_step"] = "CLAIM_RESULT"
        state["inflight_lock_id"] = RUN_ID if res.acquired else None
        save_state(state)

        # Move claimed task into In_Progress/gold (no execution; audit only)
        if res.acquired:
            src_path = VAULT_ROOT / "Needs_Action" / task0
            dst_path = VAULT_ROOT / "In_Progress" / "gold" / task0

            # Before move attempt
            state = load_state()
            state["run_id"] = RUN_ID
            state["inflight_task_id"] = task0
            state["inflight_step"] = "MOVE_ATTEMPT"
            save_state(state)

            append_log("TASK_MOVE_ATTEMPT", {"task": task0, "from": str(src_path), "to": str(dst_path)})

            if dst_path.exists():
                append_log("TASK_MOVE_SKIPPED_ALREADY_IN_PROGRESS", {"task": task0})
                # Forensic step marker (safe variant)
                state = load_state()
                state["run_id"] = RUN_ID
                state["inflight_task_id"] = task0
                state["inflight_step"] = "MOVE_SKIPPED_ALREADY_IN_PROGRESS"
                save_state(state)

            elif not src_path.exists():
                append_log("TASK_MOVE_FAILED_SOURCE_MISSING", {"task": task0, "from": str(src_path)})
                # Forensic step marker (safe variant)
                state = load_state()
                state["run_id"] = RUN_ID
                state["inflight_task_id"] = task0
                state["inflight_step"] = "MOVE_FAILED_SOURCE_MISSING"
                save_state(state)

            else:
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    src_path.replace(dst_path)
                    append_log("TASK_MOVED_TO_IN_PROGRESS", {"task": task0, "to": str(dst_path)})

                    # After move success: required contract marker
                    state = load_state()
                    state["run_id"] = RUN_ID
                    state["inflight_task_id"] = task0
                    state["inflight_step"] = "MOVED_TO_IN_PROGRESS"
                    save_state(state)

                except Exception as e:
                    append_log("TASK_MOVE_FAILED_EXCEPTION", {"task": task0, "error": type(e).__name__})
                    # Forensic step marker (safe variant)
                    state = load_state()
                    state["run_id"] = RUN_ID
                    state["inflight_task_id"] = task0
                    state["inflight_step"] = "MOVE_FAILED_EXCEPTION"
                    save_state(state)

    append_log("CYCLE_IDLE", {"note": "scan/claim/move completed; no execution"})
    return 0


if __name__ == "__main__":
    raise SystemExit(run_once())


