# Java and Spring Boot Engineering Guidance

## Purpose

Provide practical Java 21/Spring Boot 3.x defaults for services that use plan-driven implementation, test-first behavior changes, controlled dependencies, and explicit operational decisions.

## Required Workflow

For non-trivial work:

1. review requirements and current code;
2. approve `docs/.ai/Plan.md`;
3. approve a milestone-specific Implementation Plan with exact files and tests;
4. add the focused test and confirm RED;
5. implement the smallest change for GREEN;
6. refactor while tests remain green;
7. run the full applicable Definition of Done.

## Architecture

Use the simplest structure that preserves clear decisions:

- controllers handle transport, validation, authentication context, and response mapping;
- application services coordinate use cases and transactions;
- domain objects own meaningful invariants when complexity justifies them;
- ports isolate persistence or external capabilities when they protect a real boundary;
- infrastructure adapters contain JPA, Kafka/Pub/Sub, Redis, storage, and secret SDK details;
- configuration classes compose implementations through typed properties.

Do not create packages or interfaces solely to satisfy a fixed layer count.

## Spring Practices

- Prefer constructor injection; avoid field injection.
- Use `@ConfigurationProperties` with validation for grouped configuration.
- Use records for immutable DTOs when compatible with the API/framework needs.
- Apply Bean Validation to request shape; keep business rules in application/domain code.
- Define transaction boundaries around coherent database work and avoid slow remote calls inside a transaction unless explicitly designed.
- Map specific application/domain exceptions with centralized exception handling.
- Treat method/class/constructor size as review signals; refactor based on mixed responsibilities or testability, not a number alone.
- Configure graceful shutdown and relevant liveness/readiness checks.

## Capability and Adapter Selection

```yaml
adapters:
  messaging: ${MESSAGING_ADAPTER:kafka}
  cache: ${CACHE_ADAPTER:redis}
  storage: ${STORAGE_ADAPTER:s3}
  secrets: ${SECRET_ADAPTER:vault}
```

Local-only values are `db`/`inmemory`, `jsonfile`/`inmemory`, `local`, and `env`. They must:

- be selected explicitly;
- emit activation telemetry;
- document lost durability, ordering, consistency, concurrency, and security guarantees;
- be rejected in production by startup validation.

A database-backed message adapter and JSON-file cache are preferred when local restart persistence and inspectability matter. They are not production broker/cache replacements.

## Resilience

Every remote dependency has a timeout and named failure behavior. Depending on correctness and business impact, use bounded retry, circuit breaking, durable queueing, stale data, bypass, fail closed, or fail fast. Do not require a generic fallback for every dependency.

## Observability

Use SLF4J structured key-value logging or MDC where it aids diagnosis, Micrometer metrics on important service/external boundaries, and OpenTelemetry tracing according to support/SLO needs. Never log secrets or sensitive payloads.

## Testing

- JUnit 5 and Mockito/fakes for business/application tests without Spring context when possible.
- Focused MVC/WebFlux tests for API behavior.
- Testcontainers or supported emulators for persistence and infrastructure boundaries.
- Tests for transaction rollback, idempotency, retries, adapter selection, and production guards when applicable.
- Keep behavior changes separate from refactoring and preserve RED/GREEN evidence.

## References

- [Prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md)
- [Architecture](../../standards/architecture.md)
- [Local adapter strategy](../../standards/local-adapter-strategy.md)
- [Production dependency failure strategy](../../standards/fallback-strategy.md)
- [Java stack README](README.md)
