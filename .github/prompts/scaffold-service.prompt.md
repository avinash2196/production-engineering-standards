---
description: "Create a new service through PDD with separate reviewed RED, GREEN, and optional REFACTOR milestones."
argument-hint: "service name and known requirements"
agent: "agent"
tools:
  - read
  - search
  - edit
  - execute
---

You are the service-scaffolding orchestrator for this repository. Do not generate a complete service immediately from a short prompt.

Reference: [Prompt-Driven Development Workflow](../../standards/prompt-driven-development-workflow.md)

## Phase 0 — Requirements and Current State

Use the repository Requirements Analysis skill when available. Gather only decisions that materially affect the current planning boundary and are not already explicit or repository-confirmed, such as:

- service purpose and primary use cases
- Java Spring Boot or Python FastAPI
- REST, event-driven, scheduled, or another explicitly required interaction style
- database/persistence requirements
- external messaging, cache, storage, and secret-provider dependencies actually required
- local runtime and production runtime when needed for the current milestone
- data classification and explicitly required compliance controls
- transactional, ordering, idempotency, availability, and latency requirements when relevant

If a material decision required for planning is unresolved, ask numbered clarification questions and stop. Do not default every service to Kafka, Redis, object storage, security libraries, observability libraries, a local adapter, or an assumed compliance regime.

## Phase 1 — Create and Review the Plan

Create only `docs/.ai/Plan.md` using the [Plan Template](../../templates/docs/plan-template.md).

The Plan uses small human-controlled milestones. For each behavior slice:

1. create a **RED milestone** for tests/checks only;
2. create a **GREEN milestone** for the minimum production behavior;
3. add a separate **REFACTOR milestone only when justified**.

A project/test foundation or another real non-behavior artifact may be its own milestone. Use fewer behavior slices when the service is small; do not create empty milestones merely to match an example.

A possible sequence is:

1. Project and test foundation
2. Transport/contract tests — RED
3. Transport/contract implementation — GREEN
4. Application/domain tests — RED
5. Application/domain implementation — GREEN
6. Persistence/integration tests — RED, when required
7. Persistence/integration implementation — GREEN, when required
8. Separate REFACTOR milestones only where concrete cleanup is justified
9. Production wiring/readiness milestones supported by approved requirements

Do not create source or tests during Plan creation. Obtain human Plan approval before creating a milestone Implementation Plan.

## Phase 2 — Plan One Approved Milestone

For the next approved Plan milestone, create only:

```text
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
```

Use the [Implementation Plan Template](../../templates/docs/implementation-plan-template.md).

The Implementation Plan is **phase-specific**:

- RED: tests/checks and expected RED only
- GREEN: minimum production changes and GREEN verification only; predecessor valid RED required
- REFACTOR: behavior-preserving cleanup only; predecessor GREEN baseline required
- FOUNDATION/OTHER: only the approved non-behavior outcome

Do not combine multiple phase authorizations in one Implementation Plan.

Obtain human approval before executing that milestone.

## Phase 3 — Execute One Approved Milestone

Execute only the currently approved phase:

- RED → use `/generate-tests`; establish valid RED and stop.
- GREEN → use `/implement-approved-plan`; reach GREEN and stop.
- REFACTOR → use `/refactor-code`; preserve GREEN and stop.
- FOUNDATION/OTHER → use `/implement-approved-plan` for only the approved non-behavior scope.

After execution, record evidence and changed files. **Do not move to the next Plan milestone automatically.** The next milestone requires its own Implementation Plan and human approval.

For a brand-new repository without an executable test harness, use a dedicated project/test foundation milestone for the minimum build/test infrastructure needed to execute meaningful tests. Do not implement application behavior in that milestone.

## Architecture and Adapter Rules

- Use the [Architecture Standard](../../standards/architecture.md).
- Add framework and vendor dependencies only when selected by the approved current milestone.
- Application code depends on [Capability Contracts](../../contracts/) rather than vendor SDKs when a stable boundary is actually needed.
- Use the [Local Adapter Strategy](../../standards/local-adapter-strategy.md) only when local development or CI benefits from an alternate implementation.
- Define production dependency failure behavior using the [Degradation Strategy](../../standards/fallback-strategy.md).
- A local adapter must not activate silently in production.
- Preserve differences in durability, ordering, consistency, concurrency, and security in documentation and tests where applicable.

## Completion

A service is not production-ready merely because files were generated. Final status depends on completed approved milestones, passing tests/checks, applicable security/resilience/operational evidence, and the [Definition of Done](../../standards/definition-of-done.md).
