# Architecture Standard

## Purpose

Define clear dependency boundaries without forcing every service into the same number of folders. Architecture should match business complexity while keeping transport, business policy, persistence, and external infrastructure independently testable.

## Default Dependency Model

```text
API / Event Handlers
        ↓
Application Services
        ↓
Domain Model
        ↑
Ports / Contracts
        ↑
Persistence and Infrastructure Adapters
```

The diagram expresses dependency direction, not a mandatory physical folder count.

## Responsibilities

### API or Event Handler

- bind and validate transport input
- map request/event models to application input
- invoke one application use case
- map outcomes to transport responses
- avoid business rules and direct persistence access

### Application Service

- orchestrate one use case
- coordinate transactions and authorization
- call domain behavior and repository/capability ports
- define idempotency and ordering boundaries where required
- avoid vendor SDK details

### Domain

- express business rules, invariants, entities, value objects, and domain events
- remain independent of HTTP, messaging, persistence, and vendor SDK frameworks
- stay simple for CRUD-oriented services; use a richer model only when rules justify it

### Ports and Contracts

- define stable boundaries for repositories and meaningful external capabilities
- use domain/application language rather than vendor terminology where practical
- avoid speculative interfaces that have no meaningful test or substitution value

### Persistence and Infrastructure Adapters

- implement repository and capability contracts
- own SDK, database, serialization, retry, and provider-specific details
- expose production and explicitly selected local implementations
- contain no business policy

## Architecture by Complexity

### Simple CRUD Service

A controller/API layer, application service, DTOs, and persistence adapter may be sufficient. Do not add domain-event or port layers merely to satisfy a template.

### Business-Rule-Heavy Service

Use domain entities/value objects and domain-owned repository or capability contracts when invariants, transaction behavior, or cross-aggregate decisions justify them.

### Integration-Heavy Service

Use explicit capability contracts and adapters when provider semantics, failure handling, local substitutes, testing, or migration flexibility matter.

## Dependency Rules

1. Controllers/handlers do not call database or vendor SDK clients directly.
2. Domain logic does not depend on transport or infrastructure frameworks.
3. Application logic depends on contracts, not concrete provider implementations, when a meaningful boundary exists.
4. Adapters may depend on provider SDKs and mapping code; inner layers must not.
5. Cross-layer shortcuts require an architecture decision explaining why they improve rather than weaken the design.
6. Shared utilities must not become an unowned dumping ground.

## Framework Pragmatism

A persistence annotation on a domain object may be acceptable in a deliberately simple active-record or transaction-script service when documented. Do not claim “zero framework dependencies” while using framework annotations without an explicit architecture choice.

## Transactions and Consistency

- define the local transaction boundary explicitly
- roll back related database changes when a unit of work fails
- use outbox/inbox, idempotency, or saga patterns only when requirements justify distributed consistency handling
- do not imply that a local adapter provides the same ordering or durability as a production broker

## Local Adapters and Production Degradation

Local adapter selection belongs to [Local Adapter Strategy](local-adapter-strategy.md). Production dependency failure behavior belongs to [Production Dependency Failure and Degradation](fallback-strategy.md). Do not merge the two decisions.

## LLM Instructions

- Choose the smallest architecture that protects the required boundaries.
- Explain concrete coupling or testability risks instead of failing code because a folder is absent.
- Do not introduce ports, domain layers, or adapters without a justified requirement.
- Keep production provider details outside domain and application logic when a stable boundary is needed.
- Record exceptions as architecture decisions rather than silently breaking the dependency model.

## Review Checklist

- [ ] Architecture matches service complexity
- [ ] Transport, business policy, and infrastructure responsibilities are clear
- [ ] Controllers/handlers avoid business logic and direct data access
- [ ] Domain/application code avoids vendor SDK coupling where a capability boundary is justified
- [ ] Transactions, idempotency, ordering, and consistency are explicit where relevant
- [ ] Local adapters and production degradation are separate decisions
- [ ] Exceptions are documented with rationale

## References

- [Engineering Principles](engineering-principles.md)
- [Capability Contracts](../contracts/)
- [Prompt-Driven Development Workflow](prompt-driven-development-workflow.md)
