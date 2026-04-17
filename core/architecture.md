# Architecture

Layered architecture standard for all enterprise backend services.

## Purpose

Define a consistent, testable, and maintainable service architecture that separates concerns into well-defined layers with strict dependency rules.

## Layer Model

```
┌─────────────────────────────────────┐
│          Controller / API           │  ← HTTP, gRPC, event handlers
├─────────────────────────────────────┤
│            Service Layer            │  ← Business orchestration
├─────────────────────────────────────┤
│           Domain Layer              │  ← Entities, value objects, rules
├─────────────────────────────────────┤
│         Repository Layer            │  ← Data access (DB, external APIs)
├─────────────────────────────────────┤
│     Infrastructure / Adapters       │  ← Capability interface impls
└─────────────────────────────────────┘
```

## Layer Responsibilities

### Controller (API)
- Accept and validate inbound requests.
- Map DTOs to domain objects.
- Delegate to the service layer — **no business logic here**.
- Return structured responses with appropriate HTTP status codes.

### Service
- Orchestrate business workflows across domain objects and infrastructure.
- Enforce authorization and business rules.
- Publish domain events via `MessagePublisher`.
- Manage transactions (when applicable).

### Domain
- Pure business logic, entities, value objects, and domain events.
- No framework dependencies — testable in isolation.
- Rich domain model preferred over anemic DTOs.

### Repository
- Data access layer — encapsulates persistence details.
- Returns domain objects, not raw database rows.
- One repository per aggregate root.

### Infrastructure / Adapters
- Implementations of capability interfaces (`MessagePublisher`, `CacheProvider`, `ObjectStorageProvider`, `SecretProvider`, `ConfigProvider`).
- Production beans and fallback beans live here.
- Activated via environment variables and DI profiles.

## Dependency Rules

```
Controller  →  Service  →  Domain  ←  Repository
                 ↓
          Infrastructure
```

| Rule | Description |
|------|-------------|
| **Direction** | Dependencies flow inward — outer layers depend on inner layers, never the reverse. |
| **Domain independence** | Domain layer has zero dependencies on framework, infrastructure, or external libraries. |
| **Interface boundaries** | Service layer depends on capability *interfaces*, never concrete implementations. |
| **No layer skipping** | Controllers must not call repositories directly; they go through the service layer. |

## Cross-Cutting Concerns

| Concern | Where it lives |
|---------|----------------|
| Authentication | Middleware / filter (before controller) |
| Authorization | Service layer (`@PreAuthorize` or manual check) |
| Logging | All layers via structured logger |
| Metrics | Controller (request metrics) + service (business metrics) |
| Tracing | Spans created at controller edge, propagated through all layers |
| Error handling | Global exception handler maps domain exceptions to HTTP responses |

## Java Spring Boot Layout

```
src/main/java/com/myorg/{service}/
├── controller/      # @RestController classes
├── service/         # @Service classes
├── domain/          # POJOs, records, enums
├── repository/      # @Repository interfaces (Spring Data JPA)
├── infrastructure/  # Capability implementations
└── config/          # @Configuration, @Bean definitions
```

## Python FastAPI Layout

```
src/{service_name}/
├── api/             # FastAPI routers
├── service/         # Business logic classes
├── domain/          # Pydantic models, dataclasses
├── repository/      # SQLAlchemy / asyncpg data access
├── infrastructure/  # Capability implementations
└── config/          # Settings (pydantic-settings)
```

## Anti-Patterns

| Anti-Pattern | Why it's wrong |
|-------------|----------------|
| Business logic in controllers | Untestable, duplicated across endpoints |
| Controller calling repository directly | Skips authorization, validation, and event publishing |
| Domain objects with framework annotations | Couples domain to infrastructure |
| God service with 500+ lines | Split into focused services per aggregate |
| Circular dependencies between layers | Indicates incorrect boundaries — use events to decouple |

## LLM Instructions

- When generating a new endpoint, create a controller that delegates to a service, which operates on domain objects and calls repositories.
- Never place SQL queries, HTTP calls, or caching logic in the service layer — use repository or capability interfaces.
- If a service method exceeds ~50 lines, suggest splitting into smaller domain operations.

## References

- [principles.md](principles.md)
- [Core abstractions](abstractions/)
- [Fallback strategy](../standards/fallback-strategy.md)
