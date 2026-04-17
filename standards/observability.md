# Observability

Purpose
- Ensure failures and performance issues are visible, diagnosable, and actionable across distributed services.

Mandatory Rules
- Emit structured logs, metrics (latency, error, throughput, saturation), and distributed traces.
- Propagate a correlation ID across process and network boundaries (use header `X-Correlation-ID`).
- Include environment and service identifiers in metrics and logs.

Defaults
- Use OpenTelemetry for traces and common metric names (see `metrics` conventions in `standards/observability/metrics.md`).
- Log in JSON structured format with severity, timestamp, service, traceId, and spanId.

Anti-patterns
- Relying on ad-hoc println/logging without structure; not including correlation IDs.

LLM instructions
- When instrumenting code, inject correlation ID at the controller edge and add spans for service-to-service calls.
- Ask the user only if there are platform constraints (e.g., legacy logging pipeline) that prevent standard instrumentation.

Review checklist
- [ ] Structured logging enabled.
- [ ] Metrics exported to monitoring system.
- [ ] Tracing configured and correlation IDs propagated.

---

## Deep-Dive Guides

For detailed guidance on each pillar, see:

| Pillar | Guide |
|--------|-------|
| Structured logging | [observability/logging.md](observability/logging.md) |
| Metrics & naming | [observability/metrics.md](observability/metrics.md) |
| Distributed tracing | [observability/tracing.md](observability/tracing.md) |
| Correlation IDs | [observability/correlation-ids.md](observability/correlation-ids.md) |
