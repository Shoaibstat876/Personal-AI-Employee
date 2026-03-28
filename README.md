# 🚀 Personal AI Employee — Hackathon 0

> A controlled, auditable AI operations system with human-in-the-loop governance and real-world execution capabilities.

---

## 🧠 What This Project Is

A **local-first, Human-in-the-Loop (HITL) AI Employee system** that converts unstructured inputs into **controlled, auditable execution workflows** across real tools (Slack, Odoo, Email, Filesystem).

It is built to solve a critical problem:

👉 AI systems are powerful — but unsafe without control, visibility, and accountability.

This system ensures:

* structured execution
* human approval at critical steps
* deterministic behavior
* full auditability

This is not a chatbot.
This is a **state-driven AI operations system**.

---

## ⚙️ What Is Implemented

* Watcher-based task intake (filesystem + Gmail)
* Structured pipeline: Task → Plan → Approval → Execution
* Human-in-the-loop enforcement (no approval → no execution)
* Controlled execution via MCP integrations
* Multi-system actions (Slack, Odoo, Email, Filesystem)
* Append-only audit logging (JSONL)
* CEO reporting and summaries
* Deterministic orchestration with retry safety

---

## 🏆 What Gold Proves (Execution System)

The **Gold layer** is the core execution engine.

It proves that the system is:

* Deterministic (no randomness)
* Fully auditable and traceable
* Strictly controlled via HITL
* Capable of real multi-system execution
* End-to-end functional (input → execution → logs)
* Resume-safe and crash-safe

👉 Gold = **actual execution system**

---

## ☁️ What Platinum Adds (Observability Layer)

The **Platinum layer** enhances visibility and system clarity **without modifying execution logic**.

It adds:

* Cloud vs Local execution separation
* Asynchronous update lifecycle (`Incoming → Claimed → Processed → Gold`)
* Runtime visibility dashboard
* Non-executing cloud draft system
* Clear ownership and state tracking

⚠️ Platinum does NOT execute actions
⚠️ Platinum does NOT modify Gold logic

👉 Platinum = **observability + control clarity**

---

## 🔄 Demo Flow

MCP → Runtime → Watcher → Task → Plan → Approval → Artifact → Logs

This demonstrates:

* controlled execution
* human-in-the-loop enforcement
* full auditability
* deterministic system behavior

---

## ▶️ How to Run Demo

1. Check MCP:

   ```
   claude mcp list
   ```

2. Trigger watcher:

   ```
   "DEMO" | Set-Content dropbox\test.txt
   ```

3. Observe system flow:

* Needs_Action
* Plans
* Approval
* Artifacts
* Logs

---

## 🔄 System Flow

### Simplified Flow

Input → Task → Plan → Approval → Execution → Logs → Reporting

### Full Flow

MCP → Runtime → Watcher → Task → Plan → Approval → Artifact → Logs

---

## 🗂 Repository Structure (High-Level)

* `AI_Employee_Vault/` → system state, workflow, logs
* `watchers/` → perception layer (filesystem, Gmail, health)
* `tools/` → orchestration and execution scripts
* `ui/` → dashboard, HITL view, CEO view
* `evidence/` → proof for judges

---

## 🎬 Quick Demo (Judge-Safe)

1. Drop a file into `dropbox/`
2. Task appears in `AI_Employee_Vault/Needs_Action/`
3. System generates a plan → moves to `Pending_Approval/`
4. Manually approve → move to `Approved/`
5. System executes via MCP integrations
6. Outputs appear in:

   * `Artifacts/`
   * `Logs/`
   * `Briefings/`

---

# 🧩 Core Architecture

## 1. Input Layer (Watchers)

* Filesystem watcher
* Gmail intake bridge
* Manual task creation

➡ Converts raw input into structured tasks

---

## 2. Vault System (State Machine)

Needs_Action → Plans → Pending_Approval → Approved → Done

Acts as:

* system memory
* workflow engine
* single source of truth

---

## 3. AI Reasoning Layer

* Generates structured plans
* Explains intent
* Produces human-readable outputs

⚠️ Plans are advisory only

---

## 4. Human-in-the-Loop (HITL)

* Mandatory approval step
* No execution without approval
* Full decision trace

---

## 5. Controlled Execution Layer

* Executes only approved actions
* Uses MCP integrations
* Produces deterministic outputs

Examples:

* Slack actions
* Odoo operations
* Email sending
* File generation

---

## 6. Audit & Logging Layer

* JSONL append-only logs
* Full traceability
* Runtime logs

---

## 7. Reporting Layer

* CEO Briefings
* Scheduled reports
* Business insights

---

# 🔌 MCP Integrations

* Gmail
* GitHub
* Slack
* Google Calendar
* Filesystem
* Playwright
* Odoo
* Context7

All integrations are:

* controlled
* verified
* logged

---

# 🔒 System Guarantees

* No execution without approval
* No uncontrolled external actions
* Full audit trail
* Deterministic behavior
* Reproducible execution

---

# 🔁 Reliability

* Retry logic
* Crash-safe loop
* Lock-based execution
* Resume-safe system

---

# 🧪 Evidence & Verification

All proof stored in:

`/evidence/gold/`

Includes:

* logs
* artifacts
* MCP verification
* watcher outputs
* execution traces

---

# 📊 System Capabilities

* Autonomous task intake
* AI reasoning with human oversight
* Controlled execution
* Multi-system integration
* Scheduled automation
* Full traceability

---

# 🧠 What Makes This Different

This is NOT:

* a chatbot
* a simple automation script

This IS:

> A **Controlled AI Operations System**
> with human governance and production-grade architecture

---

# 🏁 Final Verdict

**ELITE GOLD + PLATINUM — COMPLETE ✅**

* Gold proves execution
* Platinum proves visibility
* System is safe, real, and production-ready

Ready for:

* Submission
* Demonstration
* Evaluation

---

# 🚫 Gold Freeze Rule

Do NOT:

* modify core system
* restructure architecture
* introduce new features

Gold is locked.

---

# ▶️ Next Step

Proceed to:

👉 Platinum extensions and scaling

---

# ❤️ Closing Note

This system proves that AI can be:

* controlled
* safe
* auditable
* reliable

—not just automated.
