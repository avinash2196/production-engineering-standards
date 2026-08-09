# Local Adapter Behavior Walkthrough

This directory documents the expected behavior of local messaging, cache, storage, and secret adapters. It does **not** currently contain an executable service.

The examples preserve an important engineering distinction:

- local adapters support development and selected tests without managed infrastructure;
- production degradation defines what a live service does when a dependency fails.

They must not be treated as the same mechanism.

## Illustrative Local Configuration

```bash
MESSAGING_ADAPTER=db
CACHE_ADAPTER=jsonfile
STORAGE_ADAPTER=local
SECRET_ADAPTER=env
```

| Capability | Local implementation | Useful property | Reduced guarantees |
|---|---|---|---|
| Messaging | Database outbox/table queue | durable across process restart and inspectable with SQL | no Kafka partitions, consumer groups, rebalancing, or equivalent throughput |
| Messaging | In-memory queue | minimal setup for narrow tests | process-local and lost on restart |
| Cache | JSON file | inspectable and retained across restart | no distributed atomicity, locking, or consistency |
| Cache | In-memory map | fast isolated tests | process-local and ephemeral |
| Storage | Local filesystem | easy inspection and deterministic local testing | no managed durability, lifecycle, replication, or cloud IAM behavior |
| Secrets | Environment variables | simple local bootstrap | no managed rotation, centralized policy, or secret audit trail |

## Expected Safeguards

Every local-only implementation should:

1. implement the same capability contract used by production code;
2. activate only through typed configuration;
3. emit a structured warning at activation and, when the project exposes application metrics, an adapter-active metric;
4. document durability, ordering, consistency, concurrency, and security differences;
5. fail application startup when selected in production;
6. have tests for selection and production rejection.

## Illustrative Flow

```text
approved plan
  -> approved implementation plan
  -> failing adapter-selection/guard tests
  -> smallest provider and adapter implementation
  -> green tests
  -> refactor with no behavior change
```

## What This Walkthrough Does Not Claim

- A database outbox is not a drop-in Kafka replacement.
- A JSON file does not reproduce Redis atomic operations or distributed locks.
- Local filesystem storage does not reproduce object-store durability or access controls.
- Environment-backed secrets are not an acceptable automatic production fallback.
- A service is not production-ready because local adapters work.

## References

- [Run with local adapters](../../playbooks/local-dev/run-with-local-adapters.md)
- [Local adapter strategy](../../standards/local-adapter-strategy.md)
- [Production dependency failure strategy](../../standards/fallback-strategy.md)
- [Python adapter tests](../../stacks/python-fastapi/project-template/tests/)
