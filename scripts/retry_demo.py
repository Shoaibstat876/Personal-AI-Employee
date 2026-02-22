from __future__ import annotations

import sys
from pathlib import Path

# Allow both:
#   python -m scripts.retry_demo   (preferred)
#   python scripts/retry_demo.py   (still works)
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.retry import RetryConfig, TransientError, with_retry


def main() -> int:
    attempts = {"n": 0}

    def flaky_operation() -> str:
        attempts["n"] += 1
        # fail first 2 times, succeed on 3rd
        if attempts["n"] < 3:
            raise TransientError(f"simulated transient failure (attempt={attempts['n']})")
        return "OK"

    result = with_retry(
        flaky_operation,
        cfg=RetryConfig(max_attempts=5, base_delay_s=0.1, max_delay_s=0.5, jitter=False),
    )

    print("retry_demo_result=", result)
    print("retry_demo_attempts=", attempts["n"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
