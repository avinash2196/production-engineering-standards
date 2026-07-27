# Enterprise AI Engineering — Workspace Instructions

This repository is the **single source of truth** for engineering standards.
Apply all rules here when generating, reviewing, or scaffolding code for this project.

## Architecture — Always Enforce

5-layer model. Dependencies flow **downward only**. Never skip layers.

| Layer | Responsibility | Forbidden |
|-------|---------------|-----------|
| **Controller** | HTTP routing, DTO binding, input validation | Business logic, domain imports |
| **Service** | Orchestrates domain + capability interfaces | Direct infrastructure imports (Kafka, Redis, S3) |
| **Domain** | Entities, value objects, domain events | Any framework annotation (Spring, FastAPI, SQLAlchemy) |
| **Repository** | Data access — one per aggregate root | Business logic |
| **Infrastructure** | Capability implementations + fallbacks | Domain logic |

Full rules: [standards/architecture.md](../standards/architecture.md)

## Capability Interfaces — Always Use

Inject **interfaces**, never concrete infrastructure classes, into the service layer:

- `MessagePublisher` / `MessageSubscriber` → [spec](../contracts/MessagePublisher.md)
- `CacheProvider` → [spec](../contracts/CacheProvider.md)
- `ObjectStorageProvider` → [spec](../contracts/ObjectStorageProvider.md)
- `SecretProvider` → [spec](../contracts/SecretProvider.md)
- `ConfigProvider` → [spec](../contracts/ConfigProvider.md)

## Fallback Toggles — Required

Every service must run with zero infrastructure via these env vars:

| Var | Default | Fallback |
|-----|---------|----------|
| `FALLBACK_KAFKA` | `db` | DB outbox table — persistent. `inmemory` = in-process queue (ephemeral) |
| `FALLBACK_CACHE` | `jsonfile` | JSON file cache — persistent. `inmemory` = in-process map (ephemeral) |
| `FALLBACK_STORAGE` | `s3` | `local` filesystem |
| `FALLBACK_SECRETS` | `vault` | `env` variables |

Details: [standards/fallback-strategy.md](../standards/fallback-strategy.md)

## Non-Negotiable Rules

1. Domain objects have **zero** framework dependencies.
2. Secrets are always retrieved via `SecretProvider` — never hardcoded or via plain env vars.
3. Every service emits structured logs, Prometheus metrics, and OTEL traces from day one.
4. No N+1 queries — every collection fetch uses a join/batch.
5. All external calls have a timeout and a documented fallback.

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
