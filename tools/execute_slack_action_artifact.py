import json
import re
from pathlib import Path
from datetime import datetime, timezone
from urllib import request, parse

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
VAULT = PROJECT / "AI_Employee_Vault"
ARTIFACTS = VAULT / "Artifacts"
LOGS = VAULT / "Logs"
ENV_FILE = PROJECT / ".env"

def iso_now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load_env(path: Path) -> dict:
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env

def slack_api(token: str, method: str, payload: dict):
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"https://slack.com/api/{method}",
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {token}"
        },
        method="POST"
    )
    with request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    result = json.loads(body)
    if not result.get("ok"):
        raise RuntimeError(json.dumps(result, ensure_ascii=False))
    return result

def latest_slack_action_artifact() -> Path:
    files = sorted(
        ARTIFACTS.glob("SLACK_ACTION_*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if not files:
        raise SystemExit("STOP: no SLACK_ACTION_*.md found in Artifacts")
    return files[0]

def extract(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else ""

def already_executed(text: str) -> bool:
    return 'status: "executed"' in text or "## Execution Record" in text

def replace_status(text: str, new_status: str) -> str:
    return re.sub(r'^status:\s*"[^"]+"', f'status: "{new_status}"', text, flags=re.MULTILINE)

def append_execution_record(text: str, channel_id: str, channel_name: str, ts: str) -> str:
    return text + f"""

## Execution Record
- executed_at: {iso_now_utc()}
- action_type: send_message
- channel_id: {channel_id}
- channel_name: {channel_name}
- message_ts: {ts}
"""

def log_event(event_name: str, artifact_file: str, result_text: str) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    log_path = LOGS / "slack_execution_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            '{{"ts":"{}","event":"{}","artifact_file":"{}","result":"{}"}}\n'.format(
                iso_now_utc(),
                event_name,
                artifact_file,
                result_text.replace('"', "'")
            )
        )

def resolve_channel_id(token: str, channel_value: str):
    normalized = channel_value.strip()
    if normalized.startswith("#"):
        normalized = normalized[1:]

    cursor = None
    while True:
        payload = {"limit": 200, "exclude_archived": True, "types": "public_channel,private_channel"}
        if cursor:
            payload["cursor"] = cursor
        result = slack_api(token, "conversations.list", payload)
        for ch in result.get("channels", []):
            if ch.get("name") == normalized or ch.get("id") == channel_value:
                return ch["id"], ch.get("name", normalized)
        cursor = result.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    raise SystemExit(f"STOP: Slack channel not found or inaccessible: {channel_value}")

def main():
    if not ENV_FILE.exists():
        raise SystemExit("STOP: .env missing")

    env = load_env(ENV_FILE)
    token = env.get("SLACK_MCP_XOXB_TOKEN")
    if not token:
        raise SystemExit("STOP: SLACK_MCP_XOXB_TOKEN missing in .env")

    artifact_path = latest_slack_action_artifact()
    artifact_text = artifact_path.read_text(encoding="utf-8")

    channel_value = extract(r'^\- channel:\s*(.+)$', artifact_text)
    message = extract(r'^\- message:\s*(.+)$', artifact_text)

    if not channel_value or not message:
        raise SystemExit("STOP: channel or message not found in Slack action artifact")

    if already_executed(artifact_text):
        msg = "already_executed_idempotency_guard"
        log_event("SKIP_ALREADY_EXECUTED", artifact_path.name, msg)
        print(f"[SKIP] Slack artifact already executed: {artifact_path}")
        return

    channel_id, channel_name = resolve_channel_id(token, channel_value)

    result = slack_api(token, "chat.postMessage", {
        "channel": channel_id,
        "text": message
    })

    ts = result.get("ts", "")

    updated = replace_status(artifact_text, "executed")
    updated = append_execution_record(updated, channel_id, channel_name, ts)
    artifact_path.write_text(updated, encoding="utf-8")

    log_event("SLACK_MESSAGE_SENT", artifact_path.name, f"channel_id={channel_id};channel_name={channel_name};ts={ts}")

    print(f"[OK] source artifact: {artifact_path}")
    print(f"[OK] sent Slack message to: #{channel_name} ({channel_id})")
    print(f"[OK] message ts: {ts}")

if __name__ == "__main__":
    main()
