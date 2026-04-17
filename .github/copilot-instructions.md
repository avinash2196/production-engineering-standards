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

Full rules: [core/architecture.md](core/architecture.md)

## Capability Interfaces — Always Use

Inject **interfaces**, never concrete infrastructure classes, into the service layer:

- `MessagePublisher` / `MessageSubscriber` → [spec](core/abstractions/MessagePublisher.md)
- `CacheProvider` → [spec](core/abstractions/CacheProvider.md)
- `ObjectStorageProvider` → [spec](core/abstractions/ObjectStorageProvider.md)
- `SecretProvider` → [spec](core/abstractions/SecretProvider.md)
- `ConfigProvider` → [spec](core/abstractions/ConfigProvider.md)

## Fallback Toggles — Required

Every service must run with zero infrastructure via these env vars:

| Var | Default | Fallback |
|-----|---------|----------|
| `FALLBACK_KAFKA` | `false` | in-memory queue |
| `FALLBACK_CACHE` | `redis` | `inmemory` HashMap |
| `FALLBACK_STORAGE` | `s3` | `local` filesystem |
| `FALLBACK_SECRETS` | `vault` | `env` variables |

Details: [core/fallbacks/fallback-strategy.md](core/fallbacks/fallback-strategy.md)

## Non-Negotiable Rules

1. Domain objects have **zero** framework dependencies.
2. Secrets are always retrieved via `SecretProvider` — never hardcoded or via plain env vars.
3. Every service emits structured logs, Prometheus metrics, and OTEL traces from day one.
4. No N+1 queries — every collection fetch uses a join/batch.
5. All external calls have a timeout and a documented fallback.

Full principles: [core/principles.md](core/principles.md)

## Standards — Key References

| Concern | Document |
|---------|----------|
| Naming, method/class size | [standards/coding-standards.md](standards/coding-standards.md) |
| Request/response DTOs | [standards/dto-guidelines.md](standards/dto-guidelines.md) |
| Security, TLS, secrets | [standards/security/security-standards.md](standards/security/security-standards.md) |
| Metrics, logs, traces | [standards/observability.md](standards/observability.md) |
| Unit + integration tests | [standards/testing/unit-testing.md](standards/testing/unit-testing.md) |
| Performance limits | [standards/performance/performance.md](standards/performance/performance.md) |
| HIPAA controls | [standards/compliance/hipaa-controls.md](standards/compliance/hipaa-controls.md) |

## Stack Quick Reference

- **Java 21 + Spring Boot 3.x** → [stacks/java-springboot/java-spring.md](stacks/java-springboot/java-spring.md)
- **Python 3.12+ + FastAPI** → [stacks/python-fastapi/python-backend.md](stacks/python-fastapi/python-backend.md)

## Available Slash Commands

Type `/` in Copilot Chat to access:
- `/scaffold-service` — generate a complete new microservice
- `/compliance-review` — audit a service against org standards
