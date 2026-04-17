# Redis Integration (Java Spring Boot)

## Purpose

Step-by-step guide for wiring Redis into a Spring Boot service through the `CacheProvider` capability interface, covering connection configuration, serialization, TTL management, observability, and fallback setup.

## Dependencies

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-pool2</artifactId>
</dependency>
```

## Connection Configuration

```yaml
# application.yml
spring:
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: ${REDIS_PORT:6379}
      password: ${REDIS_PASSWORD:}
      ssl:
        enabled: ${REDIS_SSL:true}
      timeout: 2000ms
      lettuce:
        pool:
          max-active: 16
          max-idle: 8
          min-idle: 2
          max-wait: 1000ms
        shutdown-timeout: 200ms
```

## CacheProvider Implementation

```java
@Component
@Profile("!fallback-cache")
public class RedisCacheProvider implements CacheProvider {
    private final StringRedisTemplate redisTemplate;
    private final ObjectMapper objectMapper;
    private final MeterRegistry meterRegistry;

    @Override
    public <T> Optional<T> get(String key, Class<T> type) {
        Timer.Sample sample = Timer.start(meterRegistry);
        try {
            String value = redisTemplate.opsForValue().get(key);
            if (value == null) {
                meterRegistry.counter("cache_misses_total").increment();
                return Optional.empty();
            }
            meterRegistry.counter("cache_hits_total").increment();
            return Optional.of(objectMapper.readValue(value, type));
        } catch (Exception e) {
            meterRegistry.counter("cache_errors_total").increment();
            log.warn("Cache get failed for key={}, falling back to miss", key, e);
            return Optional.empty();
        } finally {
            sample.stop(meterRegistry.timer("cache_operation_duration", "op", "get"));
        }
    }

    @Override
    public <T> void put(String key, T value, Duration ttl) {
        try {
            String serialized = objectMapper.writeValueAsString(value);
            redisTemplate.opsForValue().set(key, serialized, ttl);
            meterRegistry.counter("cache_puts_total").increment();
        } catch (Exception e) {
            meterRegistry.counter("cache_errors_total").increment();
            log.warn("Cache put failed for key={}", key, e);
            // fail open — cache miss on next read is acceptable
        }
    }

    @Override
    public void evict(String key) {
        redisTemplate.delete(key);
    }

    @Override
    public void evictByPrefix(String prefix) {
        Set<String> keys = redisTemplate.keys(prefix + "*");
        if (keys != null && !keys.isEmpty()) {
            redisTemplate.delete(keys);
        }
    }
}
```

## Key Naming Convention

```
{service}:{entity}:{id}
```

| Pattern | Example | TTL |
|---------|---------|-----|
| Entity cache | `order-svc:order:abc-123` | 5 min |
| List/query cache | `order-svc:orders:status=OPEN` | 1 min |
| Session | `order-svc:session:user-xyz` | 30 min |
| Rate limit | `order-svc:ratelimit:user-xyz` | 60 s |

## Serialization

Use JSON serialization for cross-language compatibility:

```java
@Bean
public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory factory) {
    RedisTemplate<String, Object> template = new RedisTemplate<>();
    template.setConnectionFactory(factory);
    template.setKeySerializer(new StringRedisSerializer());
    template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
    return template;
}
```

**Avoid** Java native serialization (`JdkSerializationRedisSerializer`) — it produces opaque blobs, breaks cross-language reads, and creates security risks from deserialization.

## Fallback Wiring

```java
@Component
@Profile("fallback-cache")
public class InMemoryCacheProvider implements CacheProvider {
    // See core/fallbacks/redis-fallback.md for implementation
}
```

Activate via:
```properties
FALLBACK_CACHE=inmemory
```

## Observability

| Metric | Description |
|--------|-------------|
| `cache_hits_total` | Successful cache reads |
| `cache_misses_total` | Cache read misses |
| `cache_puts_total` | Cache writes |
| `cache_errors_total` | Redis operation failures |
| `cache_operation_duration` | Latency histogram by operation type |

Spring Boot auto-exposes Lettuce metrics via Micrometer when `spring-boot-starter-data-redis` is on the classpath.

## Health Check

```java
// Auto-configured by Spring Boot Actuator
// GET /actuator/health → includes redis health indicator
```

Ensure `management.health.redis.enabled=true` (default).

## Testing

```java
@SpringBootTest
@Testcontainers
class RedisCacheProviderTest {
    @Container
    static GenericContainer<?> redis = new GenericContainer<>("redis:7-alpine")
        .withExposedPorts(6379);

    @DynamicPropertySource
    static void redisProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.data.redis.host", redis::getHost);
        registry.add("spring.data.redis.port", () -> redis.getMappedPort(6379));
    }

    @Autowired CacheProvider cacheProvider;

    @Test
    void should_put_and_get_cached_value() {
        cacheProvider.put("test:key", new Order("123"), Duration.ofMinutes(5));
        Optional<Order> result = cacheProvider.get("test:key", Order.class);
        assertThat(result).isPresent().hasValueSatisfying(o -> 
            assertThat(o.getId()).isEqualTo("123"));
    }
}
```

## References

- [CacheProvider.md](../../../core/abstractions/CacheProvider.md)
- [redis-fallback.md](../../../core/fallbacks/redis-fallback.md)
- [config-model.md](../../../core/config/config-model.md)
