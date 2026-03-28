# Platinum System Overview

## Purpose
This document defines runtime ownership and visibility for the Platinum layer.

The system is already complete. This layer adds observability only.

---

## Cloud Responsibilities
- Draft creation
- Update generation
- Writing into /Updates/Incoming/

Cloud NEVER executes actions (draft-only role).

---

## Local Responsibilities
- Claim updates
- Perform HITL review
- Process updates
- Create Gold bridge artifacts
- Execute via MCP (only after approval)
- Maintain Dashboard

---

## Core Rules

### Single-Writer Dashboard
Dashboard is LOCAL ONLY.

### Cloud Never Executes
Cloud produces drafts only.

### Local Always Approves
All execution is controlled via HITL.

### Determinism
No changes to:
- Gold scripts
- HITL flow
- MCP integrations
- Execution logic

---

## Lifecycle

Incoming -> Claimed -> Processed -> Bridged -> Gold -> Done

---

## Identity Model

source: cloud_draft  
claimed_by: local_system  
processed_by: local_system  

---

## Demo Value
- Clear system ownership
- Clear lifecycle tracking
- Production-grade visibility
- Teacher-friendly architecture clarity

---

## Safety
- Additive only
- Reversible
- Non-executing
- Fully deterministic