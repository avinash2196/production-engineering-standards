# Metrics

> Parent overview: [Observability](../observability.md)

## Purpose

Define metrics that make the service's real health, workload, dependencies, and failure modes measurable without forcing a universal metric library or fixed metric set.

## Selection

Choose metrics from actual operational questions. Useful categories may include:

- throughput/work completed;
- latency or processing duration;
- error/failure outcomes;
- queue/backlog depth;
- saturation/resource pressure;
- dependency latency/error rates;
- retry, circuit-breaker, DLQ, or reconciliation behavior;
- cache behavior;
- business outcomes that operators genuinely use.

The four golden signals are a review lens, not a requirement that every service emit all four directly.

## Naming and Labels

Follow the conventions of the selected metrics platform and the adopting organization. Use standard units where the platform expects them and stable names that survive implementation refactors.

Labels/dimensions must remain bounded. Do not use user IDs, request IDs, unbounded document/order IDs, tokens, or other high-cardinality/sensitive values.

## Mechanisms

Micrometer, Prometheus, OpenTelemetry Metrics, cloud-native metrics, or another platform mechanism may be appropriate. Select the mechanism from the approved runtime/operating model rather than installing one automatically.

## Anti-Patterns

- Emitting every golden signal only to satisfy a checklist.
- Creating arbitrary thresholds without SLO/baseline evidence.
- High-cardinality labels.
- Duplicating platform metrics without operational value.
- Treating a `/metrics` endpoint as mandatory when the platform uses another export path.

## LLM Instructions

- Ask what operators need to detect/diagnose or derive metrics from documented failure modes and SLOs.
- Do not invent metric products, exporters, label schemas, or alert thresholds.

## Review Checklist

- [ ] Metrics answer concrete operational questions.
- [ ] Names/units follow the selected platform convention.
- [ ] Labels are bounded and non-sensitive.
- [ ] Dependency/degradation behavior is measurable where it matters.
