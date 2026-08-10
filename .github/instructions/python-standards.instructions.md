---
applyTo: "**/*.py"
description: "Apply Python/FastAPI guidance with PDD phase gates, typed configuration, controlled dependencies, and requirement-driven security/observability."
---

Follow the applicable guidance in [Python backend standards](../../stacks/python-fastapi/python-backend.md), [coding standards](../../standards/coding-standards.md), and the [prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md).

## Delivery Sequence

For non-trivial behavior changes:

1. work from an approved Plan containing separate RED and GREEN milestones; add a separate REFACTOR milestone only when justified;
2. create and obtain approval for the current phase-specific Implementation Plan;
3. RED changes approved tests/checks only, confirms valid RED, records evidence, and stops;
4. GREEN requires predecessor RED evidence, implements the smallest approved Python/FastAPI behavior, runs focused/regression checks, records evidence, and stops;
5. Refactor only through a separately approved REFACTOR milestone from a verified GREEN baseline.

Do not introduce requirements/files outside the approved current milestone and do not auto-advance between phases.

## Minimal Starter Rule

A new Python service must not inherit capabilities merely because the standards repository contains examples.

Add persistence, messaging, caching, object storage, security SDKs, observability SDKs, Testcontainers/emulators, or local adapters only when explicit/repository-confirmed requirements and the approved current milestone require them.

## Architecture

- `main.py`: app composition/lifecycle.
- `config/`: typed validated settings.
- Add `api/`, `application/service/`, `domain/`, `repository/`, and `infrastructure/` only when the service actually needs those responsibilities/boundaries.
- Keep business decisions out of FastAPI route handlers and vendor adapters.
- Do not create interfaces solely to wrap one call without a real boundary.

## Python Practices

- Use Pydantic v2 for transport/configuration models; do not make every domain type Pydantic by default.
- Use async only for asynchronous composition/I/O; never block the event loop with blocking clients.
- Inject selected production dependencies at boundaries rather than constructing vendor clients inside handlers/domain code.
- Raise specific domain/application exceptions and map them centrally when an HTTP API exists.
- Use the project's configured formatter/linter/type checker.

## Configuration

- Validate risk-bearing configuration before use/startup.
- Centralize configuration enough to avoid scattered raw environment reads.
- Define precedence only for sources the service actually uses.
- Do not require `ConfigProvider` or dynamic config without a justified boundary.
- Never hardcode/log secrets.

## Security

- Validate untrusted input at trust boundaries.
- Authenticate/authorize only according to approved resource/access requirements.
- Use least privilege and prevent sensitive-data leakage.
- Do not infer JWT/OAuth/mTLS/RBAC/ABAC/HIPAA mechanisms from generic enterprise or healthcare terminology.

## Observability

- Use appropriate production logging.
- Add correlation, metrics, traces, health checks, and alerts according to actual operating/failure/SLO needs.
- Never log secrets or sensitive payloads.
- Do not auto-install OpenTelemetry/Prometheus/tracing libraries.

## Local Adapters

When an approved milestone selects a local adapter, use the separate reference implementation as guidance and implement only the needed capability.

Local-only adapters must document reduced guarantees and be rejected in production. They are not production fallback/degradation behavior.

## Testing

- Tests for a RED milestone cover only approved behavior and fail for the expected reason.
- GREEN implementation is minimal and satisfies predecessor RED evidence.
- Integration tests use realistic dependencies/emulators/local adapters only where they materially improve confidence.
- Keep behavior changes separate from refactoring.
