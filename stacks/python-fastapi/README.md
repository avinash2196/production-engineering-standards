# Python FastAPI Stack

Guidance, an executable base template, and integration notes for Python 3.12+ FastAPI services.

## Delivery Workflow

Do not copy the template and immediately generate production behavior. Follow:

> Plan -> Implementation Plan -> RED Test -> GREEN Code -> Refactor

The approved implementation plan selects the required endpoints, persistence, production adapters, local adapters, and verification commands. The base template intentionally does not include every production integration.

## Base Template

`project-template/` includes:

- typed Pydantic settings and adapter enums;
- production startup rejection for local-only adapters;
- database-backed and in-memory messaging local adapters;
- JSON-file and in-memory cache local adapters;
- local filesystem storage and environment secret adapters;
- behavior-focused tests for selection, persistence, TTL, and production guards.

Production Kafka, Pub/Sub, Redis, S3, GCS, Vault, or Secret Manager adapters are added only when selected by an approved implementation plan. Requesting a missing adapter produces an actionable error rather than silently choosing a local substitute.

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

After installing the minimal dependencies declared in `pyproject.toml`:

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
