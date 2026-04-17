# CacheProvider

## Purpose

Define the capability interface for caching data with explicit TTL, eviction, consistency, and observability contracts. Services depend on this abstraction, never directly on Redis, Memcached, or any specific cache engine.

## Interface Contract

- `get(key)` → returns value or `null`/`None` (cache miss).
- `put(key, value, ttl)` → stores value with mandatory TTL. No permanent entries allowed.
- `putIfAbsent(key, value, ttl)` → atomic set-if-not-exists. Returns `true` if stored, `false` if key existed.
- `evict(key)` → removes a single entry.
- `evictByPrefix(prefix)` → removes all entries matching prefix (use sparingly).

## Required Semantics

- **TTL is mandatory.** Every `put` call must specify a TTL. Default maximum: 1 hour. Domain-specific overrides documented per service.
- **Eviction policy:** LRU (least recently used) as default. Document if a different policy is required.
- **Consistency model:** cache-aside pattern by default. The service reads from cache first; on miss, reads from the authoritative store and populates cache. Never treat cache as the source of truth.
- **Serialization:** JSON for most payloads. Binary for large objects or performance-critical paths. Serialization format must be documented per cache usage.
- **Key naming convention:** `<service>:<entity>:<id>` (e.g., `order-service:order:12345`). This prevents collisions in shared cache clusters.

## Error Handling

- Cache unavailability must not break the service. On any cache error, log a WARNING, emit a metric, and fall through to the authoritative data source.
- Never throw an exception to the caller on cache failure.
- Emit `<service>_cache_errors_total{operation="get|put|evict"}` on errors.

## Observability

- Metrics: `<service>_cache_hits_total`, `<service>_cache_misses_total`, `<service>_cache_put_total`, `<service>_cache_evict_total`, `<service>_cache_errors_total`, `<service>_cache_latency_seconds`.
- Log cache misses at DEBUG level, errors at WARNING level.
- Create spans for cache operations in performance-critical paths.

## Production vs Local Differences

- **Production:** Redis, Memcached, or managed cache service. Clustered, replicated, with connection pooling.
- **Local / fallback (`FALLBACK_CACHE=inmemory`):** in-memory `ConcurrentHashMap` (Java) or `dict` with TTL wrapper (Python). Single-instance only. No persistence. Acceptable for development.
- Fallback must never be active in production. Enforce via startup validation.

## Java Example

```java
public interface CacheProvider {
    <T> Optional<T> get(String key, Class<T> type);
    void put(String key, Object value, Duration ttl);
    boolean putIfAbsent(String key, Object value, Duration ttl);
    void evict(String key);
    void evictByPrefix(String prefix);
}

@Component
@Profile("!fallback-cache")
public class RedisCacheProvider implements CacheProvider {
    // Redis implementation with connection pool, serialization, error handling
}

@Component
@Profile("fallback-cache")
public class InMemoryCacheProvider implements CacheProvider {
    // ConcurrentHashMap with scheduled TTL eviction
}
```

## Python Example

```python
class CacheProvider(Protocol):
    def get(self, key: str) -> Any | None: ...
    def put(self, key: str, value: Any, ttl: timedelta) -> None: ...
    def put_if_absent(self, key: str, value: Any, ttl: timedelta) -> bool: ...
    def evict(self, key: str) -> None: ...
    def evict_by_prefix(self, prefix: str) -> None: ...
```

## Anti-Patterns

- **No-TTL entries:** every cached value must expire. Permanent entries lead to stale data and memory leaks.
- **Cache as source of truth:** cache-aside only. If the cache is lost, the service must still function.
- **Catch-all keys:** avoid caching entire collections. Cache individual entities by ID.
- **Silent failures with no metrics:** always emit error metrics even when gracefully falling through.

## LLM Instructions

- When adding caching to a service, use the `CacheProvider` interface, not a direct Redis client.
- Always include a TTL on every `put` call.
- Implement the cache-aside pattern: check cache → on miss, load from DB → populate cache → return.
- Wire fallback via Spring profile or Python dependency injection.
- Ask the user for TTL requirements before choosing defaults.

## Review Checklist

- [ ] All `put` calls include an explicit TTL.
- [ ] Key naming follows `<service>:<entity>:<id>` convention.
- [ ] Cache errors are caught and do not propagate to callers.
- [ ] Hit/miss/error metrics emitted.
- [ ] Fallback implementation exists for local development.
- [ ] Fallback cannot activate in production.
