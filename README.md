# Personal AI Employee — Hackathon 0

Personal AI Employee is a controlled, auditable AI operations system built with Human-in-the-Loop (HITL) governance, workflow state management, MCP integrations, and structured audit logging.

This project is not a chatbot.  
It is a state-driven AI workflow system designed to convert unstructured inputs into controlled, reviewable, and traceable execution workflows.

---

## Live / Demo Links

- UI Demo: https://personal-ai-employee-ui.vercel.app/dashboard.html
- Final Proof Branch: `platinum-final-demo`

> Note: The `main` branch is used as the public project overview. The final demo-ready implementation and evidence are available in the `platinum-final-demo` branch.

---

## Final Review Branch

The final working demo and proof branch is:

```txt
platinum-final-demo
```

The `main` branch is used as the recruiter-facing project overview.  
The full final implementation, evidence flow, UI, and demo-ready system are available in the `platinum-final-demo` branch.

---

## What This Project Demonstrates

Personal AI Employee demonstrates how AI automation can be made safer through:

- Human approval before sensitive actions
- Controlled task lifecycle management
- Deterministic workflow states
- MCP-backed tool integrations
- Append-only audit logging
- Evidence-based execution proof
- CEO briefing/report generation
- Runtime visibility and state tracking

The system is designed around safety, traceability, and accountability.

---

## Core System Flow

```txt
Input → Task → Plan → Human Approval → Execution → Logs → Reporting
```

Full demo flow:

```txt
MCP → Runtime → Watcher → Task → Plan → Approval → Artifact → Logs
```

Each step produces verifiable files, artifacts, or logs inside the project vault.

---

## Architecture Overview

### 1. Input / Perception Layer

The system accepts tasks through watcher-based intake.

Implemented intake sources include:

- Filesystem watcher
- Gmail intake bridge
- Manual task creation

Raw inputs are converted into structured tasks.

---

### 2. Vault-Based State Machine

The project uses a local vault as the system memory and workflow engine.

Main workflow states:

```txt
Needs_Action → In_Progress → Plans → Pending_Approval → Approved → Done
```

The vault acts as:

- Source of truth
- Workflow state tracker
- Audit-friendly system memory
- Human review surface

---

### 3. Planning Layer

The system generates structured execution plans before any action is taken.

Plans are reviewable and do not automatically execute sensitive actions.

---

### 4. Human-in-the-Loop Governance

Human approval is required before controlled execution.

Key rule:

```txt
No approval → no execution
```

This ensures the system remains safe, reviewable, and accountable.

---

### 5. Controlled Execution Layer

Approved actions can be executed through controlled integrations.

Implemented / demonstrated integrations include:

- Slack
- Odoo
- Email
- Filesystem
- Gmail
- GitHub
- Google Calendar
- Playwright
- Context7

All sensitive actions are governed by approval and logging.

---

### 6. Audit and Evidence Layer

The system keeps structured logs and evidence for verification.

Evidence includes:

- JSONL audit logs
- Watcher logs
- Execution logs
- Approval artifacts
- CEO briefings
- Demo screenshots
- Platinum evidence pack

This makes the workflow traceable from input to final output.

---

## Tier Progression / Branch Guide

| Branch | Purpose |
|---|---|
| `main` | Recruiter-facing overview README |
| `silver-dev` | Silver watcher/perception layer |
| `gold-dev` | Gold orchestration, audit, and CEO briefing layer |
| `gold-gap-fix` | Gold repair and finalization branch |
| `platinum-start` | Start of Platinum visibility layer |
| `pipeline-repair-safe` | Safe pipeline repair branch |
| `platinum-final-demo` | Final working demo and proof branch |

---

## Gold Layer

The Gold layer proves the core execution system.

It demonstrates:

- Deterministic workflow execution
- Resume-safe processing
- Human approval gates
- Structured audit logs
- CEO briefing generation
- Controlled execution after approval
- Retry and crash-safety concepts

Gold represents the main controlled execution system.

---

## Platinum Layer

The Platinum layer adds visibility and final demo readiness.

It demonstrates:

- Runtime visibility dashboard
- Cloud vs local execution separation
- Clear state ownership
- Final UI/demo presentation
- Evidence pack organization
- Final proof branch preparation

Platinum improves observability and evaluation clarity without weakening the HITL safety model.

---

## Key Safety Guarantees

- No uncontrolled execution
- No sensitive action without approval
- Human-in-the-loop enforcement
- Append-only audit logging
- Traceable workflow transitions
- Deterministic state movement
- Clear Gold vs Platinum boundaries

---

## Evidence Locations

Important evidence and proof files are organized across the final branch, especially:

```txt
AI_Employee_Vault/
AI_Employee_Vault/Logs/
AI_Employee_Vault/Artifacts/
AI_Employee_Vault/Briefings/
AI_Employee_Vault/Artifacts/PLATINUM_EVIDENCE_PACK/
docs/
evidence/
```

The final demo-ready evidence is available in:

```txt
platinum-final-demo
```

---

## Quick Demo Concept

A judge-safe demo follows this flow:

1. Drop or receive an input task
2. Watcher converts input into a structured task
3. System generates a plan
4. Plan moves to pending approval
5. Human approves the action
6. Controlled execution runs
7. Output is saved as an artifact
8. Logs record the full lifecycle

---

## What Makes This Project Different

This project is not a simple automation script.

It is a controlled AI operations system focused on:

- Safety
- Auditability
- Human approval
- Real workflow states
- Tool integration
- Evidence-backed execution

The goal is to show how AI automation can be made practical, governed, and reviewable.

---

## Current Status

Final project status:

```txt
Gold + Platinum demo system completed
Final proof branch: platinum-final-demo
Live UI demo available
```

This project demonstrates practical AI automation engineering, workflow orchestration, HITL governance, MCP-style integrations, and audit-ready system design.
