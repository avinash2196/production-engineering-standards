# Local Adapter Strategy

## Purpose

Allow developers and CI jobs to exercise service behavior without requiring every external platform to be available.

Local adapters are explicit development and testing implementations. They are not automatic production failover mechanisms.

## Principles

1. A local adapter must implement the same capability contract as the production adapter.
2. Activation must be explicit through typed configuration.
3. Activation must emit a structured warning and a `fallback.active` or `adapter.active` metric.
4. Differences in durability, ordering, consistency, concurrency, and security must be documented.
5. Local adapters must not activate silently in production.
6. A service does not need a local adapter for every dependency when Testcontainers, emulators, or mocks provide a better test boundary.

## Supported Adapters

| Capability | Production adapter | Preferred local adapter | Reduced guarantees |
|---|---|---|---|
| Messaging | Kafka/Pub/Sub | Database outbox | Different consumer and ordering behavior |
| Messaging | Kafka/Pub/Sub | In-memory queue | No restart durability or multi-instance coordination |
| Cache | Redis | JSON-file cache | No distributed consistency or atomic operations |
| Cache | Redis | In-memory cache | Process-local and lost on restart |
| Storage | S3/GCS | Local filesystem | No managed durability, encryption, or lifecycle |
| Secrets | Vault/Secret Manager | Environment variables | No rotation, centralized audit, or managed access policy |

## Production Guard

Production startup must fail when a local-only adapter is selected.