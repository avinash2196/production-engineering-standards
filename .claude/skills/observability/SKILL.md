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

## Logging Rules

Severities follow `code-quality`.

| ID | Rule | Severity |
| --- | --- | --- |
| LG1 | Levels: ERROR when someone must act, WARN for a handled problem worth counting, INFO for business events, DEBUG for diagnostics. | Medium |
| LG2 | Log a failure once, where it is handled. No log-and-rethrow. | Medium |
| LG3 | Never log secrets, tokens, personal data, full payloads, or file names that can carry personal data. | High |
| LG4 | Each log line carries the correlation ID and the stable identifiers needed to trace it. | Medium |
| LG5 | No empty catch blocks and no swallowed exceptions. | High |
