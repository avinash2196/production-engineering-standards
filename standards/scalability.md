# Scalability

## Purpose

Make capacity limits, bottlenecks, and scaling behavior explicit for systems whose workload requires scaling beyond a single baseline deployment.

## Guidance

- Establish expected workload and limiting resources before choosing a scaling pattern.
- Prefer stateless/restartable compute when it matches the application, but do not externalize state merely to satisfy a stateless-service convention.
- Identify stateful bottlenecks such as database connections, hot partitions, locks, queues, caches, external quotas, and downstream capacity.
- Use horizontal scaling, vertical scaling, partitioning/sharding, batching, async processing, caching, replication, or workload isolation according to measured requirements and correctness constraints.
- Define capacity signals/limits and overload behavior for critical resources.

Autoscaling is optional. If used, select signals and thresholds from observed workload/SLO/resource behavior; do not invent CPU/RPS thresholds.

Partitioning/sharding is optional. If used, define key distribution, hot-key behavior, rebalancing/migration, consistency, and failure implications.

## Anti-Patterns

- Claiming scalability without workload/capacity evidence.
- Unbounded queues/concurrency/connections.
- Global mutable in-process state when multiple instances are expected and no synchronization/reconciliation model exists.
- Adding distributed complexity before a real bottleneck/requirement exists.

## LLM Instructions

- Ask for or inspect workload, latency/throughput targets, state ownership, and platform constraints before proposing scaling mechanisms.
- State the bottleneck each proposed mechanism addresses.
- Do not invent autoscaling thresholds or multi-region requirements.

## Review Checklist

- [ ] Workload/capacity assumptions are explicit.
- [ ] Material bottlenecks and limits are identified.
- [ ] Scaling mechanism preserves correctness/state semantics.
- [ ] Overload/backpressure behavior is bounded.
