# Cache Integration — Java Spring Boot

## Purpose

Implement Redis behind `CacheProvider`, with an explicit JSON-file or in-memory local adapter when approved. A local cache must not be used to validate Redis coordination, distributed locks, rate limits, or correctness-sensitive atomic behavior.

## Delivery Sequence

1. Plan source of truth, key namespace, TTL, invalidation, stale-data tolerance, and failure behavior.
2. Approve exact configuration, adapters, and tests.
3. Add failing tests for TTL, invalidation, selection, malformed local state, and production guards.
4. Implement the minimum cache behavior.
5. Run unit and Redis integration tests.
6. Refactor after green.

## Configuration and Composition

```yaml
adapters:
  cache: ${CACHE_ADAPTER:redis}
```

```java
@Bean
@ConditionalOnProperty(name = "adapters.cache", havingValue = "redis")
CacheProvider redisCache(RedisTemplate<String, byte[]> template) {
    return new RedisCacheProvider(template);
}

@Bean
@ConditionalOnProperty(name = "adapters.cache", havingValue = "jsonfile")
CacheProvider jsonFileCache(LocalCacheProperties properties) {
    return new JsonFileCacheProvider(properties.path());
}
```

Production accepts `redis`; it rejects `jsonfile` and `inmemory`.

## Policy Requirements

- Define command/connection timeouts.
- Use namespaced keys and deliberate TTLs.
- Avoid unbounded key scans on request paths.
- Bypass the cache only when correctness is preserved and the system of record can absorb load.
- Fail safely when cache state controls authorization, locks, idempotency, or rate limiting.

## Verification

- unit tests for application cache policy;
- shared contract tests where practical;
- Testcontainers Redis tests for TTL/serialization/atomic operations;
- JSON-file tests for restart persistence and malformed data;
- selection and production-guard tests;
- metrics/log assertions on errors and local activation where useful.

## References

- [CacheProvider](../../../contracts/CacheProvider.md)
- [Cache local adapters](../../../standards/fallbacks/redis-fallback.md)
- [Production dependency failure strategy](../../../standards/fallback-strategy.md)
