# Resiliency

Purpose
- Define patterns for making services resilient to transient failures and partial outages.

Mandatory Rules
- Implement retries with exponential backoff and capped limits for idempotent operations.
- Apply timeouts and circuit breakers around remote calls.
- Ensure operations are safe to retry (idempotency tokens or deduplication) or move to asynchronous processing.

Defaults
- Retry policy: initial 100ms, multiplier 2.0, max attempts configurable via `ConfigProvider`.
- Use circuit-breaker thresholds based on error rate and latency percentiles.

Anti-patterns
- Blindly retrying non-idempotent operations.
- No timeouts on remote calls leading to resource exhaustion.

LLM instructions
- When adding retry logic, add idempotency key requirements and fallback routing to asynchronous processing if necessary.
- Ask the user when operation semantics are unknown or when retries may cause duplicate side-effects.

Review checklist
- [ ] Retries and backoff implemented for transient errors.
- [ ] Circuit breakers present for remote dependencies.
- [ ] Idempotency or deduplication strategies defined for retryable flows.
