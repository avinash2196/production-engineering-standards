# Correlation and Operation Identifiers

> Parent overview: [Observability](../observability.md)

## Purpose

Preserve enough identity across related work to correlate logs, traces, messages, and asynchronous processing when cross-boundary diagnosis requires it.

## Decision Guidance

Use an existing correlation mechanism whenever possible. Examples include:

- W3C trace/span identifiers;
- a platform request identifier;
- a job/event/message identifier;
- a safe business-operation identifier;
- a custom correlation header when no suitable mechanism already exists.

A custom `X-Correlation-ID` + UUID v4 scheme is one valid implementation, not a universal requirement.

## Required Behavior When Correlation Is Used

- Preserve the chosen identifier across the boundaries where end-to-end correlation is needed.
- Define trust/validation behavior for caller-supplied identifiers.
- Avoid high-cardinality identifiers in metrics labels.
- Avoid sensitive values as correlation identifiers.
- Propagate context across asynchronous/reactive boundaries using the runtime's supported context mechanism.

## Anti-Patterns

- Generating a new identifier at every boundary and breaking the intended chain.
- Creating a second custom correlation ID when tracing/platform context already solves the problem.
- Using thread-local-only storage in code that crosses async/reactive execution without propagation support.
- Logging sensitive business identifiers solely for correlation convenience.

## LLM Instructions

- First determine whether the project already uses W3C tracing, request IDs, job/message IDs, or another correlation mechanism.
- Add custom correlation middleware/headers only when the approved design needs them.

## Review Checklist

- [ ] A correlation mechanism exists only where diagnosis requires it.
- [ ] The established identifier is propagated across relevant boundaries.
- [ ] Async/reactive context propagation is correct.
- [ ] Sensitive/high-cardinality identifiers are not misused.
