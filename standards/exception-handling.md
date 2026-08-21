# Exception Handling

## Purpose

Make failures explicit, safely translated at boundaries, and diagnosable without leaking sensitive/internal details.

## Rules

- Do not silently swallow failures.
- Preserve useful root-cause context when translating/wrapping exceptions.
- Use typed/domain/application error categories when callers need distinct handling; do not create an exception class for every message.
- Translate internal failures at transport/interface boundaries according to the actual protocol/error contract.
- Unexpected failures should produce sufficient secure diagnostic context using the project's observability mechanism.
- External responses must not expose stack traces, credentials, raw SQL, internal paths/topology, or sensitive payloads.

A central exception mapper, `errorCode`, `traceId`, or specific error envelope is optional unless the target framework/API contract adopts it.

## Retry Interaction

Exception handling must not convert deterministic validation/auth/business failures into retryable failures. Preserve enough classification for the approved retry/failure policy to behave correctly.

## LLM Instructions

- Reuse the project's existing error model and framework handler before introducing new infrastructure.
- Include correlation/operation context when available; do not create a custom ID solely to satisfy this document.
- Keep client-safe messages separate from secure internal diagnostics.

## Review Checklist

- [ ] Failures are handled or propagated intentionally.
- [ ] Boundary translation matches the protocol/API contract.
- [ ] Root cause/context is preserved for diagnostics without sensitive leakage.
- [ ] Retry classification remains correct.
