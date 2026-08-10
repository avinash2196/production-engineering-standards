# Workflow: Add a Local Adapter or Production Degradation Path

## Purpose

Decide whether a dependency concern is a **local-development adapter** or a **production failure/degradation behavior**, then implement it through separate PDD RED/GREEN milestones. Do not combine the two concepts under a vague fallback toggle.

## 1. Classify the Need

### Local adapter

Use when developers or CI need an alternate implementation without the production platform.

Examples:

- Kafka/Pub/Sub → database-backed queue/outbox or in-memory queue
- Redis → JSON-file or in-memory cache
- S3/GCS → local filesystem
- Vault/Secret Manager → environment provider

Reference: [Local Adapter Strategy](../standards/local-adapter-strategy.md)

### Production degradation

Use when defining live behavior during dependency failure.

Examples:

- fail closed when a critical security dependency is unavailable when approved requirements require it
- durably queue an event when the approved design requires deferred delivery
- bypass a non-critical cache when the database can safely absorb load
- return stale data only under an approved freshness contract

Reference: [Production Dependency Failure and Degradation](../standards/fallback-strategy.md)

## 2. Update and Review the Plan

Add separate behavior milestones, for example:

1. `<Capability> Adapter/Degradation Tests — RED`
2. `<Capability> Adapter/Degradation Implementation — GREEN`
3. `<Capability> Refactor — REFACTOR` only when concrete cleanup is justified

The Plan must capture the approved business/engineering need, reduced guarantees, production guard/recovery expectations, and explicit exclusions. Obtain approval.

## 3. RED Milestone

Create a RED Implementation Plan containing only the exact tests/checks required by the approved behavior.

For a local adapter, this may include approved:

- capability contract tests;
- selector tests for implemented values;
- production-startup rejection test for local-only values;
- activation telemetry test where the project uses that telemetry.

For production degradation, this may include approved:

- dependency failure-path test;
- correctness/data-loss/idempotency assertions;
- recovery behavior test;
- health/metric behavior test where applicable.

Obtain approval, execute with `/generate-tests`, confirm valid RED, record evidence, and stop.

## 4. GREEN Milestone

Create a separate GREEN Implementation Plan referencing the RED evidence and defining only the minimum approved implementation.

Possible selectors, only when actually implemented by the service:

```text
MESSAGING_ADAPTER=kafka|pubsub|db|inmemory
CACHE_ADAPTER=redis|jsonfile|inmemory
STORAGE_ADAPTER=s3|gcs|local
SECRET_ADAPTER=vault|secretmanager|env
```

Local-only activation must follow the approved design, including production rejection and documented reduced guarantees. Production degradation must preserve required correctness/durability, be observable where required, define recovery, and avoid unapproved silent fail-open behavior.

Obtain approval, execute with `/implement-approved-plan`, verify GREEN, record evidence, and stop.

## 5. Optional REFACTOR Milestone

Only when concrete duplication/boundary cleanup remains after GREEN, create and approve a separate REFACTOR milestone. Keep all approved behavior and failure/guard tests GREEN.

## Completion Criteria

- [ ] Need classified as local adapter or production degradation
- [ ] RED and GREEN are separate approved milestones
- [ ] RED tests/checks failed for the expected approved behavior
- [ ] GREEN implementation is minimal and matches approved selector/failure behavior
- [ ] Reduced guarantees/recovery are documented where applicable
- [ ] Activation/degradation is observable where required by the operating model
- [ ] Any refactor was separate and preserved GREEN
