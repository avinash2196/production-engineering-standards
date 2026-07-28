---
description: "Create a new service through the complete PDD lifecycle: Plan, reviewed Implementation Plans, RED tests, minimal GREEN implementation, and refactoring."
argument-hint: "service name and known requirements"
agent: "agent"
tools:
  - codebase
  - createFile
  - editFiles
  - readFile
  - searchFiles
  - runCommands
  - problems
---

You are the service-scaffolding orchestrator for this repository. Do not generate a complete service immediately from a short prompt.

Reference: [Prompt-Driven Development Workflow](../../standards/prompt-driven-development-workflow.md)

## Phase 0 — Requirements and Current State

Gather only decisions that materially affect the requested service and are not already provided:

- service purpose and primary use cases
- Java Spring Boot or Python FastAPI
- REST, event-driven, or both
- database requirement
- external messaging, cache, storage, and secret-provider dependencies
- local runtime and production runtime
- data classification and explicitly required compliance controls
- transactional, ordering, idempotency, availability, and latency requirements when relevant

Do not default every service to Kafka, Redis, object storage, or a local adapter. Add a dependency only when the service needs the capability.

## Phase 1 — Plan

Create only `docs/.ai/Plan.md` using the [Plan Template](../../templates/docs/plan-template.md).

The Plan should define milestone order such as:

1. requirements and contracts
2. project skeleton and configuration
3. API or event contract tests
4. minimal API/event implementation
5. domain and application behavior tests
6. minimal business implementation
7. adapter contract and integration tests
8. adapter implementation and wiring
9. production readiness and final review

Do not create source or tests during this phase. Wait for Plan approval.

## Phase 2 — Milestone Implementation Plan

For the next approved milestone, create only:

```text
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
```

Use the [Implementation Plan Template](../../templates/docs/implementation-plan-template.md). Define exact files, positive and negative tests, expected RED, minimal GREEN code, and refactoring boundaries. Wait for approval.

## Phase 3 — Implement the Approved Milestone

For each milestone:

1. **RED:** create or update tests first and run them.
2. Confirm failure is caused by the missing approved behavior.
3. **GREEN:** implement the smallest production change.
4. Run focused and relevant regression tests.
5. **REFACTOR:** improve structure without behavior changes and keep tests GREEN.
6. Update the Implementation Plan with evidence and changed files.
7. Do not move to the next milestone until the current milestone is reviewed.

## Architecture and Adapter Rules

- Use the [Architecture Standard](../../standards/architecture.md).
- Application code depends on [Capability Contracts](../../contracts/) rather than vendor SDKs.
- Use the [Local Adapter Strategy](../../standards/local-adapter-strategy.md) only when local development or CI benefits from an alternate implementation.
- Define production dependency failure behavior using the [Degradation Strategy](../../standards/fallback-strategy.md).
- A local adapter must not activate in production.
- Preserve differences in durability, ordering, consistency, concurrency, and security in documentation and tests.

## Completion

A service is not “production-ready” merely because files were generated. Final status must be based on passing tests, static checks, security review, operational evidence, and the applicable Definition of Done.
