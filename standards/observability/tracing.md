# Distributed Tracing

> Parent overview: [Observability](../observability.md)

## Purpose

Use distributed tracing when cross-service or multi-dependency execution paths are difficult to diagnose with logs and metrics alone.

## When to Use

Tracing is commonly justified for:

- requests spanning multiple services;
- asynchronous workflows with difficult handoffs;
- dependency chains where latency attribution matters;
- critical workflows needing end-to-end execution visibility.

A standalone utility, simple CRUD service, or low-complexity worker may not need tracing if existing telemetry is sufficient.

## Implementation Guidance

When tracing is selected:

- use the platform/runtime's supported context-propagation standard;
- prefer W3C Trace Context for interoperable distributed HTTP/service traces unless the platform establishes another compatible mechanism;
- instrument boundaries and significant operations rather than every trivial in-memory call;
- record error status/context safely;
- propagate trace context across async/message boundaries where end-to-end traces are required;
- never place secrets or unnecessary sensitive data in span names/attributes.

OpenTelemetry is a preferred portable option when the project chooses portable tracing, not an automatically required dependency.

Sampling, exporter, backend, and instrumentation strategy are environment/workload decisions and should be configurable where needed.

## Anti-Patterns

- Installing tracing only because the service is called distributed.
- Creating excessive spans with no diagnostic value.
- Breaking trace context across asynchronous handoffs.
- Recording high-cardinality or sensitive payload data in attributes.
- Hardcoding collector/exporter endpoints.

## LLM Instructions

- Determine whether tracing is justified by the approved operating model before adding a tracing SDK.
- If tracing already exists, preserve the established context standard and instrumentation conventions.

## Review Checklist

- [ ] Tracing is justified by real diagnostic needs.
- [ ] Relevant boundaries propagate context correctly.
- [ ] Spans provide useful latency/error attribution without sensitive data.
- [ ] Sampling/export configuration fits the environment and is not hardcoded.
