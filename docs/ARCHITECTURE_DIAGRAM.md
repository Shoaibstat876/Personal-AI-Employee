# Personal AI Employee — Architecture Diagram

## High-Level Architecture

This system is designed as a **controlled, state-driven AI operations pipeline**.

It transforms incoming work into structured tasks, routes them through AI reasoning and **human-controlled decision gates**, executes only approved actions through **safe execution bridges**, and records every step for **full auditability, traceability, and demonstration**.

---

## Core Principles

• **Human-in-the-Loop Control** → no critical action executes without approval  
• **State Machine Workflow** → every task moves through defined lifecycle states  
• **Deterministic Execution** → only approved, predictable actions are performed  
• **Full Audit Trail** → every step is logged, reviewable, and provable  
• **Separation of Concerns** → input, reasoning, approval, execution are isolated  

---

## Architecture Flow

```text
┌──────────────────────────────────────────────────────────────────────┐
│                          INPUT SOURCES                              │
│              Email / Files / Notes / Requests / Artifacts           │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                           WATCHER LAYER                             │
│      Detects incoming work and converts it into structured tasks    │
│                                                                      │
│      • filesystem watcher                                           │
│      • email ingestion bridge                                       │
│      • manual file drop                                             │
│                                                                      │
│      OUTPUT: normalized task artifacts                              │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      VAULT SYSTEM (STATE MACHINE)                   │
│   Central operational storage and workflow state management layer   │
│                                                                      │
│   Needs_Action → Plans → Pending → Approved → Executed              │
│                                                                      │
│   • enforces state transitions                                      │
│   • stores artifacts, summaries, logs                               │
│   • acts as single source of truth                                  │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      CLAUDE REASONING LAYER                         │
│      Interprets task context and generates structured plans         │
│                                                                      │
│      • intent understanding                                         │
│      • plan generation                                              │
│      • human-readable reasoning                                     │
│                                                                      │
│      OUTPUT: plan artifact (reviewable, not executable)             │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                HUMAN APPROVAL LAYER (CONTROL GATE)                  │
│            Explicit decision boundary before execution              │
│                                                                      │
│            Approve  → allow execution                              │
│            Reject   → revise / return / halt                        │
│                                                                      │
│   ❗ No execution occurs without passing this layer                  │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                      approved   │   rejected / returned
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   EXECUTION BRIDGE (CONTROLLED)                     │
│      Performs only approved actions via safe, constrained tools     │
│                                                                      │
│      • sandboxed scripts                                            │
│      • MCP tool connectors                                          │
│      • controlled automation                                        │
│                                                                      │
│      GUARANTEES:                                                    │
│      • no autonomous execution                                      │
│      • deterministic outcomes                                       │
│      • action-level logging                                         │
└────────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                 OUTPUTS, LOGS, REPORTS & FEEDBACK                   │
│                                                                      │
│   • execution records                                               │
│   • audit logs (timestamped)                                        │
│   • CEO briefing outputs                                            │
│   • proof artifacts (screenshots, files)                            │
│                                                                      │
│   FEEDBACK LOOP:                                                    │
│   • results feed back into vault                                    │
│   • enables iteration, tracking, and future decisions               │
└──────────────────────────────────────────────────────────────────────┘