from __future__ import annotations

from pathlib import Path
from typing import List


REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT_ROOT = REPO_ROOT / "AI_Employee_Vault"
NEEDS_ACTION_DIR = VAULT_ROOT / "Needs_Action"


def list_needs_action_tasks() -> List[str]:
    """
    Deterministic scan of Needs_Action.

    Returns a list of filenames (not full paths), sorted lexicographically.
    Only files are included. Directories are ignored.

    No side effects.
    """
    if not NEEDS_ACTION_DIR.exists():
        return []

    items = []
    for p in NEEDS_ACTION_DIR.iterdir():
        if p.is_file():
            items.append(p.name)

    return sorted(items)


if __name__ == "__main__":
    for name in list_needs_action_tasks():
        print(name)
