import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sender", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", required=True)
    args = parser.parse_args()

    cmd = [
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-File", r".\scripts\create_gmail_task.ps1",
        "-Sender", args.sender,
        "-Subject", args.subject,
        "-Body", args.body,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
