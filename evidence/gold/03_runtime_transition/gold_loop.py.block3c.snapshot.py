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
    default: Dict[str, Any] = {
        "run_id": None,
        "inflight_task_id": None,
        "inflight_step": None,
        "inflight_lock_id": None,
        "last_scan_time": None,
        "updated_at": None,
        "last_run_ts": None,
        "last_status": None,
        "last_checkpoint": None,
        "last_output_paths": [],
    }

    if not STATE_FILE.exists():
        return default

    raw = STATE_FILE.read_text(encoding="utf-8-sig")
    data = json.loads(raw)

    if isinstance(data, dict):
        return {**default, **data}

    return default


def save_state(state: Dict[str, Any]) -> None:
    state["updated_at"] = now_iso()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _stop_if_requested(
    *,
    run_id: str,
    where: str,
    task: str | None = None,
) -> bool:
    stop, reason = should_stop()
    if not stop:
        return False

    payload: Dict[str, Any] = {"reason": reason, "where": where}
    if task is not None:
        payload["task"] = task

    append_log("STOP_REQUESTED", payload)

    st = load_state()
    st["run_id"] = run_id
    st["inflight_step"] = "STOP_REQUESTED"
    if task is not None:
        st["inflight_task_id"] = task
    save_state(st)

    return True


def run_once() -> int:
    RUN_ID = now_iso() + "|" + str(os.getpid())

    # STOP at start
    if _stop_if_requested(run_id=RUN_ID, where="START"):
        return 0

    # Resume guard
    prev = load_state()
    prev_step = prev.get("inflight_step")
    prev_task = prev.get("inflight_task_id")

    if prev_step and prev_task and prev_step not in (
        "MOVED_TO_IN_PROGRESS",
        "RESUME_CONFIRMED_IN_PROGRESS",
        "EXECUTED_AND_MOVED_TO_COMPLETED",
        "IDLE_NO_TASKS",
    ):
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

    filtered = [t for t in tasks if not (VAULT_ROOT / "In_Progress" / "gold" / t).exists()]

    tasks = filtered

    append_log("SCAN_RESULT", {"count": len(tasks), "tasks": tasks})

    if _stop_if_requested(run_id=RUN_ID, where="AFTER_SCAN"):
        return 0

    state = load_state()
    state["run_id"] = RUN_ID
    state["last_scan_time"] = now_iso()
    state["last_run_ts"] = now_iso()
    state["last_checkpoint"] = "AFTER_SCAN"

    if not tasks:
        state["inflight_step"] = "IDLE_NO_TASKS"
        state["inflight_task_id"] = None
        state["inflight_lock_id"] = None
        state["last_status"] = "idle"
        state["last_checkpoint"] = "IDLE_NO_TASKS"
        state["last_output_paths"] = []

    save_state(state)

    if tasks:
        task0 = tasks[0]

        if _stop_if_requested(run_id=RUN_ID, where="BEFORE_CLAIM", task=task0):
            return 0

        state = load_state()
        state["run_id"] = RUN_ID
        state["inflight_task_id"] = task0
        state["inflight_step"] = "CLAIM_ATTEMPT"
        state["inflight_lock_id"] = None
        save_state(state)

        append_log("CLAIM_ATTEMPT", {"task": task0})

        if _stop_if_requested(run_id=RUN_ID, where="BEFORE_LOCK", task=task0):
            return 0

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

        # ✅ FIXED: persist actual lock_path
        state = load_state()
        state["run_id"] = RUN_ID
        state["inflight_task_id"] = task0
        state["inflight_step"] = "CLAIM_RESULT"
        state["inflight_lock_id"] = res.lock_path if res.acquired else None
        save_state(state)

        if res.acquired:
            src_path = VAULT_ROOT / "Needs_Action" / task0
            dst_path = VAULT_ROOT / "In_Progress" / "gold" / task0

            state = load_state()
            state["run_id"] = RUN_ID
            state["inflight_task_id"] = task0
            state["inflight_step"] = "MOVE_ATTEMPT"
            save_state(state)

            if _stop_if_requested(run_id=RUN_ID, where="BEFORE_MOVE", task=task0):
                return 0

            append_log(
                "TASK_MOVE_ATTEMPT",
                {"task": task0, "from": str(src_path), "to": str(dst_path)},
            )

            if dst_path.exists():
                append_log(
                    "TASK_MOVE_SKIPPED_ALREADY_IN_PROGRESS",
                    {"task": task0},
                )
                state = load_state()
                state["run_id"] = RUN_ID
                state["inflight_task_id"] = task0
                state["inflight_step"] = "MOVE_SKIPPED_ALREADY_IN_PROGRESS"
                save_state(state)

            elif not src_path.exists():
                append_log(
                    "TASK_MOVE_FAILED_SOURCE_MISSING",
                    {"task": task0, "from": str(src_path)},
                )
                state = load_state()
                state["run_id"] = RUN_ID
                state["inflight_task_id"] = task0
                state["inflight_step"] = "MOVE_FAILED_SOURCE_MISSING"
                save_state(state)

            else:
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    src_path.replace(dst_path)
                    append_log(
                        "TASK_MOVED_TO_IN_PROGRESS",
                        {"task": task0, "to": str(dst_path)},
                    )

                    state = load_state()
                    state["run_id"] = RUN_ID
                    state["inflight_task_id"] = task0
                    state["inflight_step"] = "MOVED_TO_IN_PROGRESS"
                    state["last_status"] = "moved_to_in_progress"
                    state["last_checkpoint"] = "MOVED_TO_IN_PROGRESS"
                    state["last_output_paths"] = [str(dst_path)]
                    save_state(state)

                    # ---- Phase 6: SAFE local-only execution (DEMO tasks only) ----
                    if str(task0).startswith("DEMO_EXEC_"):
                        try:
                            inprog_path = VAULT_ROOT / "In_Progress" / "gold" / task0
                            completed_dir = VAULT_ROOT / "Completed" / "gold"
                            artifacts_dir = VAULT_ROOT / "Artifacts" / "gold"

                            completed_dir.mkdir(parents=True, exist_ok=True)
                            artifacts_dir.mkdir(parents=True, exist_ok=True)

                            append_log(
                                "EXECUTION_ATTEMPT",
                                {"task": task0, "mode": "local_filesystem"},
                            )

                            # Read task content (local only)
                            try:
                                task_text = inprog_path.read_text(encoding="utf-8")
                            except Exception:
                                task_text = (
                                    "(could not read task content as utf-8; continuing safely)"
                                )

                            # Create a real artifact file
                            safe_name = Path(task0).stem  # remove .md
                            artifact_path = artifacts_dir / f"artifact.{safe_name}.result.md"

                            artifact_body = (
                                f"# Gold Phase 6 Artifact\n\n"
                                f"- task: {task0}\n"
                                f"- created_at: {now_iso()}\n"
                                f"- mode: local_filesystem\n\n"
                                f"## Task content snapshot\n\n"
                                f"{task_text}\n"
                            )

                            artifact_path.write_text(artifact_body, encoding="utf-8")

                            append_log(
                                "EXECUTION_RESULT",
                                {
                                    "task": task0,
                                    "artifact": str(artifact_path),
                                    "result": "ok",
                                },
                            )

                            # Move task to Completed (still local only)
                            completed_path = completed_dir / task0
                            inprog_path.replace(completed_path)

                            state = load_state()
                            state["run_id"] = RUN_ID
                            state["inflight_task_id"] = task0
                            state["inflight_step"] = "EXECUTED_AND_MOVED_TO_COMPLETED"
                            state["last_status"] = "executed_and_completed"
                            state["last_checkpoint"] = "EXECUTED_AND_MOVED_TO_COMPLETED"
                            state["last_output_paths"] = [str(artifact_path), str(completed_path)]
                            save_state(state)

                            append_log(
                                "TASK_MOVED_TO_COMPLETED",
                                {"task": task0, "to": str(completed_path)},
                            )

                        except Exception as e:
                            append_log(
                                "EXECUTION_FAILED_EXCEPTION",
                                {"task": task0, "error": str(e)},
                            )
                            state = load_state()
                            state["run_id"] = RUN_ID
                            state["inflight_task_id"] = task0
                            state["inflight_step"] = "EXECUTION_FAILED_EXCEPTION"
                            save_state(state)
                    # ---- end Phase 6 block ----

                except Exception as e:
                    append_log(
                        "TASK_MOVE_FAILED_EXCEPTION",
                        {"task": task0, "error": type(e).__name__},
                    )
                    state = load_state()
                    state["run_id"] = RUN_ID
                    state["inflight_task_id"] = task0
                    state["inflight_step"] = "MOVE_FAILED_EXCEPTION"
                    save_state(state)

    append_log("CYCLE_IDLE", {"note": "scan/claim/move completed; no execution"})
    return 0


if __name__ == "__main__":
    raise SystemExit(run_once())