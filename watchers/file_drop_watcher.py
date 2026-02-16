import os
import time
import shutil
import hashlib
from pathlib import Path

# ====== CONFIG (Bronze Perception Only) ======
PROJECT_ROOT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
DROPBOX_DIR = PROJECT_ROOT / "dropbox"
PROCESSED_DIR = DROPBOX_DIR / "_processed"

VAULT_ROOT = PROJECT_ROOT / "AI_Employee_Vault"
INBOX_DIR = VAULT_ROOT / "Inbox"
NEEDS_ACTION_DIR = VAULT_ROOT / "Needs_Action"

POLL_SECONDS = 2
STABLE_CHECKS = 3
STABLE_INTERVAL = 1.0
# ============================================

def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def deterministic_task_id(path: Path) -> str:
    # Deterministic ID derived from file content
    return sha256_file(path)[:16]

def wait_for_stable_size(path: Path) -> bool:
    try:
        last = path.stat().st_size
    except FileNotFoundError:
        return False

    stable = 0
    while stable < STABLE_CHECKS:
        time.sleep(STABLE_INTERVAL)
        try:
            now = path.stat().st_size
        except FileNotFoundError:
            return False

        if now == last:
            stable += 1
        else:
            stable = 0
            last = now
    return True

def atomic_write_text(dest: Path, text: str) -> None:
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, dest)

def safe_copy_to_inbox(src: Path, inbox_dir: Path, task_id: str) -> Path:
    dest = inbox_dir / src.name
    if dest.exists():
        dest = inbox_dir / f"{src.stem}__{task_id}{src.suffix}"
    shutil.copy2(src, dest)
    return dest

def move_to_processed(src: Path, processed_dir: Path, task_id: str) -> Path:
    dest = processed_dir / src.name
    if dest.exists():
        dest = processed_dir / f"{src.stem}__{task_id}{src.suffix}"
    shutil.move(str(src), str(dest))
    return dest

def make_task_md(task_id: str, original_filename: str) -> str:
    created = time.strftime("%Y-%m-%dT%H:%M:%S")
    return f"""---
task_id: "{task_id}"
title: "Ingested file: {original_filename}"
requested: "{created}"
requested_by: "dropbox_watcher"
priority: "medium"
status: "needs_action"
skill_reference: []
acceptance_criteria:
  - "Original file stored in Inbox/"
  - "TASK file exists in Needs_Action/"
---

# Ingested Input
- source: dropbox/
- original_filename: "{original_filename}"
"""

def process_one_file(f: Path):
    if f.is_dir() or f.name == "_processed":
        return

    if not wait_for_stable_size(f):
        return

    task_id = deterministic_task_id(f)
    task_file = NEEDS_ACTION_DIR / f"TASK_FILE_{task_id}.md"

    # Dedup protection
    if task_file.exists():
        print(f"[DEDUP] TASK exists for task_id={task_id}. Moving file to _processed.")
        move_to_processed(f, PROCESSED_DIR, task_id)
        return

    copied_path = safe_copy_to_inbox(f, INBOX_DIR, task_id)
    md = make_task_md(task_id, copied_path.name)
    atomic_write_text(task_file, md)
    moved_path = move_to_processed(f, PROCESSED_DIR, task_id)

    print(f"[OK] task_id={task_id}")
    print(f"     inbox: {copied_path}")
    print(f"     task : {task_file}")
    print(f"     moved: {moved_path}")

def main() -> None:
    for p in [DROPBOX_DIR, PROCESSED_DIR, VAULT_ROOT, INBOX_DIR, NEEDS_ACTION_DIR]:
        if not p.exists():
            raise SystemExit(f"STOP: required path missing: {p}")

    print("Bronze Perception Watcher (polling)")
    print(f"dropbox  : {DROPBOX_DIR}")
    print(f"processed: {PROCESSED_DIR}")
    print(f"inbox    : {INBOX_DIR}")
    print(f"needs    : {NEEDS_ACTION_DIR}")
    print("CTRL+C to stop.\n")

    while True:
        try:
            for item in DROPBOX_DIR.iterdir():
                if item.name == "_processed":
                    continue
                process_one_file(item)
            time.sleep(POLL_SECONDS)
        except KeyboardInterrupt:
            print("\nSTOP: watcher terminated by user.")
            return
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()
