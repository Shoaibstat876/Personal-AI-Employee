@echo off
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
  if /I "%%A"=="SLACK_MCP_XOXB_TOKEN" set SLACK_MCP_XOXB_TOKEN=%%B
  if /I "%%A"=="SLACK_MCP_ADD_MESSAGE_TOOL" set SLACK_MCP_ADD_MESSAGE_TOOL=%%B
)
npx -y slack-mcp-server@latest --transport stdio