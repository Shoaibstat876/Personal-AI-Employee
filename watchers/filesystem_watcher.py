import hashlib
import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
DROPBOX = PROJECT / "dropbox"
PROCESSED = DROPBOX / "_processed"

VAULT = PROJECT / "AI_Employee_Vault"
NEEDS_ACTION = VAULT / "Needs_Action"
LOGS = VAULT / "Logs"

LOG_FILE = LOGS / "watcher_filesystem_log.md"
STATE_FILE = LOGS / "filesystem_watcher_state.json"

WATCH_EXT_BLOCKLIST = {".tmp", ".part"}  # ignore partial downloads
WATCH_IGNORE_PREFIXES = {"~"}            # ignore temp names

def utc_stamp():
    # Example: 20260218T124603Z
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def iso_now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def log_line(event, msg):
    LOGS.mkdir(parents=True, exist_ok=True)
    LOG_FILE.touch(exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{iso_now_utc()} | FILE_WATCHER | {event} | {msg}\n")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        # If corrupt, do not crash the watcher; start fresh but log it.
        log_line("ERROR", "state_file_corrupt — resetting filesystem_watcher_state.json")
        return {}

def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")

def write_task(task_name: str, source_name: str, source_path: Path, archived_name: str, digest: str) -> None:
    NEEDS_ACTION.mkdir(parents=True, exist_ok=True)
    task_path = NEEDS_ACTION / task_name

    content = f"""---
type: file_drop
task_id: "drop-{utc_stamp()}"
source: "dropbox"
source_name: "{source_name}"
source_path: "{source_path}"
archived_name: "{archived_name}"
sha256: "{digest}"
status: "needs_action"
created_at: "{iso_now_utc()}"
---

## What arrived
- File: {source_name}
- SHA256: {digest}
- Archived: dropbox/_processed/{archived_name}

## Next action (manual)
- Review content
- Decide plan / approval if needed
"""
    task_path.write_text(content, encoding="utf-8")

class DropHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        src = Path(event.src_path)

        # Guard: only files directly under DROPBOX (not _processed)
        try:
            src.relative_to(DROPBOX)
        except ValueError:
            return

        if src.parent.name == "_processed":
            return

        # Ignore temp files / partial downloads
        if src.suffix.lower() in WATCH_EXT_BLOCKLIST:
            return
        if any(src.name.startswith(p) for p in WATCH_IGNORE_PREFIXES):
            return

        # Small delay to avoid reading while still being written
        time.sleep(0.2)

        if not src.exists():
            return

        try:
            PROCESSED.mkdir(parents=True, exist_ok=True)
            LOGS.mkdir(parents=True, exist_ok=True)

            digest = sha256_file(src)
            key = f"sha256:{digest}"

            state = load_state()

            stamp = utc_stamp()

            if key in state:
                # Duplicate: archive only, no new task
                archived_name = f"{stamp}_DUP_{src.name}"
                dest = PROCESSED / archived_name
                shutil.move(str(src), str(dest))
                log_line("DEDUP_SKIP", f"src={src} archived={archived_name} sha256={digest}")
                return

            # First time: create task + archive
            task_name = f"TASK_drop-{stamp}.md"
            archived_name = f"{stamp}_{src.name}"

            dest = PROCESSED / archived_name
            shutil.move(str(src), str(dest))

            write_task(task_name, src.name, src, archived_name, digest)

            state[key] = {
                "first_seen": iso_now_utc(),
                "source_name": src.name,
                "archived_name": archived_name,
                "task_file": task_name
            }
            save_state(state)

            log_line("PROCESSED", f"src={src} task={task_name} archived={archived_name} sha256={digest}")

        except Exception as e:
            log_line("ERROR", f"exception={type(e).__name__} msg={e}")

def main():
    # Guards (fail fast)
    if not DROPBOX.exists():
        raise SystemExit(f"STOP: dropbox missing: {DROPBOX}")
    PROCESSED.mkdir(parents=True, exist_ok=True)
    NEEDS_ACTION.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)

    log_line("START", f"watching={DROPBOX}")

    observer = Observer()
    observer.schedule(DropHandler(), str(DROPBOX), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
