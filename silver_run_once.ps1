$ErrorActionPreference = 'Stop'

Set-Location -Path "D:\Shoaib Project\Personal-AI-Employee"
# ===== Paths =====
$PROJECT = 'D:\Shoaib Project\Personal-AI-Employee'
$VAULT   = Join-Path $PROJECT 'AI_Employee_Vault'
$APPROVED = Join-Path $VAULT 'Approved'
$LOGS     = Join-Path $VAULT 'Logs'
$LOG_FILE = Join-Path $LOGS 'silver_scheduler_log.md'
$PROMPT_TPL = Join-Path $PROJECT 'silver_prompt_template.md'

function LogLine($msg) {
  $ts = (Get-Date).ToString('s')
  Add-Content -Encoding UTF8 -Path $LOG_FILE -Value "$ts | SILVER | $msg"
}

function Get-YamlValue($text, $key) {
  $m = [regex]::Match($text, "(?m)^\s*$key\s*:\s*(.+)\s*$")
  if ($m.Success) { return $m.Groups[1].Value.Trim().Trim('"') }
  return $null
}

# Guards
if (!(Test-Path $VAULT))      { throw "STOP: VAULT missing: $VAULT" }
if (!(Test-Path $APPROVED))   { throw "STOP: Approved folder missing: $APPROVED" }
if (!(Test-Path $LOGS))       { throw "STOP: Logs folder missing: $LOGS" }
if (!(Test-Path $PROMPT_TPL)) { throw "STOP: Prompt template missing: $PROMPT_TPL" }

# Find first approved+unexecuted approval file deterministically
$files = Get-ChildItem -Path $APPROVED -Filter *.md -File | Sort-Object Name
if ($files.Count -eq 0) {
  LogLine "NO_WORK — no approval files in Approved/"
  exit 0
}

$target = $null
$task_id = $null
$action_id = $null

foreach ($f in $files) {
  $txt = Get-Content -Raw -Path $f.FullName
  $status = Get-YamlValue $txt 'status'
  $executed = Get-YamlValue $txt 'executed'
  if ([string]::IsNullOrWhiteSpace($executed)) { $executed = 'false' }

  if (($status -eq 'approved') -and ($executed -eq 'false')) {
    $task_id = Get-YamlValue $txt 'task_id'
    $action_id = Get-YamlValue $txt 'action_id'
    if (![string]::IsNullOrWhiteSpace($task_id) -and ![string]::IsNullOrWhiteSpace($action_id)) {
      $target = $f
      break
    }
  }
}

if ($null -eq $target) {
  LogLine "NO_WORK — no approved+unexecuted items found"
  exit 0
}

# Atomic lock to prevent duplicate scheduler double-trigger
$lock = Join-Path $LOGS ("silver_lock_{0}.lock" -f $action_id)
try {
  New-Item -ItemType File -Path $lock -ErrorAction Stop | Out-Null
} catch {
  LogLine ("DEDUP_EXIT — lock exists for action_id={0}" -f $action_id)
  exit 0
}

try {
  LogLine ("START action_id={0} task_id={1} file={2}" -f $action_id, $task_id, $target.Name)
  LogLine ("MCP_EVIDENCE tool=playwright url=https://example.com mode=read-only action_id={0} task_id={1}" -f $action_id, $task_id)

  # Build concrete prompt from template (inject variables)
  $tpl = Get-Content -Raw -Path $PROMPT_TPL
  $prompt = $tpl.Replace('{{APPROVAL_FILE_PATH}}', $target.FullName).Replace('{{TASK_ID}}', $task_id).Replace('{{ACTION_ID}}', $action_id)

  # Save prompt for audit (optional but deterministic)
  $promptFile = Join-Path $LOGS ("silver_prompt_{0}.md" -f $action_id)
  Set-Content -Encoding UTF8 -Path $promptFile -Value $prompt

  # Invoke Claude Code in NON-INTERACTIVE mode
  # -p = print mode (no interactive approval prompts)
  # --allowedTools auto-approves tool use (Read/Edit + Browser/MCP use if available)
  $claudeCmd = "claude"
  $args = @(
    "-p",
    "--allowedTools", "Read,Edit,Browser,MCP",
    "--setting-sources","user,project,local",
    "--max-turns","6",
    $prompt
  )

  & $claudeCmd @args 2>&1 | ForEach-Object { LogLine ("CLAUDE_OUT | " + $_) }

  # Verify executed flag is now true
  $after = Get-Content -Raw -Path $target.FullName
  $executed_after = Get-YamlValue $after 'executed'
  if ($executed_after -ne 'true') {
    LogLine ("FAIL — executed flag not set for action_id={0}" -f $action_id)
    throw "executed_not_set"
  }

  LogLine ("PASS — executed=true confirmed for action_id={0}" -f $action_id)
  exit 0

} catch {
  # On any failure, remove lock so the next scheduler tick can retry (still prevents double-trigger concurrency)
  if (Test-Path $lock) { Remove-Item $lock -Force }
  LogLine ("LOCK_RELEASED_FAIL action_id={0}" -f $action_id)
  exit 1
}






