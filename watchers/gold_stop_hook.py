from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple, Optional


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
    if STOP_FILE.exists():
        return True, "STOP_FILE_PRESENT"

    if RUNTIME_FLAGS.exists():
        try:
            data = json.loads(RUNTIME_FLAGS.read_text(encoding="utf-8-sig"))
            if isinstance(data, dict) and data.get("stop") is True:
                return True, "RUNTIME_FLAGS_STOP_TRUE"
        except Exception:
            # Corrupt flags file is a safety risk; stop immediately.
            return True, "RUNTIME_FLAGS_CORRUPT"

    return False, ""


if __name__ == "__main__":
    stop, reason = should_stop()
    print(json.dumps({"stop": stop, "reason": reason}, ensure_ascii=False))

