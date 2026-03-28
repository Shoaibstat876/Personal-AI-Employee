# PLATINUM OPERATOR 6 — DEMO COMMAND PACK

## 1. MCP HEALTH
claude mcp list

---

## 2. PLATINUM RUNTIME STATUS
Get-Content AI_Employee_Vault\Updates\PLATINUM_RUNTIME_STATUS.md

---

## 3. WATCHER LIVE PROOF

# Trigger
"DEMO_TRIGGER 03/27/2026 10:54:40" | Set-Content dropbox\DEMO_TEST.txt
Start-Sleep -Seconds 5

# Result
Get-ChildItem dropbox\_processed | Sort-Object LastWriteTime -Descending | Select-Object -First 3 Name, LastWriteTime
Get-ChildItem AI_Employee_Vault\Needs_Action | Sort-Object LastWriteTime -Descending | Select-Object -First 3 Name, LastWriteTime

---

## 4. GOLD / HITL PROOF
Get-ChildItem AI_Employee_Vault\Needs_Action | Select-Object -First 5
Get-Content AI_Employee_Vault\Logs\approval_decision_log.jsonl -Tail 5

---

## 5. FINAL SNAPSHOT
Get-Content AI_Employee_Vault\Artifacts\gold\PLATINUM_FINAL_DEMO_SNAPSHOT.md
