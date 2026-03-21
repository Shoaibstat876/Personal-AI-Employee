import json
from pathlib import Path
from urllib import request

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
ENV_FILE = PROJECT / ".env"

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

def main():
    env = load_env(ENV_FILE)
    token = env.get("SLACK_MCP_XOXB_TOKEN")
    if not token:
        raise SystemExit("STOP: SLACK_MCP_XOXB_TOKEN missing in .env")

    cursor = None
    all_channels = []

    while True:
        payload = {"limit": 200, "exclude_archived": True, "types": "public_channel,private_channel"}
        if cursor:
            payload["cursor"] = cursor
        result = slack_api(token, "conversations.list", payload)
        for ch in result.get("channels", []):
            all_channels.append({
                "id": ch.get("id"),
                "name": ch.get("name"),
                "is_member": ch.get("is_member")
            })
        cursor = result.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    for ch in all_channels:
        print(f"{ch['id']} | #{ch['name']} | member={ch['is_member']}")

if __name__ == "__main__":
    main()
