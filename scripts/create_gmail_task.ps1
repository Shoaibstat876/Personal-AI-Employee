param(
  [Parameter(Mandatory=$true)][string]$Sender,
  [Parameter(Mandatory=$true)][string]$Subject,
  [Parameter(Mandatory=$true)][string]$Body
)

python ".\watchers\gmail_task_bridge.py" --sender $Sender --subject $Subject --body $Body
