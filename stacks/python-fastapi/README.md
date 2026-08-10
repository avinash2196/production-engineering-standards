# Python FastAPI Stack

Guidance, a minimal executable starter, and reference implementations for Python 3.12+ FastAPI services.

## Delivery Workflow

Do not copy a template and immediately generate production behavior. The approved Plan defines separate RED and GREEN milestones and an optional separate REFACTOR milestone when justified. Each repository-changing milestone receives its own reviewed phase-specific Implementation Plan.

For behavior-changing work:

> Plan -> RED milestone + RED Implementation Plan -> Human Review -> valid RED -> GREEN milestone + GREEN Implementation Plan -> Human Review -> GREEN -> optional REFACTOR milestone + REFACTOR Implementation Plan -> Human Review -> remain GREEN

A RED Implementation Plan authorizes tests/test support only. A GREEN Implementation Plan is created only after approved RED evidence and authorizes only the minimum production changes required for GREEN. Refactoring is separately planned only when justified and must preserve behavior.

## Canonical Starter

`project-template/` is intentionally minimal and includes only:

- FastAPI application foundation;
- typed Pydantic settings;
- startup/shutdown logging foundation;
- minimal tests and developer tooling.

It does **not** preload persistence, messaging, cache, object storage, security-provider SDKs, OpenTelemetry, Prometheus, or local adapters.

Those capabilities are introduced only when explicit requirements, repository-confirmed architecture, and the approved current phase-specific Implementation Plan require them.

## Local-Adapter Reference Implementation

The previous capability-rich template is retained under:

`reference-implementations/local-adapters/`

It demonstrates patterns such as database/in-memory messaging, JSON/in-memory cache, filesystem storage, environment-backed local secrets, provider selection, and production rejection of local-only adapters.

Use it as a reference when a service actually needs one of those capabilities. Do not copy the entire reference implementation into every service.

Local adapters are development/test mechanisms. They are not production degradation behavior and do not reproduce managed-service guarantees.

## Suggested Structure

Start with the smallest structure that protects actual decisions:

```text
app/
  main.py
  config/
```

Add packages only when the approved milestone needs them, commonly:

```text
app/
  api/                 transport and validation
  service/             application/use-case orchestration
  domain/              business rules/value objects when justified
  repository/          persistence boundaries when persistence exists
  infrastructure/      selected production/local adapters
  config/              typed settings and composition
```

A simple service may use fewer layers when dependencies remain controlled.

## Run Minimal Starter Tests

```bash
PYTHONPATH=stacks/python-fastapi/project-template \
  python -m unittest discover \
  -s stacks/python-fastapi/project-template/tests \
  -p 'test_*.py'
```

## Reference Adapter Tests

After installing the reference implementation's own dependencies, run its tests from:

`stacks/python-fastapi/reference-implementations/local-adapters/`

Do not treat passing reference-adapter tests as production readiness evidence for Kafka, Redis, cloud object storage, or managed secret systems.

## Guides

| Guide | Focus |
|---|---|
| [Messaging Integration](integration-guides/kafka-integration.md) | Kafka/Pub/Sub contracts, outbox/idempotency/consumer behavior when messaging is selected |
| [Cache Integration](integration-guides/redis-integration.md) | Redis policy and local cache choices when caching is selected |
| [Storage Integration](integration-guides/storage-integration.md) | S3/GCS/local filesystem behavior when object storage is selected |

## References

- [Python backend guidance](python-backend.md)
- [Prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md)
- [Local adapter strategy](../../standards/local-adapter-strategy.md)
- [Production dependency failure strategy](../../standards/fallback-strategy.md)
