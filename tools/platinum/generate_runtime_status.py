from pathlib import Path
from datetime import datetime, timezone

# -------------------------
# PATH SETUP
# -------------------------

ROOT = Path(__file__).resolve().parents[2]
VAULT = ROOT / "AI_Employee_Vault"

INCOMING = VAULT / "Updates" / "Incoming"
CLAIMED = VAULT / "Updates" / "Claimed"
PROCESSED = VAULT / "Updates" / "Processed"
NEEDS_ACTION = VAULT / "Needs_Action"
DONE = VAULT / "Done"

OUTPUT = VAULT / "Updates" / "PLATINUM_RUNTIME_STATUS.md"


# -------------------------
# TIME HELPERS (UTC SAFE)
# -------------------------

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def file_mtime_iso(path: Path) -> str:
    try:
        return datetime.fromtimestamp(
            path.stat().st_mtime,
            tz=timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return "UNKNOWN"


# -------------------------
# COUNT HELPERS (SAFE)
# -------------------------

def count_md_files(path: Path) -> int:
    if not path.exists() or not path.is_dir():
        return 0
    return len([p for p in path.glob("*.md") if p.is_file()])


def count_all_files(path: Path) -> int:
    if not path.exists() or not path.is_dir():
        return 0
    return len([p for p in path.iterdir() if p.is_file()])


# -------------------------
# LATEST FILE HELPERS
# -------------------------

def get_latest_file(path: Path, pattern: str = "*") -> tuple[str, str]:
    if not path.exists() or not path.is_dir():
        return "NONE", "NONE"

    files = [p for p in path.glob(pattern) if p.is_file()]
    if not files:
        return "NONE", "NONE"

    try:
        latest = max(files, key=lambda f: f.stat().st_mtime)
        return latest.name, file_mtime_iso(latest)
    except Exception:
        return "ERROR", "ERROR"


# -------------------------
# OPTIONAL: GOLD BRIDGE CHECK (kept for audit safety)
# -------------------------

def count_gold_bridged() -> int:
    if not PROCESSED.exists() or not PROCESSED.is_dir():
        return 0

    count = 0
    for file_path in PROCESSED.glob("*.md"):
        if not file_path.is_file():
            continue

        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore").lower()
            if "gold_bridge_created: true" in text:
                count += 1
        except Exception:
            continue

    return count


# -------------------------
# MAIN GENERATOR
# -------------------------

def main() -> None:
    # Counts
    incoming = count_md_files(INCOMING)
    claimed = count_md_files(CLAIMED)
    processed = count_md_files(PROCESSED)
    needs_action = count_md_files(NEEDS_ACTION)
    done = count_all_files(DONE)

    # Latest activity
    latest_processed_name, latest_processed_time = get_latest_file(PROCESSED, "*.md")
    latest_done_name, latest_done_time = get_latest_file(DONE, "*")

    # Timestamp
    last_updated = utc_now_iso()

    # FINAL OUTPUT (STRICT FORMAT — DO NOT CHANGE)
    content = f"""# PLATINUM RUNTIME STATUS (LIVE)

Last Updated: {last_updated}

## Update Queue
Incoming: {incoming}
Claimed: {claimed}
Processed: {processed}

## System State
Needs_Action: {needs_action}
Done: {done}

## Latest Activity
Latest Processed: {latest_processed_name} | {latest_processed_time}
Latest Done: {latest_done_name} | {latest_done_time}

Status: LIVE_SYNCED
"""

    OUTPUT.write_text(content, encoding="utf-8")
    print("UPDATED:", OUTPUT)


# -------------------------
# ENTRY POINT
# -------------------------

if __name__ == "__main__":
    main()