# Enterprise AI Engineering — Workspace Instructions

This repository is the **single source of truth** for engineering standards.
Apply all rules here when generating, reviewing, or scaffolding code for this project.

## Default Architecture

Use the following layered structure as the default for backend services. A project may use a simpler structure when its documented architecture decision explains why additional layers would add no value.

Dependencies should point toward domain and application abstractions. Infrastructure implementations must not become dependencies of domain logic.

| Area | Responsibility | Must Avoid |
|---|---|---|
| **API/Controller** | Transport handling, DTO binding, validation, response mapping | Business rules and direct data access |
| **Application Service** | Use-case orchestration, transactions, authorization coordination | Direct vendor SDK usage |
| **Domain** | Business rules, entities, value objects, domain events | Transport and infrastructure concerns |
| **Ports/Contracts** | Repository and external-capability abstractions | Vendor-specific implementation details |
| **Infrastructure Adapters** | Database, messaging, cache, storage, and secret-provider implementations | Business policy |

Full rules: [standards/architecture.md](../standards/architecture.md)

## Capability Interfaces — Always Use

Inject **interfaces**, never concrete infrastructure classes, into the service layer:

- `MessagePublisher` / `MessageSubscriber` → [spec](../contracts/MessagePublisher.md)
- `CacheProvider` → [spec](../contracts/CacheProvider.md)
- `ObjectStorageProvider` → [spec](../contracts/ObjectStorageProvider.md)
- `SecretProvider` → [spec](../contracts/SecretProvider.md)
- `ConfigProvider` → [spec](../contracts/ConfigProvider.md)


## Local Adapter Configuration

Services that depend on external infrastructure should provide local adapters when the adapter adds meaningful development or testing value.

Local adapters are not production failover mechanisms. Production degradation behavior must be designed separately based on correctness, durability, security, and business impact.

| Variable | Production/default value | Local adapter values |
|---|---|---|
| `MESSAGING_ADAPTER` | `kafka` | `db`, `inmemory` |
| `CACHE_ADAPTER` | `redis` | `jsonfile`, `inmemory` |
| `STORAGE_ADAPTER` | `s3` | `local` |
| `SECRET_ADAPTER` | `vault` | `env` |

Details: [standards/fallback-strategy.md](../standards/fallback-strategy.md)

## Non-Negotiable Rules

1. Domain objects have **zero** framework dependencies.
2. Secrets are always retrieved via `SecretProvider` — never hardcoded or via plain env vars.
3. Every service must expose sufficient logs and health information for its operating environment. 
4. Metrics and distributed tracing should be added according to runtime, support model, and service criticality.
5. Collection-fetching paths must be reviewed for N+1 query behavior. 
6. Use joins, entity graphs, batching, or purpose-built queries based on pagination and cardinality requirements.
7. All remote calls must define timeouts. Their failure behavior must be documented as retry, circuit-break, degrade, queue, return stale data, fail closed, or fail fast.

Full principles: [standards/engineering-principles.md](../standards/engineering-principles.md)

## Standards — Key References

| Concern | Document                                                                             |
|---------|--------------------------------------------------------------------------------------|
| Naming, method/class size | [standards/coding-standards.md](../standards/coding-standards.md)                    |
| Request/response DTOs | [standards/dto-guidelines.md](../standards/dto-guidelines.md)                           |
| Security, TLS, secrets | [standards/security/security-standards.md](../standards/security/security-standards.md) |
| Metrics, logs, traces | [standards/observability.md](../standards/observability.md)                             |
| Unit + integration tests | [standards/testing/unit-testing.md](../standards/testing/unit-testing.md)               |
| Performance limits | [standards/performance/performance.md](../standards/performance/performance.md)         |
| HIPAA controls | [standards/compliance/hipaa-controls.md](../standards/compliance/hipaa-controls.md)     |
| Agent planning + doc creation | [standards/agent-execution.md](../standards/agent-execution.md)                         |

## Stack Quick Reference

- **Java 21 + Spring Boot 3.x** → [stacks/java-springboot/java-spring.md](../stacks/java-springboot/java-spring.md)
- **Python 3.12+ + FastAPI** → [stacks/python-fastapi/python-backend.md](../stacks/python-fastapi/python-backend.md)

## Agent Execution — Always Follow

Before starting any task that touches ≥ 4 files, creates/deletes directories, or changes a shared standard:

1. Write a plan file at `.copilot/plans/YYYY-MM-DD-<task-slug>.md`
2. Present the plan to the user before editing anything
3. Check off each step as it completes — never batch checkoffs at end
4. When creating any `.md` file, ask the five Doc Creation Protocol questions first

Full rules: [standards/agent-execution.md](../standards/agent-execution.md)  
Doc creation workflow: [playbooks/create-doc.md](../playbooks/create-doc.md)

## Available Slash Commands

Type `/` in Copilot Chat to access:
- `/scaffold-service` — generate a complete new microservice
- `/compliance-review` — audit a service against org standards
- `/create-doc` — create any `.md` doc with guided questions + templates
- `/generate-adr` — record an architecture decision
- `/review-architecture` — assess layering, coupling, and capability interface usage
- `/review-code` — detailed code review against org standards
- `/review-api-design` — validate OpenAPI specs and detect breaking changes
- `/generate-tests` — generate unit + integration tests
- `/generate-load-tests` — generate k6 load test scripts
- `/analyse-codebase` — map dependencies, hotspots, and technical debt
- `/refactor-code` — safely restructure code with tests green
- `/review-distributed-systems` — assess reliability, idempotency, fallback wiring
- `/review-hipaa` — audit HIPAA control compliance
- `/review-production-readiness` — full pre-deploy checklist
- `/maintenance-check` — dependency audit, deprecation scan, dead code
