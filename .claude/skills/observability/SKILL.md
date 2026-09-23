---
name: observability
description: Use when designing or reviewing logs, metrics, traces, correlation, SLO signals, alerts, and failure visibility.
---

# Observability

Instrument user-visible and operationally meaningful behavior.

- structured logs with safe identifiers
- metrics for throughput, latency, errors, saturation, retries, queue depth, cache behavior, and migration progress where relevant
- traces/correlation across remote boundaries
- alerts tied to actionable failure or SLO impact
- explicit signals when degraded mode activates

Do not log secrets or sensitive payloads merely for debugging convenience.

