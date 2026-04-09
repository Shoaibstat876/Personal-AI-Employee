---
name: generate-ceo-briefing
description: Generate executive-level reports from system activity and logs.
---

# SKILL: generate-ceo-briefing

## Purpose
Summarize system activity into executive-level insights and reports.

---

## Real System Implementation
This skill is implemented through existing system components:

### Core Components
- ceo_briefing.py
- send_ceo_report.py

### Vault Mapping
- AI_Employee_Vault/Briefings/

### Artifacts
- CEO_REPORT_*.md

### Logs
- AI_Employee_Vault/Logs/ceo_report_log.jsonl

---

## Source of Execution
Report generation is handled by:

- tools/
- reporting scripts
- log aggregation

This is a **documentation layer only and does not contain runtime logic.**

---

## Inputs
- system logs
- workflow activity

---

## Outputs
- CEO reports
- stored in:
  - AI_Employee_Vault/Briefings/

---

## Workflow Position
Post-execution → Reporting

---

## Safety Boundary
- read-only aggregation
- no execution or side effects
- this skill operates within a controlled HITL workflow and does not bypass approval

---

## Evidence
- AI_Employee_Vault/Briefings/
- ceo_report_log.jsonl

---

## Notes
This is the executive intelligence layer translating operations into insights.