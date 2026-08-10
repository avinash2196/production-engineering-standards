# Java and Spring Boot Engineering Guidance

## Purpose

Provide practical Java 21/Spring Boot 3.x defaults for services that use plan-driven implementation, test-first behavior changes, controlled dependencies, and explicit operational decisions.

## Required Workflow

For non-trivial behavior-changing work:

1. review requirements and current code; if a material decision is missing or contradictory, ask the user and stop rather than inventing it;
2. approve `docs/.ai/Plan.md`, with separate RED and GREEN milestones and an optional separate REFACTOR milestone when justified;
3. for the current milestone only, approve a phase-specific Implementation Plan with exact files, allowed changes, verification commands, and exclusions;
4. execute only that phase:
   - RED: tests/test support only, confirm expected RED, record evidence, stop;
   - GREEN: require approved predecessor RED evidence, implement the smallest production change for GREEN, record evidence, stop;
   - REFACTOR: require approved predecessor GREEN evidence, change structure only, preserve behavior, remain GREEN, stop;
5. do not advance to the next phase until its own Implementation Plan is approved;
6. run the applicable Definition of Done for the completed milestone and the final capability review when the sequence is complete.

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
- Configure graceful shutdown and relevant liveness/readiness checks where the selected runtime and operating model require them.

## Capability and Adapter Selection

Define only the capability selectors the service actually uses. The following is an example for a messaging capability, not a required configuration bundle:

```yaml
adapters:
  messaging: ${MESSAGING_ADAPTER:kafka}
```

If the approved design also uses cache, storage, or managed secrets, add those selectors and dependencies explicitly in that milestone.

Local-only values may include `db`/`inmemory` for messaging, `jsonfile`/`inmemory` for cache, `local` for storage, and `env` for secrets. When used, they must:

- be selected explicitly;
- emit activation telemetry;
- document lost durability, ordering, consistency, concurrency, and security guarantees;
- be rejected in production by startup validation.

A database-backed message adapter and JSON-file cache are preferred when local restart persistence and inspectability matter. They are not production broker/cache replacements.

## Resilience

Every important remote dependency has a timeout and named failure behavior. Depending on correctness and business impact, use bounded retry, circuit breaking, durable queueing, stale data, bypass, fail closed, or fail fast. Do not require a generic fallback for every dependency.

## Observability

Use SLF4J structured key-value logging or MDC where it aids diagnosis, Micrometer metrics on important service/external boundaries, and OpenTelemetry tracing according to support/SLO needs. Never log secrets or sensitive payloads. Add libraries only for the mechanisms selected by the approved service design.

## Testing

- JUnit 5 and Mockito/fakes for business/application tests without Spring context when possible.
- Focused MVC/WebFlux tests for API behavior when that transport is used.
- Testcontainers or supported emulators for persistence and infrastructure boundaries when they provide meaningful integration evidence.
- Tests for transaction rollback, idempotency, retries, adapter selection, and production guards when applicable.
- Keep behavior changes separate from refactoring and preserve RED/GREEN evidence.

## References

- [Prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md)
- [Architecture](../../standards/architecture.md)
- [Local adapter strategy](../../standards/local-adapter-strategy.md)
- [Production dependency failure strategy](../../standards/fallback-strategy.md)
- [Java stack README](README.md)
