# Telemetry

Purpose
- Define what telemetry to collect (logs, metrics, traces) and how to name and expose them for alerting and diagnostics.

Mandatory Rules
- Record latency histograms for key RPCs and background jobs.
- Emit success/failure counters and request throughput per endpoint.
- Attach dimensional tags: `service`, `environment`, `region`, `instance_id`.

Defaults
- Buckets for latency histograms: p50, p95, p99 and use exponential histogram where supported.
- Metric units and names should follow `service.<component>.<metric>` naming.

Anti-patterns
- High-cardinality tags on metrics (e.g., user_id) that cause cardinality explosion.

LLM instructions
- When adding telemetry, instrument critical paths first (API, DB calls, message handlers) and add metric names to the code comments for consistency.
- Ask the user only if they require additional privacy-sensitive telemetry that may capture PII/PHI.

Review checklist
- [ ] Latency histograms present for key flows.
- [ ] Success/failure counters implemented.
- [ ] Metrics tagged with `service` and `environment`.
