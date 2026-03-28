import sys
import re
from pathlib import Path
from shutil import move
from datetime import datetime, UTC

ROOT = Path.cwd()
VAULT = ROOT / "AI_Employee_Vault"
UPDATES = VAULT / "Updates"
INCOMING = UPDATES / "Incoming"
CLAIMED = UPDATES / "Claimed"
PROCESSED = UPDATES / "Processed"
NEEDS = VAULT / "Needs_Action"
LOGS = VAULT / "Logs"
LOG_FILE = LOGS / "platinum_update_log.md"

def now():
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

def log(line):
    LOGS.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def extract_field(text, field):
    m = re.search(rf"^{re.escape(field)}:\s*(.+)$", text, re.MULTILINE)
    if not m:
        return ""
    value = m.group(1).strip()
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    return value

def replace_field(content, field, new_value):
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(f"{field}:"):
            lines[i] = f"{field}: {new_value}"
            return "\n".join(lines)
    return "\n".join(lines)

def claim(name):
    src = INCOMING / name
    dst = CLAIMED / name
    if not src.exists():
        print(f"MISSING: {src}")
        return
    CLAIMED.mkdir(parents=True, exist_ok=True)
    move(str(src), str(dst))
    log(f"{now()} | CLAIM | {name} | moved to Claimed")
    print(f"CLAIMED: {dst}")

def review(name, decision):
    src = CLAIMED / name
    if not src.exists():
        print(f"MISSING: {src}")
        return

    PROCESSED.mkdir(parents=True, exist_ok=True)
    NEEDS.mkdir(parents=True, exist_ok=True)

    processed = PROCESSED / name
    text = src.read_text(encoding="utf-8")

    update_id = extract_field(text, "update_id") or Path(name).stem
    task_type = extract_field(text, "task_type")

    def replace_status(content, new_status):
        return replace_field(content, "status", new_status)

    if decision.upper() == "APPROVE":
        legacy_gold_file = NEEDS / f"TASK_{update_id}.md"
        legacy_gold_text = f'''---
source: platinum_update
source_update: {name}
status: NEW
execution_allowed: false
---

# Gold Intake From Platinum

This item came from Platinum local review.

Original update: {name}

Next step:
Gold must handle this through normal task -> plan -> approval -> execution -> logs.
'''
        legacy_gold_file.write_text(legacy_gold_text, encoding="utf-8")

        bridge_file_name = legacy_gold_file.name
        bridge_created = False

        if task_type == "email_draft":
            gold_file = NEEDS / f"TASK_EMAIL_{update_id}.md"
            gold_text = f'''---
source: platinum_update
source_update: {name}
status: NEW
execution_allowed: false
---

# Gold Intake From Platinum

This item was generated automatically by Platinum.

Original update: {name}

Task type: {task_type}

Instruction:
Proceed through standard Gold pipeline:
task -> plan -> approval -> execution -> logs
'''
            gold_file.write_text(gold_text, encoding="utf-8")
            bridge_file_name = gold_file.name
            bridge_created = True
            print(f"GOLD_ITEM: {gold_file}")
            log(f"{now()} | APPROVE | {name} | created {gold_file.name}")
        else:
            print(f"GOLD_ITEM: {legacy_gold_file}")
            log(f"{now()} | APPROVE | {name} | created {legacy_gold_file.name}")

        text = replace_status(text, "APPROVED_TO_GOLD")
        text = replace_field(text, "gold_bridge_created", "true" if bridge_created else "false")

        text = re.sub(r"\nreview_decision: .*", "", text, flags=re.DOTALL).rstrip()

        text += f"\n\nreview_decision: APPROVE\ngold_bridge_file: {bridge_file_name}\nprocessed_at: {now()}\n"

    elif decision.upper() == "REJECT":
        text = replace_status(text, "REJECTED")
        text = re.sub(r"\nreview_decision: .*", "", text, flags=re.DOTALL).rstrip()
        text += f"\n\nreview_decision: REJECT\nprocessed_at: {now()}\n"
        log(f"{now()} | REJECT | {name} | no gold item created")
        print("NO_GOLD_ITEM: REJECT")

    elif decision.upper() == "IGNORE":
        text = replace_status(text, "IGNORED")
        text = re.sub(r"\nreview_decision: .*", "", text, flags=re.DOTALL).rstrip()
        text += f"\n\nreview_decision: IGNORE\nprocessed_at: {now()}\n"
        log(f"{now()} | IGNORE | {name} | no gold item created")
        print("NO_GOLD_ITEM: IGNORE")

    else:
        print("DECISION must be APPROVE, REJECT, or IGNORE")
        return

    # --- PLATINUM METADATA INSERT (SAFE) ---
    if "processed_by:" not in text:
        if "claimed_by:" in text:
            text = text.replace("claimed_by: local_system", "claimed_by: local_system\nprocessed_by: local_system")
        elif "source:" in text:
            text = text.replace("source: cloud_draft", "source: cloud_draft\nclaimed_by: local_system\nprocessed_by: local_system")

    processed.write_text(text, encoding="utf-8")
    src.unlink()
    print(f"PROCESSED: {processed}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python tools/platinum/process_update.py claim <filename>")
        print("  python tools/platinum/process_update.py review <filename> APPROVE|REJECT|IGNORE")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    name = sys.argv[2]

    if cmd == "claim":
        claim(name)
    elif cmd == "review":
        if len(sys.argv) < 4:
            print("Missing decision")
            sys.exit(1)
        review(name, sys.argv[3])
    else:
        print("Unknown command")