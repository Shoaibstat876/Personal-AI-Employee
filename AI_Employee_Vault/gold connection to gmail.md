$ErrorActionPreference="Stop"

# 1) Kill whatever is holding port 3000
taskkill /PID 25408 /F

# 2) Confirm port 3000 is free
netstat -ano | findstr :3000

# 3) Now re-check MCP health
Set-Location "D:\Shoaib Project\Personal-AI-Employee"
claude mcp list

## run this administration powershell 

$Action    = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c set PORT=3000 && gmail-mcp"
$Trigger   = New-ScheduledTaskTrigger -AtLogOn
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -RunLevel Highest
Register-ScheduledTask -TaskName "GmailMCP" -Action $Action -Trigger $Trigger -Principal $Principal -Force

then run this 

Start-ScheduledTask -TaskName "GmailMCP"
Start-Sleep -Seconds 2
netstat -ano | findstr ":3000"

Start-ScheduledTask -TaskName "GmailMCP"
Start-Sleep -Seconds 2
netstat -ano | findstr ":3000"
claude mcp list

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
🗓 DAILY ROUTINE — Production Workflow
🟢 Scenario 1 — Normal Day (Most Common)

You boot laptop → log in.

Do this:

cd D:\Shoaib Project\Personal-AI-Employee
claude

Optional confidence check:

claude mcp list

If you see:

gmail: http://localhost:3000/mcp (HTTP) - ✓ Connected

You are fully operational.

That’s it.

You do NOT need to:

Kill ports

Recreate scheduled task

Run netstat

Reinstall MCP

Touch Google Console

🟡 Scenario 2 — Gmail Shows “Failed to Connect”

This means server is not running.

Do only this:

Start-ScheduledTask -TaskName "GmailMCP"
Start-Sleep -Seconds 2
claude mcp list

Done.

No killing ports unless something unusual happened.

🔴 Scenario 3 — Port Conflict (Rare)

Only if you see:

EADDRINUSE

Then:

netstat -ano | findstr :3000
taskkill /PID <that_pid> /F
Start-ScheduledTask -TaskName "GmailMCP"

-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------
🧠 SUPER HYBRID — Gmail MCP Stability & Daily Workflow
🟦 PHASE 1 — ONE-TIME INFRASTRUCTURE VALIDATION (Cold Boot Proof)

Do this once to certify permanence.

1️⃣ Full System Restart

Start → Restart
(Not sleep. Not shutdown. Real restart.)

2️⃣ After Login — Port Verification

Open PowerShell:

netstat -ano | findstr ":3000"

Expected:

TCP    0.0.0.0:3000    ...    LISTENING    <PID>

✔ If LISTENING → Scheduled Task auto-start confirmed
❌ If nothing → Go to Phase 3 (Recovery)

3️⃣ MCP Connection Verification
cd D:\Shoaib Project\Personal-AI-Employee
claude mcp list

Expected:

gmail: http://localhost:3000/mcp (HTTP) - ✓ Connected

✔ If Connected → Infrastructure Certified Stable
You are now officially persistent.

After this phase passes once, you NEVER need netstat again unless something breaks.

🟩 PHASE 2 — DAILY PRODUCTION ROUTINE (Normal Operation)

This is your everyday workflow.

4️⃣ Boot Laptop → Login

No checks yet.

5️⃣ Start Claude
cd D:\Shoaib Project\Personal-AI-Employee
claude

That’s it.

Optional confidence check:

claude mcp list

If Gmail shows ✓ Connected → You are operational.

🟡 PHASE 3 — If Gmail Shows “Failed to Connect”

This means MCP server not running.

6️⃣ Start Scheduled Task Manually
Start-ScheduledTask -TaskName "GmailMCP"
Start-Sleep -Seconds 2
claude mcp list

If ✓ Connected → Done.

No port killing. No reinstall. No Google Console touching.

🔴 PHASE 4 — Rare Port Conflict (Only If You See EADDRINUSE)
7️⃣ Identify Port Holder
netstat -ano | findstr :3000
8️⃣ Kill Conflicting Process
taskkill /PID <PID_NUMBER> /F
9️⃣ Restart MCP
Start-ScheduledTask -TaskName "GmailMCP"
Start-Sleep -Seconds 2
claude mcp list

✔ Connected → Resolved.

---------------------------------------------------------------------------------------------

use only this the ultimate solution 

netstat -ano | findstr ":3010"
claude mcp list