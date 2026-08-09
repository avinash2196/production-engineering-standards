# Workflow: Add a Local Adapter or Production Degradation Path

## Purpose

Decide whether a dependency concern is a **local-development adapter** or a **production failure/degradation behavior**, then implement it through the PDD lifecycle. Do not combine the two concepts under a vague fallback toggle.

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

- fail closed when secrets are unavailable
- durably queue an event when a broker is unavailable
- bypass a non-critical cache when the database can absorb load
- return stale data under an approved freshness contract

Reference: [Production Dependency Failure and Degradation](../standards/fallback-strategy.md)

## 2. Plan and Review

Update `docs/.ai/Plan.md` with the capability, business need, reduced guarantees, and scope. Create a milestone Implementation Plan with exact contract, selector, tests, code, telemetry, production guard, and recovery behavior.

Obtain approval before tests or source changes.

## 3. RED — Tests First

For a local adapter, write:

- capability contract tests
- selector tests for production and local values
- production-startup rejection test for local-only values
- telemetry activation test where practical

For production degradation, write:

- dependency failure-path test
- correctness/data-loss/idempotency assertions
- recovery behavior test where relevant
- health/metric behavior test where relevant

Confirm valid RED.

## 4. GREEN — Minimal Implementation

Standard selectors:

```text
MESSAGING_ADAPTER=kafka|pubsub|db|inmemory
CACHE_ADAPTER=redis|jsonfile|inmemory
STORAGE_ADAPTER=s3|gcs|local
SECRET_ADAPTER=vault|secretmanager|env
```

Implement only values approved and tested by the service. Selection must be typed and explicit.

Local-only activation must:

- emit a structured warning
- expose an adapter-active metric when the project has application metrics
- document reduced guarantees
- fail startup in production

Production degradation must:

- preserve required correctness and durability
- be observable
- define recovery
- avoid silent fail-open behavior

## 5. REFACTOR

After GREEN, extract shared selector, telemetry, or mapping code only when it reduces real duplication. Keep all contract and failure tests GREEN.

## Completion Criteria

- [ ] Need classified as local adapter or production degradation
- [ ] Plan and Implementation Plan approved
- [ ] Contract/failure tests were RED first
- [ ] Typed selector and production guard implemented where applicable
- [ ] Reduced guarantees and recovery documented
- [ ] Activation/degradation observable
- [ ] Refactor preserved GREEN
