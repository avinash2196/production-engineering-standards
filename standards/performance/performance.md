# Performance

Performance checklist covering database access patterns, batching, caching, connection management, and profiling guidance.

## Purpose

Define actionable performance standards that prevent common bottlenecks before they reach production.

## Mandatory Rules

### Database Access

- **No N+1 queries.** Use eager fetching, batch loading, or projections for associations.
- **Paginate all list queries.** No unbounded `SELECT *` — enforce page size limits (default 20, max 100).
- **Index all WHERE/JOIN columns.** New queries require an explain plan review.
- **Use read replicas** for reporting queries and dashboards.
- **Connection pool sizing:** Start with `max_connections = 2 * CPU_cores + disk_spindles` (typically 10–20 per instance). Monitor pool saturation via metrics.

```yaml
# Java — HikariCP defaults
spring:
  datasource:
    hikari:
      maximum-pool-size: 15
      minimum-idle: 5
      connection-timeout: 2000
      idle-timeout: 300000
      max-lifetime: 600000
```

```python
# Python — asyncpg pool
pool = await asyncpg.create_pool(
    dsn=DATABASE_URL,
    min_size=5,
    max_size=15,
    command_timeout=5,
)
```

### Caching

- **Cache at the service layer**, not the repository layer.
- Use `CacheProvider` abstraction (see `contracts/CacheProvider.md`).
- Default TTLs: entity lookup = 5 min, list/search = 1 min, config = 10 min.
- **Cache invalidation:** Prefer TTL expiry over event-driven invalidation unless strict consistency is required.
- **Cache-aside pattern:** Check cache → miss → load from DB → write to cache → return.

### Batching

- Batch database writes (bulk insert) for operations processing > 10 records.
- Batch Kafka publishes using `linger.ms` (default 5ms) for throughput.
- Batch HTTP calls using concurrent futures / async gather — never sequential loops.

### HTTP Response Times

| Tier | Target P95 | Example |
|------|------------|----------|
| Fast | < 50ms | Health checks, cached reads |
| Standard | < 250ms | Single-entity CRUD |
| Complex | < 1000ms | Multi-aggregate operations, search |
| Background | N/A | Async processing via events |

Endpoints consistently exceeding their tier target require a performance review.

### Payload Size

- JSON response bodies: max **1 MB** for synchronous endpoints.
- For larger payloads, use presigned URLs (storage) or streaming responses.
- Compress responses with gzip for payloads > 1 KB (enabled by default in both stacks).

### Async Processing

- Operations taking > 500ms should be made asynchronous where possible.
- Publish an event and return `202 Accepted` with a status-tracking endpoint.
- Never block an HTTP thread on a long-running Kafka publish — use `send()` (async), not `send().get()` (blocking).

## Profiling Guidance

### When to Profile

- Any endpoint exceeding its tier P95 target.
- Before and after adding caching or batching.
- Monthly review of top-10 slowest endpoints (from Prometheus/Grafana).

### Tools

| Stack | Profiler | Flame graph |
|-------|----------|-------------|
| Java | `async-profiler`, VisualVM | `jfr` + `jfr-flame-graph` |
| Python | `py-spy`, `cProfile` | `py-spy` generates SVG flamegraphs |

### Database Query Analysis

```sql
-- PostgreSQL: identify slow queries
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;
```

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| Loading all records then filtering in-app | Push WHERE clauses to the database |
| Caching at the repository level | Cache at service level through `CacheProvider` |
| Unbounded `IN (...)` clauses | Batch into chunks of 500 |
| Synchronous external HTTP calls in a loop | `CompletableFuture.allOf()` / `asyncio.gather()` |
| Missing connection pool limits | Set explicit pool sizes and monitor saturation |

## LLM Instructions

- When generating list endpoints, always include pagination parameters.
- When generating repository methods, check for N+1 patterns and suggest fetch joins.
- If a service method calls multiple external APIs sequentially, suggest concurrent execution.
- When adding caching, use the `CacheProvider` interface and specify a TTL.

## Review Checklist

- [ ] No N+1 queries in new code paths.
- [ ] List endpoints are paginated (max 100).
- [ ] Caching uses `CacheProvider` with explicit TTLs.
- [ ] Connection pool size is configured and monitored.
- [ ] No synchronous loops over external calls.
- [ ] Response payloads are under 1 MB.

## References

- [CacheProvider.md](../../contracts/CacheProvider.md)
- [observability.md](../observability.md)
- [coding-standards.md](../coding-standards.md)
