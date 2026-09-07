# Application Copilot Instructions

Use this file as a starter for an application adopting the production-engineering-standards PDD workflow.

Replace the application-specific placeholders before use.

## Application Context

- Runtime: <runtime/version>
- Framework: <framework/version>
- Build system: <build system>
- Persistence: <database or no persistence>
- Verification commands: <commands>

## Approved Sources of Context

Before starting a task, review the relevant approved artifacts for the current work, including when present:

- requirements,
- `docs/.ai/Plan.md`,
- approved API/external contract,
- approved milestone Implementation Plan,
- current source code and tests related to the task.

The active prompt defines the current authorization boundary.

## Clarification Before Action

Do not invent, assume, or silently resolve material information.

If missing, ambiguous, or contradictory information materially affects the correctness or scope of the current task:

1. ask the minimum focused clarification questions required;
2. do not create or update the dependent artifact;
3. stop and wait for the user's response.

Do not use an Open Questions section as a substitute for required clarification.

## Scope Control

- Do not invent requirements, non-functional requirements, business rules, or validation rules.
- Do not pull future milestone work into the current task.
- Change only files authorized by the active prompt and approved Implementation Plan.
- Do not introduce unrelated dependencies, infrastructure, observability, resilience, or architecture changes.
- Do not rewrite approved artifacts merely to match implementation.

## Artifact Authority

- Requirements define intended behavior and constraints.
- Plan defines approved scope and milestone sequence.
- API/external contract defines approved externally observable behavior when applicable.
- Implementation Plan defines how the current milestone will be executed.
- Tests provide executable evidence.
- Production code implements the approved behavior.

If authoritative artifacts materially conflict, stop and surface the conflict for human review.

## Plan Integrity

After Plan approval:

- do not change milestone definitions during milestone execution;
- update only milestone execution/status information after verified success criteria pass;
- require explicit replanning and human review for scope or milestone changes.

## PDD Authorization Boundaries

For behavior-changing work:

**Requirements → Plan → Human Review → API/External Contract when applicable → Human Review → Implementation Plan → Human Review → RED → GREEN → optional REFACTOR → Final Review**

RED, GREEN, and REFACTOR are separate authorization boundaries.

Completing one phase does not authorize the next.

## Verification

Do not claim a build, test, validator, migration, or command passed unless it was actually executed successfully or evidence was explicitly supplied.

## Human Review

Human review is required for:

- material requirement interpretation,
- Plan approval,
- API/external contract approval when applicable,
- Implementation Plan approval,
- architecture trade-offs,
- production-readiness decisions,
- exceptions to approved scope.
