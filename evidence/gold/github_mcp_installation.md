GitHub MCP Installation Evidence

Project: Personal AI Employee
Operator: Muhammad Shoaib Abdul Shakoor
Date: March 11, 2026
Environment: Windows PowerShell + Claude Code MCP

1. Objective

Install, configure, test, and stabilize the GitHub MCP Server for the Personal AI Employee system using STDIO transport.

The server must successfully:

connect to Claude MCP

authenticate with GitHub

load available tools

perform read operations

perform write operations

reconnect automatically after restart

2. Environment

Project directory:

D:\Shoaib Project\Personal-AI-Employee

Configuration files used:

.mcp.json
.env
github-mcp-launcher.cmd

Docker version:

Docker version 29.1.3

Claude MCP servers installed:

context7
filesystem
gcal
gmail
playwright
slack
github
3. MCP Server Configuration

.mcp.json

{
  "mcpServers": {
    "slack": {
      "command": "cmd",
      "args": [
        "/c",
        "D:\\Shoaib Project\\Personal-AI-Employee\\slack-mcp-launcher.cmd"
      ]
    },
    "github": {
      "command": "cmd",
      "args": [
        "/c",
        "D:\\Shoaib Project\\Personal-AI-Employee\\github-mcp-launcher.cmd"
      ]
    }
  }
}
4. GitHub MCP Launcher

File:

github-mcp-launcher.cmd

Content:

@echo off
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
  if /I "%%A"=="GITHUB_TOKEN" set GITHUB_PERSONAL_ACCESS_TOKEN=%%B
)
docker run --rm -i -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server stdio

Purpose:

load token from .env

start official GitHub MCP server

run using STDIO transport

5. MCP Discovery Verification

Command executed:

claude mcp list

Result:

github: cmd /c D:\Shoaib Project\Personal-AI-Employee\github-mcp-launcher.cmd - ✓ Connected

Claude interface verification:

/mcp

Result:

github · ✔ connected
Capabilities: tools · prompts
Tools: 41 tools
6. Read-Only Smoke Test

Command executed:

mcp__github__list_issues owner="Shoaibstat876" repo="Personal-AI-Employee"

Result:

issues: []
totalCount: 0

Conclusion:

GitHub MCP successfully authenticated and queried repository data.

7. Write Permission Test

Command executed:

mcp__github__create_issue owner="Shoaibstat876" repo="Personal-AI-Employee"
title="GitHub MCP Smoke Test — Personal AI Employee"

Result:

Issue ID: 4057569969
URL: https://github.com/Shoaibstat876/Personal-AI-Employee/issues/1

Conclusion:

GitHub MCP successfully performed a write operation.

8. Restart Stability Test

Procedure:

Claude exited

Claude restarted

/mcp executed

Result:

github · ✔ connected

Conclusion:

GitHub MCP reconnects automatically after restart.

9. Final Status

All operational gates completed successfully.

GITHUB MCP SERVER — STABLE