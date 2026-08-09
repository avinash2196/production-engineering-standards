# Performance and Efficiency

## Purpose

Provide reviewable performance guidance without pretending one latency target, page size, cache TTL, batch size, pool size, or asynchronous threshold fits every service.

## Mandatory Rules

1. Define performance targets from approved requirements, measured baselines, business impact, and downstream capacity.
2. Bound list operations and unbounded work. Choose pagination and payload limits from cardinality, payload size, client behavior, and measured latency.
3. Review query plans for critical or high-volume database access paths. Add indexes based on selectivity and measured access patterns rather than indexing every filtered column automatically.
4. Configure connection pools with explicit bounds derived from database capacity, service instance count, concurrency, query latency, and load testing. Monitor saturation.
5. Cache only when correctness permits it. Derive TTL and invalidation behavior from freshness requirements and failure semantics.
6. Use batching and producer/client tuning only after measuring the workload and downstream limits.
7. Use bounded concurrency only for independent work and only when downstream capacity can absorb it.
8. Choose synchronous versus asynchronous execution from the API/business contract, latency budget, durability requirements, user workflow, and failure semantics.
9. Establish a baseline before claiming an optimization and record the measurement method used to verify improvement.

## Decision Guidance

### Database

- Investigate N+1 access, repeated queries, large scans, lock contention, connection saturation, and missing/ineffective indexes using evidence from plans and metrics.
- Prefer query and schema changes that improve the measured bottleneck rather than adding generic indexes.

### Caching

- Document what is cached, freshness tolerance, invalidation behavior, stampede/hot-key risks, and behavior when the cache is unavailable.
- Treat a cache as a performance optimization unless the business contract explicitly depends on it for correctness.

### External Calls and Concurrency

- Parallelize independent I/O only when the combined load is safe for downstream systems and cancellation/timeouts are bounded.
- Do not hide blocking work behind asynchronous syntax; measure thread/event-loop utilization and queueing.

### Messaging and Batching

- Choose batch size, producer buffering, linger, compression, and concurrency from throughput/latency goals and measured broker/client behavior.
- Preserve ordering, idempotency, and durability requirements while tuning throughput.

### API Payloads

- Bound response sizes and list cardinality.
- Use compression based on client/server support and measured benefit rather than a repository-wide byte threshold.

## Anti-patterns

- Universal numeric performance targets copied into every service.
- Indexing every `WHERE`/`JOIN` column without query-plan evidence.
- Increasing thread or connection pools without considering downstream capacity.
- Adding a cache without a freshness/invalidation contract.
- Parallelizing dependent work or overwhelming downstream services.
- Declaring an operation asynchronous solely because it crosses an arbitrary duration threshold.

## LLM Instructions

- Do not invent latency, throughput, pagination, TTL, pool-size, batch-size, or payload targets when requirements are missing.
- Ask for or derive targets from documented SLOs/requirements and measured baselines.
- When identifying a performance concern, name the evidence to collect and the trade-off of the proposed change.
- Prefer a measurable hypothesis: baseline → change → repeat measurement → compare.

## Review Checklist

- [ ] Performance targets come from requirements or an explicitly documented baseline.
- [ ] High-volume list operations and work queues are bounded.
- [ ] Critical database paths have evidence-based query/index review.
- [ ] Connection/thread/worker pools are bounded and monitored.
- [ ] Cache freshness and failure behavior are documented where caching is used.
- [ ] Concurrency and batching respect downstream capacity and correctness semantics.
- [ ] Claimed improvements include a reproducible measurement method.

## References

- [Observability](../observability.md)
- [Resiliency](../resiliency.md)
- [Scalability](../scalability.md)
