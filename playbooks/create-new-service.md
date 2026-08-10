# Workflow: Create a New Service

## Purpose

Create a Java Spring Boot or Python FastAPI service through small reviewed PDD milestones rather than generating a large codebase from one prompt.

## Required Lifecycle

> **Requirements → Plan → Human Review → Implementation Plan → Human Review → RED Tests → GREEN Code → Refactor → Final Review**

For behavior-changing work, RED, GREEN, and optional REFACTOR are separate Plan milestones. Each repository-changing milestone has its own Implementation Plan and review gate.

Reference: [Prompt-Driven Development Workflow](../standards/prompt-driven-development-workflow.md)

## 1. Review Requirements

Identify only decisions needed for the requested service/current planning boundary:

- service purpose and use cases
- API, event, scheduled-work, or other required contracts
- stack and runtime target
- persistence requirements
- external messaging, cache, storage, or secret-provider capabilities actually needed
- validation and business rules
- transaction, concurrency, idempotency, ordering, and consistency requirements when applicable
- data classification and explicitly required controls
- availability and operational expectations when explicitly required

Use repository evidence when available. If a material decision is unresolved, ask and stop. Do not add Kafka, Redis, object storage, a domain layer, local adapters, or a compliance regime simply because the repository supports them.

## 2. Create and Review the Plan

Run `/create-plan` or create:

```text
docs/.ai/Plan.md
```

Use the [Plan Template](../templates/docs/plan-template.md). Define scope, requirements, risks, exclusions, success criteria, and the phase-specific milestone sequence.

For each behavior slice:

1. RED milestone — tests/checks only
2. GREEN milestone — minimum production implementation
3. REFACTOR milestone — optional and only when justified

A foundation or approved artifact may be its own non-behavior milestone.

Obtain human approval before continuing.

## 3. Plan One Milestone

For the next approved Plan milestone, run `/create-implementation-plan` and create:

```text
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
```

The Implementation Plan must declare the phase and authorize only that phase.

### RED Implementation Plan

Include:

- exact test/check files
- approved positive/negative/necessary boundary cases
- expected RED failure and why it is valid
- focused command
- out-of-scope work

Do not include production implementation or refactoring.

### GREEN Implementation Plan

Require valid predecessor RED evidence and include:

- exact production files
- minimum production changes
- applicable transaction/idempotency/degradation/adapter/security/observability decisions supported by approved requirements
- focused and regression commands
- out-of-scope work

Do not include refactoring.

### REFACTOR Implementation Plan

Require a verified GREEN baseline and include:

- concrete cleanup/design issue
- exact files and structural changes
- behavior/contracts that must remain unchanged
- before/after verification commands

Do not include feature behavior or defect fixes.

Obtain human approval before executing the milestone.

## 4. Execute Only the Approved Milestone

### RED

Use `/generate-tests`:

- create/update only approved tests/checks
- run the focused command
- confirm valid RED
- record evidence
- stop before production implementation

### GREEN

Use `/implement-approved-plan`:

- verify valid predecessor RED evidence
- implement the smallest approved production change
- run focused and relevant regression tests
- record evidence
- stop after GREEN

### REFACTOR

Use `/refactor-code` only when a separate approved REFACTOR milestone exists:

- start from verified GREEN
- perform only approved structural cleanup
- preserve behavior
- run before/after verification
- stop after the milestone

Do not move to the next Plan milestone automatically. Create and review its Implementation Plan first.

## 5. Example Milestone Decomposition

A service may use:

1. Project/Test Foundation — FOUNDATION
2. API/Event Contract Tests — RED
3. API/Event Minimal Implementation — GREEN
4. Domain/Application Tests — RED
5. Domain/Application Minimal Implementation — GREEN
6. Persistence/Integration Tests — RED when required
7. Persistence/Integration Implementation — GREEN when required
8. Reliability/Security/Operational RED/GREEN pairs when explicitly required
9. REFACTOR milestones only where concrete cleanup is justified
10. Production wiring/readiness milestones supported by approved requirements

This sequence is guidance, not a fixed architecture. Keep milestones small and do not pull later dependencies, configuration, abstractions, or infrastructure forward.

## 6. Adapter Decisions

Use [Local Adapter Strategy](../standards/local-adapter-strategy.md) for development/CI substitutes and [Production Dependency Failure and Degradation](../standards/fallback-strategy.md) for live failure behavior.

Only document/select capabilities actually used by the service. Local-only adapters must not silently activate in production and their reduced guarantees must be explicit.

## 7. Final Review

Run applicable checks:

- focused and full relevant tests
- formatter/linter/static analysis
- API/event contract validation
- repository/project validators
- applicable security/dependency scans
- architecture/distributed-systems/production-readiness reviews when relevant

A generated scaffold is not production-ready until the applicable [Definition of Done](../standards/definition-of-done.md) is satisfied.

## Completion Criteria

- [ ] Requirements are grounded and material gaps were clarified
- [ ] Plan was reviewed
- [ ] Every repository-changing milestone had its own reviewed Implementation Plan
- [ ] RED and GREEN were separate milestones for behavior-changing work
- [ ] GREEN milestones had valid predecessor RED evidence
- [ ] REFACTOR milestones, when present, were separate, justified, and behavior-preserving
- [ ] Dependencies and architecture match actual approved complexity
- [ ] Local-adapter and production-degradation decisions remain separate
- [ ] Final validation passes or gaps are explicitly documented
