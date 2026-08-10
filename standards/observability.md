# Observability Standard

## Purpose

Define the minimum observability outcomes required for production software without forcing the same telemetry mechanism into every service.

Observability is a production requirement. OpenTelemetry, Prometheus, a specific correlation header, or distributed tracing are implementation choices that must be selected because they fit the approved operating model.

## Core Principle

A production service must provide enough trustworthy telemetry to:

1. detect meaningful failures and service-health degradation;
2. diagnose important incidents without reproducing them locally;
3. understand the health of important dependencies and execution paths;
4. connect technical symptoms to business-impacting operations where appropriate;
5. support the approved SLOs, alerts, and operational ownership model when those are defined.

Do not invent SLOs, dashboards, tracing requirements, log fields, or monitoring products when requirements and the target platform have not established them.

## Required Invariants

### Logging

Production services must use an application logging mechanism appropriate to the runtime and deployment platform.

Logs must:

- use stable event names or otherwise machine-searchable structure for important operational events;
- include enough context to diagnose the event without requiring sensitive payloads;
- use appropriate levels consistently;
- avoid secrets, credentials, access tokens, private keys, and sensitive payloads;
- avoid PII/PHI or other classified data unless an explicitly approved policy permits a specific field and protection mechanism;
- record startup/shutdown and material configuration/runtime state only when doing so does not expose sensitive values.

Structured JSON is preferred when the target logging platform benefits from it, but the standard does not require one serialization format for every runtime.

### Correlation

Use correlation identifiers when an operation crosses boundaries and correlation materially improves diagnosis.

The identifier may be:

- an existing W3C trace identifier;
- a request identifier;
- a job/event/message identifier;
- a stable business operation identifier that is safe to log;
- another platform-standard correlation mechanism.

Do not mandate `X-Correlation-ID` when the approved platform already supplies an equivalent mechanism. Do not create identifiers merely to satisfy a checklist.

### Metrics

A production service must expose or emit metrics when quantitative runtime/service-health signals are needed to operate it safely.

Select metrics from the service's actual failure modes, workload, dependencies, and approved operational objectives. Common categories include:

- request/job/event throughput;
- latency or processing duration;
- error/failure outcomes;
- queue/backlog depth;
- saturation/resource pressure;
- dependency latency/error rates;
- retry/DLQ/reconciliation behavior;
- cache behavior;
- domain/business outcome counters where operationally useful.

The four golden signals are a useful review lens, not a mandatory metric set for every component.

Metrics must not contain high-cardinality sensitive values such as patient identifiers, raw document identifiers, tokens, or unbounded user-supplied values.

### Distributed Tracing

Distributed tracing is required when cross-service or multi-dependency execution paths are sufficiently important or complex that logs/metrics alone do not provide adequate diagnosis.

Tracing is normally justified for cases such as:

- request flows spanning multiple services;
- asynchronous workflows whose handoffs are difficult to diagnose;
- dependency chains where latency attribution matters;
- critical workflows requiring end-to-end execution visibility.

Do not require tracing for every standalone worker, batch utility, or simple service when it adds no material operating value.

OpenTelemetry is a preferred portable implementation when tracing or portable telemetry instrumentation is selected, but it is not an automatically installed dependency.

### Health and Readiness

A service must expose health/readiness behavior when the deployment target or operating model relies on it.

Health checks must distinguish what the platform actually needs to know. Do not create separate liveness/readiness endpoints solely because Kubernetes terminology exists if the target does not use those concepts.

Do not make a service appear healthy when a required dependency or startup guard makes it unable to perform its approved function.

### Alerting

Alerts must be tied to actionable service or business impact and have clear ownership.

Avoid alerts that:

- fire only because a low-level metric crosses an arbitrary threshold;
- duplicate platform alerts without added value;
- have no identified responder or action;
- expose sensitive data in notification payloads.

When SLOs or error budgets are explicitly approved, alerts should align with those objectives where practical.

## Dependency and Failure Observability

For important remote dependencies, observe the signals necessary to distinguish:

- local application failure;
- dependency failure;
- timeout;
- retry activity;
- rejected/circuit-open behavior when used;
- queued/deferred work;
- degraded/stale/bypassed behavior when used;
- recovery/reconciliation behavior when used.

Do not add every resilience metric to every integration. Instrument the behaviors that actually exist.

## Local Adapters

When a local-only adapter is selected, emit a clear startup warning. If the service already exposes application metrics and an adapter-active metric is useful, expose one.

A local adapter must never create false production-readiness evidence. Local adapter telemetry demonstrates local behavior, not the guarantees of Kafka, Redis, object storage, managed secrets, or another production dependency.

## Security and Privacy

Observability data is production data and must follow the service's approved data classification.

At minimum:

- never log secrets or authentication credentials;
- avoid sensitive request/response bodies by default;
- redact or omit sensitive fields at the source rather than relying only on downstream scrubbing;
- control access to logs, metrics, and traces according to their data sensitivity;
- define retention requirements only when the project or policy establishes them.

Healthcare terminology alone does not establish that HIPAA/PHI-specific telemetry controls apply. Apply those controls when requirements or approved data classification explicitly establish regulated health data handling.

## PDD Integration

Observability changes must follow the approved Plan and current phase-specific Implementation Plan.

The planner must not automatically add tracing, metrics libraries, dashboards, or alerting infrastructure because a service is described as "enterprise" or "healthcare".

When observability behavior is required:

- RED milestones may define tests/checks for important telemetry or production guards where executable verification is practical;
- GREEN milestones add only the approved telemetry behavior;
- REFACTOR milestones may improve instrumentation structure without changing approved observable behavior unless the Plan explicitly authorizes that behavior change.

## Review Questions

Use these questions during design/review:

1. What meaningful production failures must operators detect?
2. What evidence is needed to diagnose them?
3. Which identifiers safely connect related operations?
4. Which metrics correspond to actual workload, failure modes, dependencies, or approved SLOs?
5. Does cross-service tracing materially improve diagnosis?
6. Does the deployment platform require health/readiness semantics?
7. Could any telemetry expose sensitive or regulated data?
8. Are alerts actionable and owned?

If a material answer is missing and it affects the current Plan, ask the user rather than inventing it.

## Anti-Patterns

- Installing OpenTelemetry, Prometheus, or tracing libraries in every starter automatically.
- Mandating all four golden-signal metrics for components where some signals are meaningless.
- Requiring `X-Correlation-ID` when platform trace context already solves correlation.
- Logging payloads to make troubleshooting easier without considering data classification.
- High-cardinality metrics containing user, patient, document, or request-specific identifiers.
- Declaring production readiness because local adapter telemetry works.
- Inventing SLOs or alert thresholds during implementation.
