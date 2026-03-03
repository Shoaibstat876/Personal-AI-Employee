# Business Goals — Personal AI Employee (Hackathon 0)

## Vision
Build a local-first, human-in-the-loop Digital FTE that reliably turns intents into audited actions with zero-risk safeguards.

## Problem
Manual operations (tasks, email drafts, approvals, briefings) are slow, inconsistent, and hard to audit. We need deterministic execution with proof artifacts.

## Who This Serves
- Founder/operator (Shoaib)
- Future teammates reviewing evidence
- Judges evaluating real executions

## Business Goals
1) Convert user requests into safe, deterministic actions.
2) Maintain an append-only audit trail for every attempt and result.
3) Enforce HITL approval before any risky action.
4) Produce weekly CEO briefings from local state and logs.
5) Recover safely from transient failures using retry/backoff and stop hooks.
6) Remain local-first and cost-controlled.

## KPIs (Measurable)
- 100% actions logged with timestamp + status + actor + output paths
- 0 uncontrolled external sends/posts (draft-only unless approved)
- Deterministic loop completes cleanly with clear end-state
- Evidence folders contain proof artifacts for every phase

## Out of Scope (Gold)
- Fully autonomous production posting
- Cloud-required dependencies

## Guardrails (Non-Negotiable)
- Draft-only by default for external systems
- No secrets in logs or evidence
- One task at a time; crash-safe resume supported
- Stop hook respected at checkpoints

## Acceptance Criteria
- Business_Goals.md is non-empty and structured
- Evidence copy exists under evidence/gold/01_business_context/
