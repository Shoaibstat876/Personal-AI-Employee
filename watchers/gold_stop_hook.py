from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple


VAULT_ROOT = Path(__file__).resolve().parents[1] / "AI_Employee_Vault"
STOP_FILE = VAULT_ROOT / "STOP"
RUNTIME_FLAGS = VAULT_ROOT / "Decisions" / "runtime_flags.json"


def should_stop() -> Tuple[bool, str]:
    """
    Deterministic stop-hook for Gold tier.

    Stop conditions:
      1) AI_Employee_Vault/STOP exists
      2) AI_Employee_Vault/Decisions/runtime_flags.json contains {"stop": true}

    Returns:
      (True, reason) if stop requested
      (False, "") otherwise
    """

    # 1️⃣ STOP file has highest priority
    if STOP_FILE.exists():
        return True, "STOP_FILE_PRESENT"

    # 2️⃣ Runtime flags (explicit stop only)
    if RUNTIME_FLAGS.exists():
        try:
            text = RUNTIME_FLAGS.read_text(encoding="utf-8-sig").strip()

            # Ignore empty / partially written file
            if not text:
                return False, ""

            data = json.loads(text)

            if isinstance(data, dict) and data.get("stop") is True:
                return True, "RUNTIME_FLAGS_STOP_TRUE"

        except Exception:
            # If file is corrupt or partially written,
            # ignore it instead of forcing STOP.
            return False, ""

    return False, ""


if __name__ == "__main__":
    stop, reason = should_stop()
    print(json.dumps({"stop": stop, "reason": reason}, ensure_ascii=False))