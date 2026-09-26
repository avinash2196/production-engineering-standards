---
name: resilience-and-degradation
description: Use when handling dependency failures, retries, timeouts, circuit breaking, fallback, stale data, queues, or reduced-functionality modes.
---

# Resilience and Degradation

Choose failure behavior deliberately:

- fail fast
- fail closed
- bounded retry with backoff/jitter
- circuit break
- queue durably
- serve explicitly stale data
- bypass a non-critical capability
- operate in reduced functionality

Choose by the role the dependency plays, not by its product name:

- **Cache** (the data also lives in a system of record): bypass to the system of record, bounded by timeouts, and make the extra load observable.
- **Coordination or protection** (distributed lock, rate limiter, idempotency keys, session store): usually fail closed — a local substitute silently breaks the guarantee across instances.
- **Messaging** (events another system relies on): prefer durable publication, for example a transactional outbox — record the event in the same database transaction as the business change and publish it asynchronously — over dropping, blocking indefinitely, or buffering to a local file.
- **System of record:** there is no substitute; fail and surface the failure.

Local files and in-memory stores are not production fallbacks when instances are multiple, replaceable, or run on ephemeral disks: data is lost on restart, and ordering and deduplication break across instances.

A fallback is not automatically safer. Degraded behavior must be explicit, observable, testable, bounded, and unable to activate silently.

Read `references/local-adapters-vs-production-degradation.md` when local development behavior is involved.

