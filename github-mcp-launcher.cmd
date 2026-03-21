@echo off
for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
  if /I "%%A"=="GITHUB_TOKEN" set GITHUB_PERSONAL_ACCESS_TOKEN=%%B
)
docker run --rm -i -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server stdio
