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

A degradation path must expose telemetry appropriate to its operational risk, such as:

- structured activation/recovery logs
- metrics for activation, duration, failures, queue depth, stale responses, or bypasses when those signals are useful
- health/readiness behavior appropriate to whether the service can safely operate
- alerts based on business and operational risk

Do not invent a specific observability mechanism merely because a degradation path exists; apply the repository observability standard and approved operating model.

## Test-First Changes

Dependency failure behavior is production behavior and follows the full phase-milestone PDD lifecycle:

1. Define or confirm the behavior in the approved Plan. If material failure semantics are unresolved, ask the user and stop rather than inventing them.
2. Create and review a **RED milestone Implementation Plan** for failure-path tests only.
3. Execute the RED milestone, confirm valid RED for the expected missing behavior, record evidence, and stop.
4. Create and review a separate **GREEN milestone Implementation Plan** for the minimum approved degradation/failure behavior.
5. Execute the GREEN milestone, reach GREEN, run regression checks, record evidence, and stop.
6. Use a separate **REFACTOR milestone and Implementation Plan only when justified**, preserving observable behavior and GREEN tests.
7. Perform production-readiness review using applicability-based evidence.

A request for end-to-end implementation does not waive the separate Plan or phase-specific Implementation Plan review gates.

## Core Principle

> The fallback itself is not the standard. The standard is that degraded behavior is explicit, observable, testable, and unable to activate silently.

## LLM Instructions

- Do not assume every dependency should fail open.
- Treat security, secrets, authorization, and correctness controls as fail-closed unless approved requirements or architecture explicitly define another safe behavior.
- Require durable handling when approved requirements establish that data loss is unacceptable.
- Separate local adapters from production failure behavior.
- Include recovery and observability, not only activation behavior.
- Do not collapse RED, GREEN, and optional REFACTOR work into one Implementation Plan.

## Review Checklist

- [ ] Every material dependency has named failure behavior when that decision is required by the current scope
- [ ] Correctness, data loss, duplication, ordering, and replay were considered
- [ ] Retry policy is bounded and safe for idempotency
- [ ] Degradation is observable and recoverable
- [ ] Failure-path RED evidence exists before GREEN implementation
- [ ] RED and GREEN used separate approved milestones and Implementation Plans
- [ ] Local adapters are not presented as production failover
