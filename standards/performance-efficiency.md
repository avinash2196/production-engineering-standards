# Performance Efficiency

Purpose
- Provide pragmatic guidance to identify and avoid common performance pitfalls while retaining readable code.

Mandatory Rules
- Avoid N+1 database access patterns; prefer batching and projection queries for read-heavy flows.
- Enforce request/response size limits and guardrails on serialization/deserialization costs.

Defaults
- Use caching (CacheProvider) for idempotent read operations with clear TTL and invalidation rules.
- Default database query timeouts and circuit-breaker thresholds must be configured via `ConfigProvider`.

Anti-patterns
- Pulling entire tables into memory for filtering.
- Over-caching mutable sensitive data without invalidation strategy.

LLM instructions
- When optimizing queries, generate parameterized queries and recommend indexes; ask the user if schema changes are permitted.
- Do not apply aggressive micro-optimizations without benchmarks; request permission before introducing complexity.

Review checklist
- [ ] No N+1 queries on critical paths.
- [ ] Caching strategy documented with TTL and invalidation.
- [ ] Timeouts and circuit-breakers configured via config.
