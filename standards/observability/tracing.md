# Tracing

> Parent overview: [standards/observability.md](../observability.md)

Purpose
- Enable end-to-end request tracing across service boundaries to diagnose latency, failures, and distributed flow issues.

Mandatory Rules
- Use OpenTelemetry SDK for trace instrumentation. All services must participate in the same trace context propagation (W3C Trace Context format).
- Create a span for every inbound request (controller/handler), outbound service call (HTTP, gRPC, messaging), and significant internal operation (database query, cache lookup).
- Span names must be descriptive: `<verb> <resource>` (e.g., `GET /api/orders`, `publish order.created`, `query orders_table`).
- Set span status to `ERROR` and record exception details when operations fail.
- Never include secrets, tokens, or full PII in span attributes. Redact sensitive fields.

Defaults
- Java: OpenTelemetry Java agent (auto-instrumentation) + manual spans for business-critical paths. Configure via `OTEL_SERVICE_NAME`, `OTEL_EXPORTER_OTLP_ENDPOINT`.
- Python: `opentelemetry-instrumentation-fastapi` for auto-instrumentation + `tracer.start_as_current_span()` for manual spans.
- Sampling: use parent-based sampling with a default rate of 1.0 in dev, configurable via `OTEL_TRACES_SAMPLER_ARG` in production.

Anti-patterns
- Creating spans for trivial in-memory operations (noise).
- Not propagating trace context across async boundaries (message publish/subscribe).
- Hardcoding exporter endpoints instead of using environment configuration.

LLM instructions
- When adding a new service call or external integration, wrap it in a span with descriptive name and error handling.
- Ensure message publishers inject trace context into message headers and subscribers extract it.

Review checklist
- [ ] OpenTelemetry configured with W3C Trace Context propagation.
- [ ] Spans created for inbound requests, outbound calls, and DB/cache operations.
- [ ] Span errors recorded with exception details.
- [ ] Trace context propagated across async/messaging boundaries.
