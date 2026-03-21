import json
import re
from pathlib import Path
from datetime import datetime, timezone
from urllib import request

PROJECT = Path(r"D:\Shoaib Project\Personal-AI-Employee")
VAULT = PROJECT / "AI_Employee_Vault"
ARTIFACTS = VAULT / "Artifacts"
LOGS = VAULT / "Logs"
ENV_FILE = PROJECT / ".env.odoo"

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

def json_rpc(odoo_url: str, service: str, method: str, args: list):
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": service,
            "method": method,
            "args": args
        },
        "id": int(datetime.now().timestamp())
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"{odoo_url}/jsonrpc",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    result = json.loads(body)
    if result.get("error"):
        raise RuntimeError(json.dumps(result["error"], ensure_ascii=False))
    return result["result"]

def login(env: dict):
    uid = json_rpc(env["ODOO_URL"], "common", "login", [
        env["ODOO_DB"],
        env["ODOO_USER"],
        env["ODOO_API_KEY"]
    ])
    if not uid:
        raise SystemExit("STOP: Odoo login failed")
    return uid

def execute_kw(env: dict, uid: int, model: str, method: str, positional_args=None, keyword_args=None):
    positional_args = positional_args or []
    keyword_args = keyword_args or {}
    return json_rpc(env["ODOO_URL"], "object", "execute_kw", [
        env["ODOO_DB"],
        uid,
        env["ODOO_API_KEY"],
        model,
        method,
        positional_args,
        keyword_args
    ])

def latest_odoo_action_artifact() -> Path:
    files = sorted(
        ARTIFACTS.glob("ODOO_ACTION_*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    if not files:
        raise SystemExit("STOP: no ODOO_ACTION_*.md found in Artifacts")
    return files[0]

def extract(pattern: str, text: str) -> str:
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else ""

def already_executed(text: str) -> bool:
    return 'status: "executed"' in text or "## Execution Record" in text

def replace_status(text: str, new_status: str) -> str:
    return re.sub(r'^status:\s*"[^"]+"', f'status: "{new_status}"', text, flags=re.MULTILINE)

def append_execution_record(text: str, customer_id: str, customer_name: str) -> str:
    return text + f"""

## Execution Record
- executed_at: {iso_now_utc()}
- action_type: create_customer
- customer_id: {customer_id}
- customer_name: {customer_name}
"""

def log_event(event_name: str, artifact_file: str, result_text: str) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    log_path = LOGS / "odoo_execution_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(
            '{{"ts":"{}","event":"{}","artifact_file":"{}","result":"{}"}}\n'.format(
                iso_now_utc(),
                event_name,
                artifact_file,
                result_text.replace('"', "'")
            )
        )

def main():
    if not ENV_FILE.exists():
        raise SystemExit("STOP: .env.odoo missing")

    env = load_env(ENV_FILE)
    required = ["ODOO_URL", "ODOO_DB", "ODOO_USER", "ODOO_API_KEY"]
    for key in required:
        if not env.get(key):
            raise SystemExit(f"STOP: missing {key} in .env.odoo")

    artifact_path = latest_odoo_action_artifact()
    artifact_text = artifact_path.read_text(encoding="utf-8")

    customer_name = extract(r'^\- customer_name:\s*(.+)$', artifact_text)
    customer_email = extract(r'^\- customer_email:\s*(.+)$', artifact_text)
    customer_phone = extract(r'^\- customer_phone:\s*(.+)$', artifact_text)

    if not customer_name:
        raise SystemExit("STOP: customer_name not found in Odoo action artifact")

    if already_executed(artifact_text):
        msg = "already_executed_idempotency_guard"
        log_event("SKIP_ALREADY_EXECUTED", artifact_path.name, msg)
        print(f"[SKIP] Odoo artifact already executed: {artifact_path}")
        return

    uid = login(env)

    existing = execute_kw(
        env, uid, "res.partner", "search_read",
        [[["name", "=", customer_name]]],
        {"fields": ["id", "name", "email", "phone"], "limit": 1}
    )

    if existing:
        existing_id = existing[0]["id"]
        updated = replace_status(artifact_text, "executed")
        updated = append_execution_record(updated, str(existing_id), customer_name)
        artifact_path.write_text(updated, encoding="utf-8")
        log_event("SKIP_CUSTOMER_ALREADY_EXISTS", artifact_path.name, f"existing_customer_id={existing_id}")
        print(f"[SKIP] customer already exists in Odoo: {customer_name} (id={existing_id})")
        return

    customer_id = execute_kw(
        env, uid, "res.partner", "create",
        [{
            "name": customer_name,
            "email": customer_email,
            "phone": customer_phone
        }]
    )

    updated = replace_status(artifact_text, "executed")
    updated = append_execution_record(updated, str(customer_id), customer_name)
    artifact_path.write_text(updated, encoding="utf-8")

    log_event("ODOO_CUSTOMER_CREATED", artifact_path.name, f"customer_id={customer_id};name={customer_name}")

    print(f"[OK] source artifact: {artifact_path}")
    print(f"[OK] created Odoo customer: {customer_name}")
    print(f"[OK] customer_id: {customer_id}")

if __name__ == "__main__":
    main()
