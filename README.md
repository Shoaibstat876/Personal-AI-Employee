🚀 Personal AI Employee — Hackathon 0

A controlled, auditable AI operations system with human-in-the-loop governance and real-world execution capabilities.

🧠 What This Project Is

A local-first, Human-in-the-Loop (HITL) AI Employee system that converts unstructured inputs into controlled, auditable execution workflows across real tools (Slack, Odoo, Email, Filesystem).

It is built to solve a critical problem:

👉 AI systems are powerful — but unsafe without control, visibility, and accountability.

This system ensures:

structured execution
human approval at critical steps
deterministic behavior
full auditability

This is not a chatbot.
This is a state-driven AI operations system.

⚙️ What Is Implemented
Watcher-based task intake (filesystem + Gmail)
Structured pipeline: Task → Plan → Approval → Execution
Human-in-the-loop enforcement (no approval → no execution)
Controlled execution via MCP integrations
Multi-system actions (Slack, Odoo, Email, Filesystem)
Append-only audit logging (JSONL)
CEO reporting and summaries
Deterministic orchestration with retry safety
🏆 What Gold Proves (Execution System)

The Gold layer is the core execution engine.

It proves that the system is:

Deterministic (no randomness)
Fully auditable and traceable
Strictly controlled via HITL
Capable of real multi-system execution
End-to-end functional (input → execution → logs)
Resume-safe and crash-safe

👉 Gold = actual execution system

☁️ What Platinum Adds (Observability Layer)

The Platinum layer enhances visibility and system clarity without modifying execution logic.

It adds:

Cloud vs Local execution separation
Asynchronous update lifecycle (Incoming → Claimed → Processed → Gold)
Runtime visibility dashboard
Non-executing cloud draft system
Clear ownership and state tracking

⚠️ Platinum does NOT execute actions
⚠️ Platinum does NOT modify Gold logic

👉 Platinum = observability + control clarity
👉 Gold handles execution
👉 Platinum explains and tracks the system

🔄 Demo Flow

MCP → Runtime → Watcher → Task → Plan → Approval → Artifact → Logs

(Each step produces verifiable files and logs inside the Vault)

This demonstrates:

controlled execution
human-in-the-loop enforcement
full auditability
deterministic system behavior
▶️ How to Run Demo
Check MCP:
claude mcp list
Trigger watcher:
"DEMO" | Set-Content dropbox\test.txt
Observe lifecycle:
Needs_Action
Plans
Pending_Approval
Approved
Artifacts
Logs
🔄 System Flow
Simplified Flow

Input → Task → Plan → Approval → Execution → Logs → Reporting

Full Flow

MCP → Runtime → Watcher → Task → Plan → Approval → Artifact → Logs

🗂 Repository Structure (High-Level)
AI_Employee_Vault/ → system state, workflow, logs
watchers/ → perception layer
tools/ → orchestration + execution
ui/ → dashboard + HITL + CEO view
docs/ → architecture + demo scripts
evidence/ → structured proof layer
🧪 Evidence Structure (IMPORTANT)

This project maintains two complementary evidence layers:

1. Repository Evidence (/evidence/)

Contains:

structured verification files
logs and snapshots
MCP validation
Gold execution proof
deterministic workflow evidence

👉 This is the core judge-verifiable proof layer

2. Platinum Evidence Pack

AI_Employee_Vault/Artifacts/PLATINUM_EVIDENCE_PACK/

Contains:

grouped screenshot-based validation
A → J structured proof packs
end-to-end lifecycle visual evidence
UI and execution screenshots

👉 This is the final presentation-ready evidence pack

✅ Why Two Layers?
evidence/ → technical proof (deep validation)
PLATINUM_EVIDENCE_PACK/ → visual proof (easy judging)

Together they provide:

✔ full traceability
✔ visual clarity
✔ judge-friendly validation

🎬 Quick Demo (Judge-Safe)
Drop file into dropbox/
Task appears in Needs_Action/
Plan generated → Pending_Approval/
Approve → move to Approved/
Execution via MCP
Output appears in:
Artifacts/
Logs/
Briefings/
🧩 Core Architecture
1. Input Layer (Watchers)

Filesystem + Gmail → structured tasks

2. Vault System (State Machine)

Needs_Action → Plans → Pending_Approval → Approved → Done

Acts as:

system memory
workflow engine
single source of truth
3. AI Reasoning Layer

Generates structured plans (non-executing)

4. Human-in-the-Loop (HITL)

Mandatory approval before execution

5. Controlled Execution Layer

MCP-based execution:

Slack
Odoo
Email
Files
6. Audit & Logging Layer

Append-only JSONL logs → full traceability

7. Reporting Layer

CEO Briefings + insights

🔌 MCP Integrations
Gmail
GitHub
Slack
Google Calendar
Filesystem
Playwright
Odoo
Context7

✔ controlled
✔ verified
✔ logged

🔒 System Guarantees
No execution without approval
No uncontrolled actions
Full audit trail
Deterministic behavior
Reproducibility
🔁 Reliability
Retry logic
Crash-safe loop
Lock-based execution
Resume-safe system
📊 System Capabilities
Autonomous intake
AI reasoning + HITL
Controlled execution
Multi-system integration
Scheduling
Full traceability
🧠 What Makes This Different

This is NOT:

a chatbot
a simple automation script

This IS:

A Controlled AI Operations System
with human governance and production-style architecture

🏁 Final Verdict

ELITE GOLD + PLATINUM — COMPLETE ✅

Gold → execution
Platinum → visibility
System → safe, controlled, auditable

👉 Proven with real logs, real execution, real artifacts

🚫 Gold Freeze Rule

Do NOT:

modify core system
restructure architecture
introduce new features
▶️ Next Step

👉 Platinum validation + demo presentation

❤️ Closing Note

This system proves AI can be:

controlled
safe
auditable
reliable

—not just automated.