# CacheProvider

## Purpose

Define a stable cache capability for application code without coupling cache policy to Redis or a local implementation.

## Contract

Common operations include `get`, `set/put` with TTL, and `delete`. Add atomic operations such as `putIfAbsent`, compare-and-set, or counters only when the selected implementation and business requirement need them.

Document for each use:

- system of record;
- key namespace;
- TTL and invalidation owner;
- serialization format;
- stale-data tolerance;
- behavior when the cache is unavailable;
- whether correctness depends on atomic/distributed behavior.

## Safety Guidance

A cache may be bypassed only when correctness does not depend on it and the system of record can handle the load. Do not apply generic fail-open behavior to authorization, rate limiting, idempotency, locks, or coordination.

## Production and Local Implementations

| Selection | Use | Limitation |
|---|---|---|
| `redis` | production cache/coordination when approved | platform semantics and operational dependency |
| `jsonfile` | inspectable local cache | no distributed atomicity or safe multi-process consistency |
| `inmemory` | isolated tests | process-local and lost on restart |

Local-only values are rejected in production.

## Composition

```java
@Bean
@ConditionalOnProperty(name = "adapters.cache", havingValue = "jsonfile")
CacheProvider jsonFileCache(LocalCacheProperties properties) {
    return new JsonFileCacheProvider(properties.path());
}
```

```python
if settings.cache_adapter is CacheAdapter.JSON_FILE:
    return JsonFileCacheProvider(settings.json_cache_path)
```

## Test-First Requirements

- hit/miss behavior;
- TTL expiry;
- invalidation;
- serialization errors;
- selected unavailable-cache behavior;
- JSON-file malformed data/atomic replacement;
- provider selection and production rejection;
- Redis integration for required atomic operations.

## Observability

Track hits, misses, writes, errors, and latency where useful. Emit a local-adapter activation warning. Never log sensitive cached values.

## Review Checklist

- [ ] Cache is not treated as source of truth without explicit design
- [ ] TTL and invalidation are owned
- [ ] Failure behavior is safe for this use
- [ ] Atomic/distributed requirements are not tested only with local adapters
- [ ] Local selector and production guard tests exist
