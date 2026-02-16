# SKILL: Basic Task Processor (Bronze)

## Purpose
Convert a TASK file into a short human-readable summary and a safe next-step checklist.

## Inputs
- One TASK file path inside /Needs_Action

## Output
Write a markdown summary file to:
- /Done/SUMMARY_<task_id>.md

## Rules (Bronze)
- Do NOT execute external actions.
- Do NOT call network services.
- Do NOT modify watcher scripts.
- Do NOT create plans or approvals automatically.
- Only summarize and suggest next steps.

## Output Format
---
task_id: "<task_id>"
source_task: "<filename>"
created: "<ISO timestamp>"
---
# Summary
(3-6 bullets)

# Suggested Next Steps
- [ ] Step 1
- [ ] Step 2
