# Python and FastAPI Engineering Guidance

## Purpose

Provide practical Python 3.12+/FastAPI defaults for plan-driven delivery, test-first behavior changes, typed configuration, controlled external dependencies, and explicit local-adapter safety.

## Required Workflow

For non-trivial work:

1. review requirements and current repository state;
2. approve `docs/.ai/Plan.md`;
3. approve a milestone-specific Implementation Plan with exact files/tests;
4. add the focused test and confirm RED;
5. implement the smallest change for GREEN;
6. refactor while tests remain green;
7. run the full applicable Definition of Done.

## Architecture

Use the simplest structure that protects decisions:

- `api/` handles routing, request/response validation, auth context, and mapping;
- `service/` or `application/` coordinates use cases and transaction boundaries;
- `domain/` owns business rules/value objects when meaningful invariants exist;
- repository/capability protocols protect boundaries when they add testing, portability, or policy value;
- `infrastructure/` contains SQLAlchemy and vendor/local adapter details;
- `config/` owns typed settings, composition, and production guards.

A small CRUD service may combine areas when dependencies remain controlled. Do not create protocols and packages solely to satisfy a diagram.

## Python/FastAPI Practices

- Use Pydantic v2 for transport and settings models; prefer plain classes/dataclasses for domain behavior when framework independence helps.
- Use `async def` when awaiting asynchronous I/O. Keep CPU-only helpers synchronous unless composition requires otherwise.
- Do not call blocking clients in the event loop; use async drivers, worker threads, or background/queue processing according to the plan.
- Inject dependencies at API/application boundaries; do not construct vendor clients inside handlers.
- Use specific application/domain exceptions with centralized FastAPI exception mapping.
- Add type annotations at public and important internal boundaries. Apply the project's configured type checker rather than claiming one universal strictness level.
- Treat function/class size and nesting as review signals; refactor based on mixed responsibilities or hard-to-test behavior.

## Adapter Selection

Typed values include:

- messaging: `kafka`, `pubsub`, `db`, `inmemory`
- cache: `redis`, `jsonfile`, `inmemory`
- storage: `s3`, `gcs`, `local`
- secrets: `vault`, `secretmanager`, `env`

Local-only adapters must be explicit, emit an activation warning/metric where runtime telemetry is wired, document reduced guarantees, and be rejected in production.

Prefer a database-backed message adapter over an in-memory queue when restart durability and SQL inspection matter. Prefer a JSON-file cache over an in-memory cache when inspectability/restart persistence matter. Neither reproduces production broker or Redis semantics.

## Resilience

Define timeouts and named failure behavior for remote dependencies. Choose bounded retry, circuit breaking, durable queueing, stale data, bypass, fail closed, or fail fast based on correctness and business impact. Do not automatically generate a fallback for every dependency.

## Observability

Use structured logging, stable correlation/business identifiers, and health signals appropriate to support needs. Add metrics and tracing at important service/external boundaries. Never log secrets or sensitive payloads.

## Testing

- Use `pytest`/`pytest-asyncio` or standard-library `unittest` according to project needs.
- Unit-test application/domain decisions without network access.
- Use Testcontainers/emulators for selected production boundaries.
- Use temporary directories/files/databases for local adapter tests.
- Test transaction rollback, idempotency, TTL, path safety, selection, and production guards when applicable.
- Preserve RED/GREEN evidence and keep refactoring behavior-neutral.

## References

- [Prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md)
- [Architecture](../../standards/architecture.md)
- [Local adapter strategy](../../standards/local-adapter-strategy.md)
- [Production dependency failure strategy](../../standards/fallback-strategy.md)
- [Python stack README](README.md)
