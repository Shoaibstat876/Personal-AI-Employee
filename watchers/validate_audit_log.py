from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
JSONL = REPO_ROOT / "AI_Employee_Vault" / "Logs" / "gold_action_log.jsonl"

REQUIRED = ["ts", "event", "status", "actor"]

def main() -> int:
    if not JSONL.exists():
        print("FAIL: missing", JSONL)
        return 2

    bad_json = 0
    missing_required = 0
    total = 0

    with JSONL.open("r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                obj = json.loads(line)
            except Exception:
                bad_json += 1
                continue

            for k in REQUIRED:
                if k not in obj:
                    missing_required += 1
                    break

    print("AUDIT_LOG_PATH:", JSONL)
    print("TOTAL_LINES:", total)
    print("BAD_JSON_LINES:", bad_json)
    print("MISSING_REQUIRED_LINES:", missing_required)

    if total == 0:
        print("FAIL: empty log")
        return 3
    if bad_json or missing_required:
        print("FAIL")
        return 4

    print("PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
