---
applyTo: "**/*.py"
description: "Apply Python and FastAPI engineering guidance with typed configuration, explicit boundaries, test-first changes, and safe local-adapter selection."
---

Follow the applicable guidance in [Python backend standards](../../stacks/python-fastapi/python-backend.md), [coding standards](../../standards/coding-standards.md), and the [prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md).

## Delivery Sequence

For non-trivial behavior changes:

1. work from an approved plan and implementation plan;
2. add or update a behavior-focused test and confirm the expected failure;
3. implement the smallest change that makes it pass;
4. run the focused and relevant regression suites;
5. refactor only while tests remain green.

Do not introduce requirements or files outside the approved implementation plan.

## Architecture Defaults

- **API (`api/`)**: FastAPI routing, request parsing, validation, authentication context, and response mapping. Keep business decisions out of route handlers.
- **Application (`service/` or `application/`)**: use-case orchestration and transaction boundaries.
- **Domain (`domain/`)**: business rules and value objects when the service has meaningful invariants. Prefer framework-independent dataclasses or plain classes for domain behavior.
- **Ports/contracts**: protocols or abstract interfaces when they protect a real external or persistence boundary.
- **Infrastructure (`infrastructure/`)**: SQLAlchemy repositories and vendor-specific messaging, cache, storage, and secret adapters.

A small CRUD service may use a simpler structure when dependencies remain controlled and the decision is documented.

## Python Practices

- Use type annotations on public functions and important internal boundaries.
- Prefer Pydantic v2 models for transport and configuration models; do not make every domain object a Pydantic model by default.
- Use `async def` for handlers and operations that await asynchronous I/O. Keep CPU-only helpers synchronous unless asynchronous composition requires otherwise.
- Use dependency injection at application boundaries; do not instantiate production vendor clients inside handlers or domain code.
- Raise specific domain/application exceptions and map them through centralized exception handlers.
- Avoid broad `except Exception` unless re-raising after adding useful context or handling a process boundary safely.
- Treat function length, class size, and parameter count as review signals. Split code when mixed responsibilities, excessive nesting, or difficult testing demonstrates a concrete problem.
- Run the configured formatter, linter, and type checker for the project. Do not claim `mypy --strict` is mandatory unless the project configuration adopts it.

## Adapter Selection

Select implementations through typed settings and provider functions in `infrastructure/local/providers.py` or the project's equivalent composition root.

Examples:

- messaging: `kafka`, `pubsub`, `db`, or `inmemory`
- cache: `redis`, `jsonfile`, or `inmemory`
- storage: `s3`, `gcs`, or `local`
- secrets: `vault`, `secretmanager`, or `env`

Local-only values must emit a warning/metric, document reduced guarantees, and be rejected when `environment=production`.

## Security and Observability

- Read credentials through typed settings or an approved `SecretProvider`; never embed secrets in source.
- Use the project's structured logger rather than `print()` for service behavior.
- Bind stable correlation and business identifiers when useful, without logging secrets, PII, or PHI.
- Add metrics and spans to important service/external boundaries based on operating needs rather than instrumenting every helper.
- Define timeouts and explicit failure behavior for remote calls.

## Testing

- Use the project's selected framework, commonly `pytest`/`pytest-asyncio` or `unittest` for dependency-free template checks.
- Unit tests isolate business decisions through ports or fakes; they do not require a live network.
- Integration tests use realistic dependencies such as Testcontainers, emulators, or a documented local adapter when the boundary matters.
- Assert externally meaningful behavior, production guards, durability expectations, and error contracts.
- Keep test refactoring separate from behavior changes unless the approved implementation plan requires both.
