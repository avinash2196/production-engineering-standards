---
name: distributed-systems
description: Use when a change involves asynchronous messaging, concurrency, caching, distributed coordination, retries, consistency, ordering, or duplicate delivery.
---

# Distributed Systems

Review the concrete execution path for:

- delivery semantics and duplicates
- idempotency and deduplication
- ordering requirements
- consistency model
- concurrency races
- cache invalidation and staleness
- retry amplification
- backpressure and queue growth
- partial failure and recovery
- timeouts and cancellation
- observability across boundaries

Do not use distributed patterns such as CQRS, event sourcing, sagas, or consensus mechanisms unless the problem actually requires them.

