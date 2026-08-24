# Production Engineering Standards — Copilot Instructions

Use these instructions when planning, implementing, testing, reviewing, or refactoring code in this repository.

## Mandatory Delivery Workflow

For any task that changes production behavior, contracts, shared standards, reliability, security, compliance, or four or more files, follow this sequence:

> **Requirements → Plan → Human Review → Implementation Plan → Human Review → RED Tests → GREEN Code → Refactor → Final Review**

Apply that sequence through separate human-controlled Plan milestones:

1. Create or update `docs/.ai/Plan.md` using the [Plan Template](../templates/docs/plan-template.md).
2. Resolve material requirement ambiguity before Plan creation; do not invent missing behavior, controls, infrastructure, or non-functional requirements.
3. For behavior-changing work, create separate `RED` and `GREEN` milestones. Add a separate `REFACTOR` milestone only when concrete refactoring is justified.
4. After Plan approval, create one milestone-specific `docs/.ai/NNN_Implementation_Plan_<Milestone>.md` for the **current phase only** using the [Implementation Plan Template](../templates/docs/implementation-plan-template.md).
5. Obtain human approval before executing that milestone.
6. RED milestones modify tests/checks only, prove valid RED, record evidence, and stop.
7. GREEN milestones require valid predecessor RED evidence plus their own approved GREEN Implementation Plan; implement only enough production behavior to reach GREEN, record evidence, and stop.
8. REFACTOR milestones are optional, require a verified GREEN baseline plus their own approved REFACTOR Implementation Plan, preserve behavior, and stop.
9. Do not automatically advance to the next milestone. An end-to-end request does not waive these review gates for behavior-changing work.
10. Complete final review and repository validation after the required milestone chain is complete.

Full workflow: [Prompt-Driven Development Workflow](../standards/prompt-driven-development-workflow.md)

## Requirements Gate

Before creating or materially updating `docs/.ai/Plan.md`, apply the [Requirements Analysis Skill](skills/requirements-analysis/SKILL.md) or the equivalent behavior defined there.

- Separate facts that are explicit in the request from facts confirmed by the repository.
- Do not convert common architecture practices, framework defaults, industry conventions, or prior examples into requirements.
- If missing or contradictory information materially affects the current Plan's behavior, contract, data handling, security/compliance decision, persistence/integration behavior, test expectations, or milestone boundaries, ask numbered clarification questions and stop before creating the Plan.
- Ask the smallest set of questions needed for the current planning boundary. Do not ask about decisions that belong only to later milestones.
- When a decision is not required yet, leave it unresolved for the milestone where it becomes necessary rather than inventing it early.
- Repository defaults may guide implementation mechanics only after requirements and approved architecture permit the choice; they must never create business behavior, validation rules, compliance obligations, SLOs, or external dependencies.

See [Questioning Policy](../standards/questioning-policy.md).

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

## Capability Boundaries

Keep vendor SDKs out of business logic when a meaningful capability boundary is needed. The contracts below are reference examples, not interfaces that every service must implement:

- [MessagePublisher](../contracts/MessagePublisher.md) and [MessageSubscriber](../contracts/MessageSubscriber.md)
- [CacheProvider](../contracts/CacheProvider.md)
- [ObjectStorageProvider](../contracts/ObjectStorageProvider.md)
- [SecretProvider](../contracts/SecretProvider.md)
- [ConfigProvider](../contracts/ConfigProvider.md)

Introduce an abstraction only when it protects a real boundary, improves testability, isolates vendor coupling, or supports multiple implementations. Prefer an adopting project's existing abstraction/configuration model when it already satisfies that need. Do not create speculative interfaces for symmetry.

## Local Adapter Configuration

Local adapters help developers and CI exercise behavior without every external platform. They are not automatic production failover mechanisms.

The repository's reference implementation demonstrates adapter names such as `db`, `inmemory`, `jsonfile`, `local`, and `env`. Those names and environment-variable keys are **examples**, not required configuration contracts for every adopting project. Reuse an existing project configuration model when one exists.

Rules:

1. Adapter selection is explicit and validated through the project's typed/configuration mechanism.
2. Local-only adapter activation is observable; use logging and metrics where those signals are part of the project's operating model.
3. Reduced durability, ordering, consistency, concurrency, and security guarantees are documented.
4. Production startup or deployment validation rejects local-only adapters.
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
2. Production secrets use the approved secure delivery/access mechanism. When an adopting project uses this repository's `SecretProvider` boundary, access secrets through that boundary. Environment-backed secret resolution in the local-adapter reference is local/test guidance and must not silently become a production fallback.
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
| Copilot customizations | [Copilot Customization Model](../docs/copilot-customizations.md) |

## Stack Guidance

- [Java 21 and Spring Boot 3.x](../stacks/java-springboot/java-spring.md)
- [Python 3.12+ and FastAPI](../stacks/python-fastapi/python-backend.md)

## Available Prompt Workflows

- `/review-requirements` — analyze requirement completeness and ask only blocking clarification questions; no planning or implementation
- `/create-plan` — create or update `docs/.ai/Plan.md` only after the requirements gate passes; no implementation
- `/create-implementation-plan` — create one phase-specific milestone Implementation Plan; no source/test changes
- `/generate-tests` — execute one approved RED milestone only, verify valid RED, and stop
- `/implement-approved-plan` — execute one approved GREEN or non-behavior milestone only; never RED or REFACTOR
- `/refactor-code` — execute one approved REFACTOR milestone only from a verified GREEN baseline
- `/scaffold-service` — orchestrate service creation while preserving Plan and per-milestone human review gates
- `/review-code`, `/review-architecture`, `/review-distributed-systems`, `/review-production-readiness` — evidence-based reviews
- `/compliance-review`, `/review-hipaa` — engineering control reviews, not legal certification

Repository Agent Skills under `.github/skills/` provide deeper task-specific behavior. The requirements-analysis skill is a planning gate; the code-review skill reinforces evidence-based review without replacing the canonical standards or prompts.
