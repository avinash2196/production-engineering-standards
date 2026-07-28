# Production Dependency Failure and Degradation Strategy

## Purpose

Define what a live service does when a dependency is slow, unavailable, inconsistent, or returning errors. This is separate from local-development adapter selection.

## Required Decision

For every material external dependency, choose and document one or more behaviors:

- fail fast
- fail closed
- retry with bounded backoff
- circuit break
- queue durably for later processing
- serve stale data
- bypass a non-critical capability
- provide reduced functionality

Do not use “fallback” as a vague promise. Name the exact behavior and the guarantees that change.

## Decision Factors

- Could continuing produce incorrect business results?
- Could data be lost or duplicated?
- Is ordering required?
- Is the operation idempotent and replayable?
- Is stale data safer than unavailability?
- Does the dependency enforce authorization, secrets, rate limits, locks, or compliance?
- Can the system of record absorb cache-bypass load?
- How will users and operators know degraded mode is active?
- How does the service recover when the dependency returns?

## Default Safety Guidance

### Messaging unavailable

For non-loss-tolerant events, persist the event and business change atomically through an outbox or reject the operation. Do not silently replace durable messaging with an in-memory queue in production.

### Cache unavailable

Bypass a cache only when correctness does not depend on it and the system of record can safely handle load. Fail closed when cache state is used for authorization, distributed locks, rate limiting, or correctness-sensitive coordination.

### Secret provider unavailable

Fail closed. Do not silently use insecure, unknown, or expired credentials.

### Object storage unavailable

Reject the operation or persist a durable pending record according to the API contract. Do not report durable success before durable storage is confirmed unless the contract explicitly defines asynchronous acceptance.

### Downstream HTTP/gRPC unavailable

Define timeout budgets, retryable error classes, bounded attempts, idempotency requirements, and circuit-break behavior. Avoid retries that amplify load or duplicate non-idempotent operations.

## Observability

A degradation path must expose:

- structured activation/recovery logs
- metrics for activation, duration, failures, queue depth, stale responses, or bypasses
- health/readiness behavior appropriate to whether the service can safely operate
- alerts based on business and operational risk

## Test-First Changes

Dependency failure behavior is production behavior and follows the full PDD lifecycle:

1. Plan and Implementation Plan
2. failure-path tests first
3. valid RED
4. minimal behavior to GREEN
5. refactor after GREEN
6. production-readiness review

## Core Principle

> The fallback itself is not the standard. The standard is that degraded behavior is explicit, observable, testable, and unable to activate silently.

## LLM Instructions

- Do not assume every dependency should fail open.
- Treat security, secrets, authorization, and correctness controls as fail-closed by default.
- Require durable handling when data loss is unacceptable.
- Separate local adapters from production failure behavior.
- Include recovery and observability, not only activation behavior.

## Review Checklist

- [ ] Every material dependency has named failure behavior
- [ ] Correctness, data loss, duplication, ordering, and replay were considered
- [ ] Retry policy is bounded and safe for idempotency
- [ ] Degradation is observable and recoverable
- [ ] Failure-path tests exist
- [ ] Local adapters are not presented as production failover
