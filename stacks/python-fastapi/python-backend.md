# Python and FastAPI Engineering Guidance

## Purpose

Provide practical Python 3.12+/FastAPI guidance for plan-driven delivery, test-first behavior changes, typed configuration, controlled dependencies, and production-safe operations.

The canonical starter is deliberately minimal. Persistence, messaging, cache, object storage, security mechanisms, telemetry SDKs, and local adapters are capabilities selected by requirements and an approved phase-specific Implementation Plan—not defaults inherited by every service.

## Required Workflow

For non-trivial behavior-changing work:

1. review requirements and current repository state; if a material decision is missing or contradictory, ask the user and stop rather than inventing it;
2. approve `docs/.ai/Plan.md`, with separate RED and GREEN milestones and an optional separate REFACTOR milestone when justified;
3. for the current milestone only, approve a phase-specific Implementation Plan with exact files, allowed changes, verification commands, and exclusions;
4. execute only that phase:
   - RED: tests/test support only, confirm expected RED, record evidence, stop;
   - GREEN: require approved predecessor RED evidence, implement the smallest production change for GREEN, record evidence, stop;
   - REFACTOR: require approved predecessor GREEN evidence, change structure only, preserve behavior, remain GREEN, stop;
5. do not advance until the next phase has its own approved Implementation Plan.

## Architecture

Use the simplest structure that protects actual decisions.

Start with:

- `main.py` for application composition/lifecycle;
- `config/` for typed settings.

Add only when justified:

- `api/` for routing, request/response validation, auth context, mapping;
- `service/` or `application/` for use-case orchestration/transactions;
- `domain/` for meaningful business rules/value objects;
- `repository/` when persistence exists and a boundary is useful;
- `infrastructure/` for selected vendor/local adapters.

A small CRUD service may combine areas when dependencies remain controlled. Do not create protocols/packages solely to satisfy a diagram.

## Python/FastAPI Practices

- Use Pydantic v2 for transport/settings models; prefer plain classes/dataclasses for domain behavior when framework independence helps.
- Use `async def` when awaiting asynchronous I/O. Keep CPU-only helpers synchronous unless composition requires otherwise.
- Do not call blocking clients in the event loop; use async drivers, worker threads, or background/queue processing according to the approved design.
- Inject important dependencies at application boundaries; do not construct vendor clients inside handlers/domain code.
- Use specific application/domain exceptions with centralized HTTP mapping when an API exists.
- Add type annotations at public and important internal boundaries. Apply the project's configured type checker rather than claiming one universal strictness level.

## Capability Selection

Do not preload these capabilities into a new service:

- SQLAlchemy/database drivers;
- Kafka/PubSub/queues;
- Redis/cache;
- S3/GCS/object storage;
- OAuth/OIDC/JWT/security-provider SDKs;
- OpenTelemetry/Prometheus/exporters;
- Testcontainers/emulators;
- local adapter implementations.

When a Plan requires a capability, select the minimum concrete dependency and boundary in that milestone's Implementation Plan.

The separate local-adapter reference demonstrates database/in-memory messaging, file/in-memory cache, filesystem storage, and environment-backed local secrets. Use only the relevant pattern when a service needs it.

## Configuration

Use typed/validated configuration for settings that affect correctness, security, dependencies, or startup safety.

Do not require a `ConfigProvider` interface unless multiple providers, runtime refresh, portability, or a policy boundary justifies it.

When multiple sources exist, document deterministic precedence. Do not invent dynamic configuration or a secret-provider product.

## Security

Treat external/lower-trust input as untrusted. Protect resources according to explicit authentication/authorization requirements and approved data classification.

Do not select JWT, OAuth/OIDC, mTLS, RBAC/ABAC, HIPAA controls, or a security vendor merely because the service is described as enterprise/healthcare.

Never embed/log secrets or sensitive payloads.

## Observability

Logging/telemetry must provide enough evidence to operate the service safely.

- use searchable/structured logging appropriate to the target platform;
- add safe correlation when operations cross boundaries and it improves diagnosis;
- add metrics tied to actual workload/failure/SLO needs;
- add distributed tracing when cross-service diagnosis justifies it;
- add health/readiness behavior when the target runtime relies on it.

Do not automatically install OpenTelemetry, Prometheus, or tracing exporters in the starter.

## Resilience

Define timeouts and explicit failure behavior for important remote dependencies. Choose bounded retry, circuit breaking, durable queueing, stale data, bypass, fail closed, or fail fast based on correctness/business impact. Do not automatically generate a fallback for every dependency.

## Testing

- Use `pytest`/`pytest-asyncio` or `unittest` according to project needs.
- Unit-test application/domain decisions without network access.
- Use Testcontainers/emulators only when selected real boundaries need realistic integration verification.
- Use local adapters only when their reduced guarantees are appropriate to the test/development objective.
- Test transaction rollback, idempotency, TTL, path safety, selection, and production guards only when those behaviors exist.
- Preserve RED/GREEN evidence and keep refactoring behavior-neutral.

## References

- [Prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md)
- [Architecture](../../standards/architecture.md)
- [Configuration management](../../standards/configuration-management.md)
- [Observability](../../standards/observability.md)
- [Security](../../standards/security/security-standards.md)
- [Local adapter strategy](../../standards/local-adapter-strategy.md)
- [Production dependency failure strategy](../../standards/fallback-strategy.md)
- [Python stack README](README.md)
