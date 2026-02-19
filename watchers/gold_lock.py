from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT_ROOT = REPO_ROOT / "AI_Employee_Vault"
LOCK_DIR = VAULT_ROOT / "In_Progress" / "gold"

STALE_DIR = VAULT_ROOT / "Logs" / "stale_locks"

TTL_SECONDS = 1800  # 30 minutes


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


@dataclass(frozen=True)
class LockResult:
    acquired: bool
    reason: str
    lock_path: str


def parse_iso(ts: str) -> datetime | None:
    try:
        # Python 3.11+ supports fromisoformat with offset
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def lock_age_seconds(lock_data: Dict[str, Any]) -> int | None:
    ts = lock_data.get("created_at")
    if not isinstance(ts, str):
        return None
    dt = parse_iso(ts)
    if dt is None:
        return None
    # Ensure tz-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    age = datetime.now(timezone.utc).astimezone() - dt
    return int(age.total_seconds())


def is_lock_stale(lock_data: Dict[str, Any]) -> bool:
    age = lock_age_seconds(lock_data)
    if age is None:
        # Unknown age => treat as stale for safety
        return True
    return age > TTL_SECONDS


def lock_path_for(task_name: str) -> Path:
    # task_name is a filename like TASK_xxx.md
    safe = task_name.replace("/", "_").replace("\\", "_")
    return LOCK_DIR / f"{safe}.lock.json"


def try_acquire_lock(task_name: str, lock_id: str) -> LockResult:
    """
    Attempt to acquire an exclusive lock for a task by creating the lock file.
    Deterministic: lock path derived from task filename.

    Returns:
      acquired=True if lock was created
      acquired=False if lock already exists or on error
    """
    LOCK_DIR.mkdir(parents=True, exist_ok=True)
    path = lock_path_for(task_name)

    payload: Dict[str, Any] = {
        "task_name": task_name,
        "lock_id": lock_id,
        "created_at": now_iso(),
        "executor_host": os.environ.get("COMPUTERNAME", ""),
        "executor_pid": os.getpid(),
    }

    try:
        # Exclusive create: fails if file exists.
        with path.open("x", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
        return LockResult(True, "LOCK_ACQUIRED", str(path))
    except FileExistsError:
        exists, data, _ = read_lock(task_name)
        if exists and is_lock_stale(data):
            # Move stale lock aside (audit) then retry once.
            STALE_DIR.mkdir(parents=True, exist_ok=True)
            stale_name = path.name.replace(".lock.json", f".stale.{lock_id}.lock.json")
            stale_path = STALE_DIR / stale_name
            try:
                path.replace(stale_path)
            except Exception:
                # If we cannot move it, do not proceed.
                return LockResult(False, "LOCK_STALE_MOVE_FAILED", str(path))

            try:
                with path.open("x", encoding="utf-8") as f:
                    json.dump(payload, f, ensure_ascii=False, indent=2)
                    f.write("\n")
                return LockResult(True, "LOCK_ACQUIRED_STALE_RECOVERED", str(path))
            except FileExistsError:
                return LockResult(False, "LOCK_EXISTS_AFTER_STALE_MOVE", str(path))
            except Exception as e:
                return LockResult(False, f"LOCK_ERROR:{type(e).__name__}", str(path))

        return LockResult(False, "LOCK_EXISTS", str(path))
    except Exception as e:
        return LockResult(False, f"LOCK_ERROR:{type(e).__name__}", str(path))


def read_lock(task_name: str) -> Tuple[bool, Dict[str, Any], str]:
    """
    Read existing lock file if present.
    Returns: (exists, data, path)
    """
    path = lock_path_for(task_name)
    if not path.exists():
        return False, {}, str(path)
    raw = path.read_text(encoding="utf-8-sig")
    return True, json.loads(raw), str(path)


if __name__ == "__main__":
    # Manual test: python watchers/gold_lock.py TASK_x.md
    import sys
    task = sys.argv[1] if len(sys.argv) > 1 else "TASK_TEST.md"
    res = try_acquire_lock(task, lock_id="TEST_LOCK")
    print(json.dumps(res.__dict__, ensure_ascii=False))


