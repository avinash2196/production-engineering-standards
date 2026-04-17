# Java Spring Boot Guidance

Purpose
- Provide concrete, production-oriented patterns for building Spring Boot services that comply with the repository's engineering principles: configuration-first, fallback-aware, observable, testable, and cloud-local friendly.

Structure
- Layers: `controller` -> `service` -> `domain` -> `repository`.
- Recommended folders:
  - `src/main/java/com/<org>/<service>/api` (controllers, DTOs)
  - `src/main/java/com/<org>/<service>/service` (application services)
  - `src/main/java/com/<org>/<service>/domain` (entities, value objects)
  - `src/main/java/com/<org>/<service>/repository` (data access)
  - `src/main/java/com/<org>/<service>/adapter` (infrastructure adapters: messaging, storage, cache)
  - `src/main/java/com/<org>/<service>/config` (configuration wiring and `ConfigProvider` adapters)
  - `src/test/java/...` (unit + integration tests)
- Naming: DTOs end with `Request`/`Response`. Interfaces use `...Provider` suffix (e.g., `MessagePublisher`), implementations use `...Impl` or `...KafkaAdapter`.

Abstractions
- Messaging: define `MessagePublisher` and `MessageSubscriber` interfaces in a shared `core` module. Publisher methods accept `topic`, `payload`, `attributes` and optional `idempotencyKey` and `traceId`.
- Storage: define `ObjectStorageProvider` with `put/get/delete/list/presign`. Implement cloud adapter and local file adapter.
- Config: `ConfigProvider` exposes typed config objects and supports refresh hooks; prefer Spring `@ConfigurationProperties` bound to a provider wrapper that consults dynamic config.
- Cache: `CacheProvider` exposing `get/put/invalidate` with TTL semantics; default to Redis in prod and in-memory LRU fallback in dev.

Fallback handling (local vs production)
- Explicit toggles: enable fallbacks only when env var like `FALLBACK_KAFKA=true`, `FALLBACK_CACHE=inmemory`, `FALLBACK_STORAGE=local`.
- Production images must default toggles off; local dev compose files enable toggles.
- Telemetry: when a fallback is active, emit a metric `fallback.active{name="kafka"}` and a structured warning log including the `X-Correlation-ID`.
- Behavior differences must be documented (durability, ordering, consistency) and tested in `examples/fallback-demo`.

Spring Boot patterns
- Use Spring Boot starter modules and keep one `@SpringBootApplication` per service.
- Configuration-first: use `@ConfigurationProperties` DTOs that are populated by a `ConfigProviderAdapter` which reads env → dynamic → file per precedence.
- Wiring: prefer constructor injection and create beans for adapters (`@Configuration` classes). Keep controllers thin and map DTOs to domain models in service layer.

ControllerAdvice and DTO separation
- Use `@RestController` for controllers and `@ControllerAdvice` for centralized exception handling and validation error mapping.
- Keep DTOs in `api.dto` package. Use MapStruct or explicit mappers in `service` layer for DTO ↔ domain transformations.

Testing (Testcontainers)
- Unit tests: mock capability abstractions (`MessagePublisher`, `ObjectStorageProvider`) using Mockito.
- Integration tests: use Testcontainers for DB and broker in CI where possible; otherwise use local fallbacks for deterministic CI runs.
- Provide contract tests for API and messaging flows (Pact or custom consumer-driven tests).

Anti-patterns
- Business logic in controllers.
- Direct use of SDK objects (e.g., KafkaProducer) in domain code or controllers.
- Implicit fallback activation in production images.

LLM instructions
- When scaffolding a Spring Boot service, generate:
  - `ConfigProvider` adapter and `@ConfigurationProperties` DTOs
  - interfaces for `MessagePublisher`, `ObjectStorageProvider`, `CacheProvider`, `SecretProvider`
  - both cloud adapter stubs and local fallback implementations with explicit env toggles
  - centralized `@ControllerAdvice` for error mapping and correlation-ID injection at the filter level
- Ask the user only when: data sensitivity is ambiguous, ordering guarantees are required for events, or multi-region deployment is requested.

Review checklist
- [ ] Layer separation enforced (controller/service/domain/repository).
- [ ] DTOs present and mapped to domain objects.
- [ ] Capability abstractions present and used.
- [ ] Fallback toggles explicit and documented.
- [ ] Observability hooks (logging/metrics/tracing) present and tested.
