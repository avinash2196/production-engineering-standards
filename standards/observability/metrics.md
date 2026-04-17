# Metrics

> Parent overview: [standards/observability.md](../observability.md)

Purpose
- Define canonical metric names, types, and labeling conventions that enable consistent dashboards, alerts, and SLO tracking across all services.

Mandatory Rules
- Every service must emit the four golden signals: **latency**, **error rate**, **throughput**, **saturation**.
- Metric names must follow the pattern: `<service>_<subsystem>_<signal>_<unit>` (e.g., `orders_api_request_duration_seconds`).
- Use standard units: `_seconds` for durations, `_bytes` for sizes, `_total` for counters.
- Label dimensions must include: `service`, `environment`, `method`, `status` (HTTP status code family or gRPC code).
- Avoid high-cardinality labels (no user IDs, request IDs, or unbounded enum values in metric labels).

Defaults
- Java: Micrometer with Prometheus registry. Use `@Timed` and `@Counted` annotations for controller/service methods.
- Python: `prometheus_client` or OpenTelemetry metrics SDK. Register metrics in a shared registry module.
- Export format: Prometheus exposition format (`/metrics` endpoint) or OpenTelemetry OTLP.

Anti-patterns
- Custom metric names that diverge from naming convention (prevents dashboard reuse).
- Not emitting error metrics for caught exceptions that represent degraded behavior.
- Emitting metrics with user-specific labels (causes cardinality explosion).

LLM instructions
- When adding a new endpoint or service call, emit latency (histogram) and error (counter) metrics following the naming convention.
- Do not add user-specific or request-specific labels to metrics.

Review checklist
- [ ] Four golden signals emitted for every service boundary.
- [ ] Metric names follow `<service>_<subsystem>_<signal>_<unit>` convention.
- [ ] No high-cardinality labels.
- [ ] Metrics endpoint exposed and scrapeable.
