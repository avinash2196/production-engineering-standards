# Cache Integration — Python FastAPI

## Purpose

Wire Redis behind `CacheProvider` while supporting explicit JSON-file or in-memory local adapters when approved. A local cache is not a substitute for Redis coordination, distributed locks, rate limiting, or correctness-sensitive atomic operations.

## Required Workflow

1. Plan what is cached, source of truth, TTL, invalidation, stale-data behavior, and failure impact.
2. Approve exact implementation/test files.
3. Add failing tests for TTL, invalidation, serialization, selection, and production guards.
4. Implement the smallest adapter behavior.
5. Run unit and Redis integration tests.
6. Refactor only after green.

## Typed Selection

```python
class CacheAdapter(StrEnum):
    REDIS = "redis"
    JSON_FILE = "jsonfile"
    IN_MEMORY = "inmemory"
```

```python
def get_cache(settings: Settings) -> CacheProvider:
    if settings.cache_adapter is CacheAdapter.JSON_FILE:
        return JsonFileCacheProvider(settings.json_cache_path)
    if settings.cache_adapter is CacheAdapter.IN_MEMORY:
        return InMemoryCacheProvider()
    return RedisCacheProvider(settings.redis_url)
```

Production startup rejects `JSON_FILE` and `IN_MEMORY`.

## Redis Requirements

- Set connection and command timeouts.
- Define behavior when Redis is unavailable: bypass cache, serve stale data, or fail closed depending on use.
- Use namespaced keys such as `{service}:{entity}:{id}`.
- Apply TTL deliberately; avoid permanent entries without ownership and invalidation.
- Avoid scanning large keyspaces on request paths.
- Do not use optional-cache degradation for authorization, distributed locks, idempotency, or rate limiting without a correctness review.

## JSON-File Local Adapter

The file-backed adapter is useful because values survive a process restart and can be inspected directly. It remains process-local and lacks distributed atomicity or safe multi-process writes.

Tests should prove:

- value round trip;
- TTL expiry;
- delete behavior;
- malformed-file error behavior;
- atomic replacement of the file;
- production rejection.

## Observability

Track hits, misses, writes, errors, operation latency, and whether a local adapter is active. Do not log cached sensitive values.

## Verification

- unit tests for cache policy in application code;
- contract tests shared across adapters where practical;
- Testcontainers Redis tests for serialization and TTL;
- local JSON-file tests using a temporary directory;
- production guard and provider-selection tests.

## References

- [CacheProvider](../../../contracts/CacheProvider.md)
- [Cache local adapter detail](../../../standards/local-adapters/cache-local-adapter.md)
- [Production dependency failure strategy](../../../standards/fallback-strategy.md)
