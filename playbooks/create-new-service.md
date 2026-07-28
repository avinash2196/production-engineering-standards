# Workflow: Create a New Service

## Purpose

Create a Java Spring Boot or Python FastAPI service through reviewed milestones rather than generating a large codebase from one prompt.

## Required Lifecycle

> **Requirements → Plan → Human Review → Implementation Plan → Human Review → RED Tests → GREEN Code → Refactor → Final Review**

Reference: [Prompt-Driven Development Workflow](../standards/prompt-driven-development-workflow.md)

## 1. Review Requirements

Identify only the decisions needed for the requested service:

- service purpose and use cases
- API, event, or scheduled-work contracts
- stack and runtime target
- persistence requirements
- external messaging, cache, storage, or secret-provider capabilities actually needed
- validation and business rules
- transaction, idempotency, ordering, and consistency requirements
- data classification and explicitly required controls
- availability and operational expectations

Do not add Kafka, Redis, object storage, a domain layer, or local adapters simply because the repository supports them.

## 2. Create and Review the Plan

Run `/create-plan` or create:

```text
docs/.ai/Plan.md
```

Use the [Plan Template](../templates/docs/plan-template.md). Define scope, milestones, dependencies, risks, exclusions, and success criteria. Do not write tests or implementation.

Obtain human approval before continuing.

## 3. Plan One Milestone

For the next approved milestone, run `/create-implementation-plan` and create:

```text
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
```

The Implementation Plan must identify:

- current repository state
- exact files
- positive and negative tests
- expected RED failure
- minimal production changes for GREEN
- transaction, idempotency, adapter, degradation, security, and observability decisions where applicable
- permitted refactoring
- out-of-scope work and commands

Obtain human approval before changing tests or source.

## 4. Implement the Milestone

Run `/implement-approved-plan`.

### RED

- create or update only approved tests
- run the focused command
- confirm failure is caused by missing approved behavior

### GREEN

- implement the smallest approved production change
- run focused tests, then relevant regression tests

### REFACTOR

- improve structure without changing behavior
- keep tests GREEN after each meaningful change

Update the Implementation Plan with evidence and changed files.

## 5. Recommended Milestone Order

A service may use this sequence when appropriate:

1. requirements and API/event contract
2. project skeleton and typed configuration
3. transport/contract tests and minimal transport implementation
4. domain/application tests and minimal business implementation
5. persistence tests and implementation
6. external adapter contract tests and implementation
7. security and authorization
8. observability and operational behavior
9. production readiness and final review

Do not combine all milestones into one unreviewable implementation.

## 6. Adapter Decisions

Use [Local Adapter Strategy](../standards/local-adapter-strategy.md) for development/CI substitutes and [Production Dependency Failure and Degradation](../standards/fallback-strategy.md) for live failure behavior.

Standard selectors:

```text
MESSAGING_ADAPTER=kafka|pubsub|db|inmemory
CACHE_ADAPTER=redis|jsonfile|inmemory
STORAGE_ADAPTER=s3|gcs|local
SECRET_ADAPTER=vault|secretmanager|env
```

Only document values implemented by the service. Local-only values must fail startup in production.

## 7. Final Review

Run applicable checks:

- focused and full relevant tests
- formatter/linter/static analysis
- API/event contract validation
- repository or project validators
- security and dependency scans
- architecture, distributed-systems, and production-readiness reviews

A generated scaffold is not production-ready until the applicable [Definition of Done](../standards/definition-of-done.md) is satisfied.

## Completion Criteria

- [ ] Requirements are grounded and not invented
- [ ] Plan and every milestone Implementation Plan were reviewed
- [ ] Tests preceded production code
- [ ] RED, GREEN, and refactor evidence is recorded
- [ ] Dependencies and architecture match actual complexity
- [ ] Local adapter and production degradation decisions are separate
- [ ] Final validation passes or gaps are explicitly documented
