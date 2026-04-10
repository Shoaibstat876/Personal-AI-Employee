# OVERVIEW — PERSONAL AI EMPLOYEE (HACKATHON 0)

## Purpose

This document defines the complete system overview of the Personal AI Employee built for Hackathon 0. The system demonstrates a controlled, auditable, human-supervised AI workflow that transforms incoming tasks into approved and executed actions with full traceability and evidence.

## System Definition

The Personal AI Employee is a workflow-driven AI system, not an autonomous agent. It is designed to receive inputs from external sources, convert inputs into structured tasks, generate plans for execution, enforce human approval (HITL), execute only approved actions, and produce logs and artifacts as proof. The system prioritizes control over automation, traceability over abstraction, and evidence over claims.

## Core Workflow

The system follows a deterministic lifecycle: Intake → Task → Plan → Pending Approval → Approved → Execution → Logs → Done. Each stage is represented through filesystem state and artifacts. No step is hidden, no step is skipped, every transition is traceable, and every action produces evidence.

## System Architecture

The system operates through layered responsibilities. The Intake Layer (Watchers) captures incoming data from sources such as filesystem inputs and email bridges and converts them into structured tasks. The Planning Layer transforms tasks into structured plans by parsing task content and preparing actions for review. The Human-in-the-Loop (HITL) layer acts as the control boundary by reviewing generated plans and approving or rejecting execution, ensuring no unintended actions occur. The Execution Layer performs approved actions in a controlled environment, such as creating records, preparing or sending messages, or generating content, and only executes after approval. The Logging and Evidence Layer captures all activity including workflow logs, execution logs, approval logs, and generated artifacts, ensuring that all behavior is verifiable and append-only.

## Gold Layer (Execution Proof)

The Gold layer demonstrates that the system executes the full workflow, enforces HITL control, maintains task traceability, produces real logs and artifacts, and behaves deterministically. Gold represents working, proven capability and serves as the foundation of system credibility.

## Platinum Layer (Control and Visibility)

The Platinum layer enhances the system without changing its core behavior. It introduces cloud versus local responsibility separation, update ingestion and processing flow, runtime visibility, and system-level observability. In this model, the cloud proposes and drafts work, while the local system reviews, approves, and executes actions. Execution authority exists only in the local system.

## Evidence Model

The system is evaluated based on logs, artifacts, and file-based workflow transitions. Documentation must always match actual outputs. If documentation and evidence differ, evidence is considered correct.

## Design Principles

The system is built on deterministic workflow, human-controlled execution, explicit state transitions, append-only logging, filesystem transparency, and clear separation of concerns.

## Non-Goals

The system intentionally does not operate as a fully autonomous agent, does not execute actions without approval, does not hide internal behavior, and does not simulate capabilities without proof. These constraints are deliberate to ensure safety and auditability.

## Final Summary

The Personal AI Employee is a controlled AI workflow system that converts inputs into structured tasks, enforces human approval before execution, executes actions in a bounded environment, and produces verifiable logs and artifacts. It is designed to be auditable, deterministic, evidence-driven, and submission-ready.