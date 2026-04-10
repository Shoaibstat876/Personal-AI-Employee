# CONSTITUTION — PERSONAL AI EMPLOYEE (HACKATHON 0)

## Purpose

This constitution defines the governing principles for the Personal AI Employee system implemented in Hackathon 0.

It establishes how the system behaves, what it is allowed to do, what it must not do, and how it maintains trust, control, and auditability.

This document applies to both Gold and Platinum layers.

---

## 1. System Philosophy

The system is designed as a **controlled, auditable, human-supervised AI workflow**, not an autonomous agent.

Core philosophy:

- Execution is **controlled**, not automatic
- Decisions are **reviewed**, not assumed
- Actions are **logged**, not hidden
- Behavior is **deterministic**, not random
- Evidence is **required**, not optional

---

## 2. Human-in-the-Loop (HITL) is Mandatory

No meaningful action may be executed without human approval.

This includes:

- sending messages
- creating external records
- posting content
- triggering integrations (Odoo, Slack, etc.)

Rules:

- Plans must be generated before execution
- Plans must be reviewed before approval
- Approval must exist before execution
- Execution without approval is prohibited

HITL is a **core safety boundary**, not a feature.

---

## 3. Deterministic Workflow Enforcement

All tasks must follow a defined lifecycle:
