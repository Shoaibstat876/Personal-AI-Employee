$ErrorActionPreference = "Stop"

# ======================================================
# GOLD — Gmail MCP Connection (Stable + Judge-Safe)
# ======================================================
# Goal:
# - Gmail MCP stays stable across reboot/logon via Scheduled Task
# - Quick recovery steps if Claude shows "Failed to Connect"
# - Optional: MCP Pre-Flight Check for Gmail(3010) + Filesystem + GCAL
#
# NOTE:
# - If you are using PORT 3010 (recommended), update all commands accordingly.
# - If you still use PORT 3000, keep the 3000 sections as-is.
# ======================================================


# ======================================================
# A) EMERGENCY: If Port Conflict Happened (rare)
# ======================================================
# Use ONLY if you truly see EADDRINUSE or port is stuck.

# 1) Find what is holding the port
# (change 3000 -> 3010 if you are using 3010)
netstat -ano | findstr :3000

# 2) Kill the conflicting process (ONLY the PID you found)
# Example:
# taskkill /PID 25408 /F
# Replace <PID> with your actual PID:
taskkill /PID <PID> /F

# 3) Re-check MCP health
Set-Location "D:\Shoaib Project\Personal-AI-Employee"
claude mcp list


# ======================================================
# B) ONE-TIME SETUP: Create Scheduled Task (Run as Admin)
# ======================================================
# Run this once in an *Administrator PowerShell*.
# IMPORTANT:
# - Recommended PORT = 3010 (avoid common conflicts)
# - If you want 3000, set PORT=3000 instead

$Action    = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c set PORT=3010 && gmail-mcp"
$Trigger   = New-ScheduledTaskTrigger -AtLogOn
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -RunLevel Highest
Register-ScheduledTask -TaskName "GmailMCP" -Action $Action -Trigger $Trigger -Principal $Principal -Force


# ======================================================
# C) Start the Scheduled Task + Verify Port + Verify Claude
# ======================================================

Start-ScheduledTask -TaskName "GmailMCP"
Start-Sleep -Seconds 2

# Confirm port is listening (3010 recommended)
netstat -ano | findstr ":3010"

# Check Claude MCP list
Set-Location "D:\Shoaib Project\Personal-AI-Employee"
claude mcp list


# ======================================================
# 🗓 DAILY ROUTINE — Production Workflow
# ======================================================

## 🟢 Scenario 1 — Normal Day (Most Common)

You boot laptop → log in.

Do this:

cd D:\Shoaib Project\Personal-AI-Employee
claude

Optional confidence check:

claude mcp list

If you see:

gmail: http://localhost:3010/mcp (HTTP) - ✓ Connected

You are fully operational.

That’s it.

You do NOT need to:

- Kill ports
- Recreate scheduled task
- Run netstat
- Reinstall MCP
- Touch Google Console


## 🟡 Scenario 2 — Gmail Shows “Failed to Connect”

This means server is not running.

Do only this:

Start-ScheduledTask -TaskName "GmailMCP"
Start-Sleep -Seconds 2
claude mcp list

Done.

No killing ports unless something unusual happened.


## 🔴 Scenario 3 — Port Conflict (Rare)

Only if you see:

EADDRINUSE

Then:

# Identify port holder
netstat -ano | findstr :3010

# Kill the conflicting PID
taskkill /PID <PID_NUMBER> /F

# Restart task
Start-ScheduledTask -TaskName "GmailMCP"
Start-Sleep -Seconds 2

# Verify
claude mcp list


-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------


# ======================================================
# 🧠 SUPER HYBRID — Gmail MCP Stability & Daily Workflow
# ======================================================

## 🟦 PHASE 1 — ONE-TIME INFRASTRUCTURE VALIDATION (Cold Boot Proof)

Do this once to certify permanence.

1️⃣ Full System Restart

Start → Restart  
(Not sleep. Not shutdown. Real restart.)

2️⃣ After Login — Port Verification

Open PowerShell:

netstat -ano | findstr ":3010"

Expected:

TCP    0.0.0.0:3010    ...    LISTENING    <PID>

✓ If LISTENING → Scheduled Task auto-start confirmed  
❌ If nothing → Go to Phase 3 (Recovery)

3️⃣ MCP Connection Verification

cd D:\Shoaib Project\Personal-AI-Employee
claude mcp list

Expected:

gmail: http://localhost:3010/mcp (HTTP) - ✓ Connected

✓ If Connected → Infrastructure Certified Stable  
You are now officially persistent.

After this phase passes once, you NEVER need netstat again unless something breaks.


## 🟩 PHASE 2 — DAILY PRODUCTION ROUTINE (Normal Operation)

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


## 🟡 PHASE 3 — If Gmail Shows “Failed to Connect”

This means MCP server not running.

6️⃣ Start Scheduled Task Manually

Start-ScheduledTask -TaskName "GmailMCP"
Start-Sleep -Seconds 2
claude mcp list

If ✓ Connected → Done.

No port killing. No reinstall. No Google Console touching.


## 🔴 PHASE 4 — Rare Port Conflict (Only If You See EADDRINUSE)

7️⃣ Identify Port Holder
netstat -ano | findstr :3010

8️⃣ Kill Conflicting Process
taskkill /PID <PID_NUMBER> /F

9️⃣ Restart MCP
Start-ScheduledTask -TaskName "GmailMCP"
Start-Sleep -Seconds 2
claude mcp list

✓ Connected → Resolved.


---------------------------------------------------------------------------------------------


# ======================================================
# ✅ ULTIMATE QUICK CHECK (Recommended)
# ======================================================

# Gmail port + Claude MCP list
netstat -ano | findstr ":3010"
claude mcp list


# ======================================================
# OPTIONAL: Start GCAL runner + confirm
# ======================================================

$ErrorActionPreference = "Stop"

# Start GCAL runner (safe even if already running)
Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "C:\mcp\gcal\run-gcal.cmd" -WindowStyle Minimized
Start-Sleep -Seconds 2

# Check MCP list
claude mcp list


# ======================================================
# ✅ MCP PRE-FLIGHT CHECK (Gmail 3010 + Filesystem + GCAL)
# ======================================================

$ErrorActionPreference = "Stop"

"================ MCP PRE-FLIGHT CHECK ================"
"Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss K')"
"Repo: $(Get-Location)"
""

# -------------------------
# 1) Gmail (port 3010) check
# -------------------------
"--- Gmail Port Check (3010) ---"
$gmailListening = (Get-NetTCPConnection -LocalPort 3010 -State Listen -ErrorAction SilentlyContinue) -ne $null
if ($gmailListening) {
  "Gmail port 3010 listening ✓"
} else {
  "Gmail port 3010 NOT listening ✗"
  "NOTE: Start your gmail-mcp (scheduled task or your start script), then rerun."
}

# -------------------------
# 2) Filesystem MCP binary check
# -------------------------
"--- Filesystem MCP Binary Check ---"
$fsBin = ".\tools\mcp-filesystem\node_modules\.bin\mcp-server-filesystem.cmd"
if (Test-Path $fsBin) {
  "Filesystem binary exists ✓"
} else {
  "Filesystem binary missing ✗"
  "Fix: cd tools\mcp-filesystem ; npm ci"
}

# -------------------------
# 3) GCAL start check (optional)
# -------------------------
"--- GCAL Start Check ---"
Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "C:\mcp\gcal\run-gcal.cmd" -WindowStyle Minimized
Start-Sleep -Seconds 2
"GCAL runner started/ensured ✓"

# -------------------------
# 4) Final health
# -------------------------
""
"--- FINAL MCP STATUS ---"
claude mcp list
"======================================================="
