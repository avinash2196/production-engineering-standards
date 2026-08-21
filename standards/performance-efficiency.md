# Performance Efficiency

## Purpose

Provide pragmatic guidance for finding performance risks without turning generic optimization patterns into mandatory architecture.

## Mandatory Outcomes

- Avoid avoidable repeated work on performance-critical paths when evidence shows it is material.
- Bound request/response and batch sizes where unbounded work could threaten reliability or cost.
- Keep remote/database operations within the latency and resource limits established by the service requirements.
- Measure before introducing complexity that exists only for optimization.

## Contextual Techniques

Depending on the actual bottleneck, appropriate techniques may include:

- joins, batching, projection queries, or prefetching for N+1 access;
- caching for suitable read paths when freshness, invalidation, privacy, and failure semantics are defined;
- pagination/streaming for large result sets;
- indexes based on observed query patterns and database evidence;
- concurrency or asynchronous processing where ordering, resource limits, and failure behavior are understood.

A `CacheProvider`, `ConfigProvider`, circuit breaker, or particular timeout source is optional. Use an existing project/platform mechanism unless an abstraction is justified by the design.

## Anti-Patterns

- Pulling entire large datasets into memory for filtering when the data store can do the work safely.
- Adding caches without explicit freshness/invalidation and failure behavior.
- Adding concurrency without bounded resource use or correctness reasoning.
- Applying micro-optimizations without measurements.
- Inventing universal timeout, cache TTL, or circuit-breaker values.

## LLM Instructions

- Ask for or inspect evidence before recommending significant optimization.
- When suggesting database changes, distinguish query/code changes from schema/index changes and state when schema approval is required.
- Do not introduce `CacheProvider`, `ConfigProvider`, a circuit breaker, or async infrastructure merely because they exist in this repository.
- Preserve correctness and operability while optimizing.

## Review Checklist

- [ ] Material hot paths have evidence or a stated performance requirement.
- [ ] Repeated database/remote work is appropriate for the access pattern.
- [ ] Large/bulk operations are bounded.
- [ ] Any cache has explicit freshness, invalidation, privacy, and failure behavior.
- [ ] Timeout/resource controls come from the actual runtime/configuration model.
- [ ] Added optimization complexity is justified by measurable benefit or a concrete requirement.
