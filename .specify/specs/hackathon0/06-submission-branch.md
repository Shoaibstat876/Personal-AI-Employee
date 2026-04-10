SUBMISSION BRANCH SPEC — PERSONAL AI EMPLOYEE (HACKATHON 0)

Purpose

This document defines the role and rules of the final submission branch for the Personal AI Employee system. It ensures that the system remains stable, consistent, and reliable during evaluation.

The submission branch represents the final state of the system and must reflect a complete, working, and verifiable implementation.

Submission Branch

The official submission branch is:

platinum-final-demo

This branch contains:

the complete Gold workflow
the complete Platinum layer
all logs and artifacts required for proof
final documentation and UI

It is the version intended for demonstration and evaluation.

Branch Role

The submission branch acts as a stable snapshot of the system.

It represents:

final system behavior
verified execution flow
complete evidence structure
judge-ready presentation

It is not a development branch.

Stability Requirement

The submission branch must remain stable at all times.

Rules:

no breaking changes
no experimental modifications
no structural changes to workflow
no changes that affect execution behavior

Only safe and controlled updates are allowed.

Allowed Changes

The following changes are allowed:

documentation improvements
clarity enhancements
wording fixes
addition of specification files
non-impactful presentation updates

These changes must not affect system behavior.

Restricted Changes

The following changes are not allowed:

modifying runtime scripts
changing workflow logic
altering logs or artifacts
renaming core folders
introducing new untested features
removing existing evidence

These changes can invalidate system proof.

Evidence Integrity

All logs and artifacts in the submission branch must remain unchanged.

Rules:

logs must remain append-only
artifacts must reflect real execution
no cleanup or rewriting of evidence
no artificial enhancement of outputs

Evidence must remain authentic.

Branch Integrity

The submission branch must preserve:

repository structure
workflow behavior
file-based state transitions
task_id continuity
existing commit history

Any change that breaks these properties is not allowed.

Relationship to Other Branches

Other branches may exist for development, but they are not part of the submission.

Only the submission branch:

is evaluated
contains final proof
represents system behavior

All improvements must be carefully merged into this branch without breaking stability.

Spec Layer Integration

The .specify layer is allowed in the submission branch as a governance and documentation layer.

Rules:

it must not modify runtime behavior
it must not contradict existing evidence
it must reflect actual system behavior
it must improve clarity without altering functionality

It exists to strengthen presentation, not to change the system.

Demonstration Readiness

The submission branch must be ready for demonstration at any time.

This means:

workflow must run correctly
logs must be available
artifacts must be accessible
UI must reflect system state
documentation must be aligned

No setup or repair should be required during demo.

Consistency Requirement

All parts of the system must remain consistent:

workflow
logs
artifacts
documentation
specifications

If inconsistency appears, it must be resolved without breaking existing proof.

Final Guarantees

The submission branch guarantees that:

the system is complete
the system is stable
the system is verifiable
the system is ready for evaluation

It serves as the final representation of the project.

Final Understanding

The submission branch is not just a code branch. It is the official version of the system presented for evaluation.

It must remain stable, truthful, and evidence-backed, ensuring that what is shown can be trusted and verified.