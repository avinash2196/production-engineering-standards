# Python FastAPI Stack

Guidance, an executable reference template, and integration notes for Python 3.12+ FastAPI services.

## Delivery Workflow

Do not copy the template and immediately generate production behavior. The approved Plan defines the required phase milestones, and each repository-changing milestone receives its own reviewed Implementation Plan.

For behavior-changing work:

> Plan -> RED milestone + RED Implementation Plan -> Human Review -> valid RED -> GREEN milestone + GREEN Implementation Plan -> Human Review -> GREEN -> optional REFACTOR milestone + REFACTOR Implementation Plan -> Human Review -> remain GREEN

A RED Implementation Plan authorizes tests/test support only. A GREEN Implementation Plan is created only after approved RED evidence and authorizes only the minimum production changes required for GREEN. Refactoring is separately planned only when justified and must preserve behavior. Do not combine these phases into one Implementation Plan or auto-advance between them.

The current phase-specific Implementation Plan selects only the endpoints, persistence, production adapters, local adapters, files, and verification commands required for that milestone. The template demonstrates the shared local-adapter strategy; it is not a mandate to carry every demonstrated capability into every real service.

## Base Template

`project-template/` includes:

- typed Pydantic settings and adapter enums;
- production startup rejection for local-only adapters;
- database-backed and in-memory messaging local adapters;
- JSON-file and in-memory cache local adapters;
- local filesystem storage and environment secret adapters;
- behavior-focused tests for selection, persistence, TTL, and production guards.

Production Kafka, Pub/Sub, Redis, S3, GCS, Vault, or Secret Manager adapters and their SDK dependencies are added only when selected by the approved current phase-specific Implementation Plan. Requesting a missing adapter produces an actionable error rather than silently choosing a local substitute.

Metrics, distributed tracing, authentication, and other optional production mechanisms are also added only when selected by the approved service design. Structured startup/shutdown logging remains part of the reference template.

## Suggested Structure

```text
app/
  api/                 transport, validation, response mapping
  service/             application/use-case orchestration
  domain/              business rules and value objects where justified
  repository/          persistence boundaries and implementations
  infrastructure/
    local/              explicit local-only adapters and composition
    messaging/          selected production messaging adapter
    cache/              selected production cache adapter
    storage/            selected production storage adapter
    secrets/            selected production secret adapter
  config/              typed settings and startup guards
  main.py
```

A simple CRUD service may combine areas when dependencies remain controlled and the decision is documented.

## Run Template Tests

After installing the dependencies declared in `pyproject.toml`:

```bash
PYTHONPATH=project-template \
  python -m unittest discover \
  -s project-template/tests \
  -p 'test_*.py'
```

## Local Adapter Selection

```bash
ENVIRONMENT=local \
MESSAGING_ADAPTER=db \
CACHE_ADAPTER=jsonfile \
STORAGE_ADAPTER=local \
SECRET_ADAPTER=env \
uvicorn app.main:app --reload --port 8000
```

The database messaging adapter is preferred when restart durability and SQL inspection are useful. It does not reproduce broker partitions, consumer groups, rebalancing, replay, or production throughput. JSON-file cache similarly does not reproduce Redis atomicity or distributed coordination.

## Guides

| Guide | Focus |
|---|---|
| [Messaging Integration](integration-guides/kafka-integration.md) | Kafka/Pub/Sub contracts, database outbox, idempotency, consumer behavior |
| [Cache Integration](integration-guides/redis-integration.md) | Redis policy, JSON-file/in-memory local adapters, TTL and correctness |
| [Storage Integration](integration-guides/storage-integration.md) | S3/GCS, local filesystem, path safety and durability semantics |

## References

- [Python backend guidance](python-backend.md)
- [Prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md)
- [Capability boundary pattern](../../contracts/CapabilityPattern.md)
- [Local adapter strategy](../../standards/local-adapter-strategy.md)
- [Production dependency failure strategy](../../standards/fallback-strategy.md)
