# Resiliency

## Purpose

Define how services make dependency failure explicit, bounded, observable, and safe for the operation being performed.

## Mandatory Rules

- All remote calls must have bounded timeouts appropriate to the end-to-end latency budget.
- Retry, circuit breaking, bulkheads, durable queueing, fail-fast, fail-closed, stale-data, or bypass behavior is selected according to operation semantics and failure impact; no single pattern is mandatory for every dependency.
- Retries are allowed only when duplicate execution is safe, idempotency/deduplication controls exist, or the operation explicitly tolerates duplicate effects.
- Retry attempts, total retry time, backoff, queues, and concurrency must be bounded.
- Recovery and degraded behavior must be observable and tested where they affect correctness or availability.

## Decision Guidance

- **Timeouts:** compose downstream timeouts within the caller's end-to-end budget and include queueing/retry time.
- **Retries:** use only for failures likely to be transient; exclude deterministic validation/business failures and respect downstream overload signals.
- **Circuit breakers:** use when failing quickly protects the caller/downstream from repeated expensive failures. Do not add one merely to satisfy a checklist.
- **Bulkheads/concurrency limits:** use where shared pools or dependencies need isolation from overload.
- **Durable asynchronous paths:** use when the business contract permits delayed completion and the system needs to survive dependency outages without data loss.

Retry budgets, backoff, and attempt limits are dependency-specific and must be bounded and observable; this repository does not prescribe universal timing values.

## Anti-patterns

- Blindly retrying non-idempotent operations.
- No timeout on remote calls.
- Unbounded retry queues or executor queues.
- Silently switching to a weaker local adapter in production.
- Treating circuit breakers or retries as substitutes for capacity planning and backpressure.

## LLM Instructions

- Determine operation semantics, business impact, idempotency, latency budget, and downstream limits before selecting resiliency patterns.
- If semantics are unknown, identify the missing decision rather than inventing a retry count or degradation mode.
- Keep production degradation separate from local-development adapter selection.

## Review Checklist

- [ ] Remote calls have bounded timeouts.
- [ ] Retry behavior is safe for duplicate effects and bounded.
- [ ] Failure/degradation behavior is explicit for important dependencies.
- [ ] Overload/backpressure behavior is considered where concurrency or queues exist.
- [ ] Recovery and degraded behavior are observable and tested where relevant.
