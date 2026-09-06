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

A fallback is not automatically safer. Degraded behavior must be explicit, observable, testable, bounded, and unable to activate silently.

Read `references/local-adapters-vs-production-degradation.md` when local development behavior is involved.

