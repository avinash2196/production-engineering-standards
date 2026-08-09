# Production Engineering Standards — Copilot Instructions

Use these instructions when planning, implementing, testing, reviewing, or refactoring code in this repository.

## Mandatory Delivery Workflow

For any task that changes production behavior, contracts, shared standards, reliability, security, compliance, or four or more files, follow this sequence:

> **Requirements → Plan → Human Review → Implementation Plan → Human Review → RED Tests → GREEN Code → Refactor → Final Review**

1. Create or update `docs/.ai/Plan.md` using the [Plan Template](../templates/docs/plan-template.md).
2. Do not include complete production code in the Plan.
3. After Plan approval, create a milestone-specific `docs/.ai/NNN_Implementation_Plan_<Milestone>.md` using the [Implementation Plan Template](../templates/docs/implementation-plan-template.md).
4. Do not edit production source until the Implementation Plan is approved.
5. Write or update tests first and confirm RED for the expected missing behavior.
6. Implement only enough production code to reach GREEN.
7. Refactor separately while keeping all relevant tests GREEN.
8. Complete final review and repository validation.

Full workflow: [Prompt-Driven Development Workflow](../standards/prompt-driven-development-workflow.md)

## Default Architecture

Use architecture appropriate to the service's business complexity. Preserve these dependency rules:

| Area | Responsibility | Must Avoid |
|---|---|---|
| **API/Controller** | Transport handling, DTO binding, validation, response mapping | Business rules and direct data access |
| **Application Service** | Use-case orchestration, transactions, authorization coordination | Direct vendor SDK usage |
| **Domain** | Business rules, entities, value objects, domain events | Transport and infrastructure concerns |
| **Ports/Contracts** | Repository and external-capability abstractions | Vendor-specific implementation details |
| **Infrastructure Adapters** | Database, messaging, cache, storage, and secret-provider implementations | Business policy |

Simple CRUD services may use fewer structural layers when the dependency direction remains clear. Do not add folders merely to satisfy a diagram.

Full rules: [Architecture Standard](../standards/architecture.md)

## Capability Interfaces

Application and domain code depend on capability contracts rather than vendor SDKs:

- [MessagePublisher](../contracts/MessagePublisher.md) and [MessageSubscriber](../contracts/MessageSubscriber.md)
- [CacheProvider](../contracts/CacheProvider.md)
- [ObjectStorageProvider](../contracts/ObjectStorageProvider.md)
- [SecretProvider](../contracts/SecretProvider.md)
- [ConfigProvider](../contracts/ConfigProvider.md)

Introduce an abstraction when it protects a meaningful boundary, supports testing, or permits multiple implementations. Do not create speculative interfaces without a justified use case.

## Local Adapter Configuration

Local adapters help developers and CI exercise behavior without every external platform. They are not automatic production failover mechanisms.

| Variable | Production adapters | Local-only adapters |
|---|---|---|
| `MESSAGING_ADAPTER` | `kafka`, `pubsub` | `db`, `inmemory` |
| `CACHE_ADAPTER` | `redis` | `jsonfile`, `inmemory` |
| `STORAGE_ADAPTER` | `s3`, `gcs` | `local` |
| `SECRET_ADAPTER` | `vault`, `secretmanager` | `env` |

Rules:

1. Adapter selection uses typed configuration.
2. Local-only adapter activation emits a structured warning and metric.
3. Reduced durability, ordering, consistency, concurrency, and security guarantees are documented.
4. Production startup fails when a local-only adapter is selected.
5. Testcontainers or official emulators may be preferable to a custom local adapter.

Details: [Local Adapter Strategy](../standards/local-adapter-strategy.md)

## Production Dependency Failure Behavior

Every external dependency must have documented failure behavior. Select based on correctness and business impact:

- fail fast
- fail closed
- retry with bounded backoff
- circuit break
- queue durably for later processing
- serve stale data
- bypass a non-critical capability
- provide reduced functionality

Do not silently replace a durable production dependency with an in-memory implementation. Security, authorization, secrets, and correctness controls normally fail closed.

Details: [Production Dependency Failure and Degradation](../standards/fallback-strategy.md)

## Engineering Rules

1. Domain logic must not depend on web, persistence, or vendor SDK frameworks unless a project-specific architecture decision explicitly adopts an active-record model.
2. Secrets are accessed through the configured secret-provider boundary. Environment variables are permitted only for explicitly local development adapters.
3. External calls define timeouts and documented failure behavior.
4. Transaction and idempotency boundaries are explicit where duplicate or partial processing could occur.
5. Collection-fetching paths are reviewed for N+1 behavior using cardinality and pagination context.
6. Logs must be structured and avoid secrets, PHI, and unnecessary PII.
7. Metrics and traces are added according to service criticality, runtime, and support needs.
8. Numeric method or class-size thresholds are review signals, not automatic failures.
9. Tests cover approved positive and negative behavior without inventing requirements.
10. Human review remains required for commits and production readiness decisions.

## Rule Classification

When reporting a standards finding, classify it as:

- `AUTOMATED` — a test, validator, static check, or CI gate fails on violation
- `REVIEWED` — engineering judgment is required
- `ADVISORY` — a default recommendation with justified exceptions

Do not call a rule “enforced” unless an executable mechanism blocks the violation.

## Key References

| Concern | Document |
|---|---|
| PDD lifecycle | [Prompt-Driven Development Workflow](../standards/prompt-driven-development-workflow.md) |
| Agent execution | [Agent Execution Standard](../standards/agent-execution.md) |
| Coding standards | [Coding Standards](../standards/coding-standards.md) |
| DTO and API boundaries | [DTO Guidelines](../standards/dto-guidelines.md) |
| Security | [Security Standards](../standards/security/security-standards.md) |
| Observability | [Observability](../standards/observability.md) |
| Unit testing | [Unit Testing](../standards/testing/unit-testing.md) |
| Integration testing | [Integration Testing](../standards/testing/integration-testing.md) |
| Production readiness | [Production Readiness](../standards/production-readiness.md) |
| Enforcement status | [Enforcement Matrix](../docs/enforcement-matrix.md) |

## Stack Guidance

- [Java 21 and Spring Boot 3.x](../stacks/java-springboot/java-spring.md)
- [Python 3.12+ and FastAPI](../stacks/python-fastapi/python-backend.md)

## Available Prompt Workflows

- `/create-plan` — create or update `docs/.ai/Plan.md`; no implementation
- `/create-implementation-plan` — create the exact milestone implementation plan; no source changes
- `/implement-approved-plan` — run RED → GREEN → REFACTOR from an approved implementation plan
- `/scaffold-service` — orchestrate service creation through all planning and test gates
- `/generate-tests` — create tests only and verify RED when behavior is not implemented
- `/refactor-code` — refactor only from a GREEN baseline
- `/review-code`, `/review-architecture`, `/review-distributed-systems`, `/review-production-readiness` — evidence-based reviews
- `/compliance-review`, `/review-hipaa` — engineering control reviews, not legal certification
