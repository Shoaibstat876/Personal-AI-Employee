from pathlib import Path
import shutil
import subprocess
import sys

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
IN_PROGRESS_GOLD = PROJECT / "AI_Employee_Vault" / "In_Progress" / "gold"
NEEDS_ACTION = PROJECT / "AI_Employee_Vault" / "Needs_Action"
PLAN_GENERATOR = PROJECT / "tools" / "generate_plan_from_email_task.py"

def main():
    if len(sys.argv) < 2:
        print("ERROR: task filename required")
        sys.exit(1)

    task_filename = sys.argv[1]
    source_file = IN_PROGRESS_GOLD / task_filename

    if not source_file.exists():
        print(f"ERROR: source task not found: {source_file}")
        sys.exit(1)

    if task_filename.startswith("TASK_EMAIL_"):
        bridge_filename = task_filename
    else:
        bridge_filename = f"TASK_EMAIL_BRIDGE_{source_file.stem}.md"

    copied_file = NEEDS_ACTION / bridge_filename

    shutil.copy2(source_file, copied_file)
    print(f"BRIDGE_COPY_OK: {source_file} -> {copied_file}")

    result = subprocess.run(
        ["python", str(PLAN_GENERATOR)],
        cwd=str(PROJECT)
    )

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()