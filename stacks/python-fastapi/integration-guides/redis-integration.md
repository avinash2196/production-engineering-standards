# Redis Integration (Python FastAPI)

## Purpose

Step-by-step guide for wiring Redis into a FastAPI service through the `CacheProvider` capability interface using `redis.asyncio`, covering connection configuration, serialization, TTL management, observability, and fallback setup.

## Dependencies

```txt
# requirements.txt
redis[hiredis]>=5.0.0
pydantic>=2.0
prometheus-client>=0.20.0
```

## Configuration

```python
# config/redis.py
from pydantic_settings import BaseSettings

class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    password: str = ""
    ssl: bool = True
    db: int = 0
    socket_timeout: float = 2.0
    max_connections: int = 20

    class Config:
        env_prefix = "REDIS_"
```

## CacheProvider Implementation

```python
# infrastructure/cache/redis_cache_provider.py
import json
import time
from typing import Optional, Type, TypeVar
from redis.asyncio import Redis
from core.abstractions import CacheProvider

T = TypeVar("T")

class RedisCacheProvider(CacheProvider):
    def __init__(self, redis: Redis, metrics: MetricsCollector):
        self._redis = redis
        self._metrics = metrics

    async def get(self, key: str, type_: Type[T]) -> Optional[T]:
        start = time.monotonic()
        try:
            value = await self._redis.get(key)
            if value is None:
                self._metrics.increment("cache_misses_total")
                return None
            self._metrics.increment("cache_hits_total")
            return type_.model_validate_json(value) if hasattr(type_, "model_validate_json") \
                else json.loads(value)
        except Exception as e:
            self._metrics.increment("cache_errors_total")
            logger.warning("Cache get failed: key=%s, error=%s", key, e)
            return None
        finally:
            elapsed = time.monotonic() - start
            self._metrics.observe("cache_operation_duration_seconds", elapsed, tags={"op": "get"})

    async def put(self, key: str, value: object, ttl_seconds: int) -> None:
        try:
            serialized = value.model_dump_json() if hasattr(value, "model_dump_json") \
                else json.dumps(value)
            await self._redis.setex(key, ttl_seconds, serialized)
            self._metrics.increment("cache_puts_total")
        except Exception as e:
            self._metrics.increment("cache_errors_total")
            logger.warning("Cache put failed: key=%s, error=%s", key, e)

    async def evict(self, key: str) -> None:
        await self._redis.delete(key)

    async def evict_by_prefix(self, prefix: str) -> None:
        cursor = 0
        while True:
            cursor, keys = await self._redis.scan(cursor, match=f"{prefix}*", count=100)
            if keys:
                await self._redis.delete(*keys)
            if cursor == 0:
                break
```

## FastAPI Dependency Wiring

```python
# dependencies.py
from redis.asyncio import Redis

_redis_pool: Redis | None = None

async def get_redis(settings: RedisSettings) -> Redis:
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = Redis(
            host=settings.host,
            port=settings.port,
            password=settings.password,
            ssl=settings.ssl,
            db=settings.db,
            socket_timeout=settings.socket_timeout,
            max_connections=settings.max_connections,
            decode_responses=True,
        )
    return _redis_pool

def get_cache_provider(settings: Settings = Depends(get_settings)) -> CacheProvider:
    if settings.fallback_cache == "inmemory":
        return InMemoryCacheProvider()
    redis = get_redis(settings.redis)
    return RedisCacheProvider(redis, get_metrics())
```

## Key Naming Convention

```
{service}:{entity}:{id}
```

| Pattern | Example | TTL |
|---------|---------|-----|
| Entity cache | `order-svc:order:abc-123` | 300s |
| List/query cache | `order-svc:orders:status=OPEN` | 60s |
| Session | `order-svc:session:user-xyz` | 1800s |
| Rate limit | `order-svc:ratelimit:user-xyz` | 60s |

## Fallback Wiring

```python
# infrastructure/cache/inmemory_cache_provider.py
import threading
import time
from core.abstractions import CacheProvider

class InMemoryCacheProvider(CacheProvider):
    """See standards/fallbacks/redis-fallback.md for full implementation."""
    def __init__(self):
        self._store: dict[str, tuple[object, float]] = {}
        self._lock = threading.Lock()

    async def get(self, key, type_=None):
        with self._lock:
            entry = self._store.get(key)
            if entry is None or entry[1] < time.time():
                self._store.pop(key, None)
                return None
            return entry[0]

    async def put(self, key, value, ttl_seconds=300):
        with self._lock:
            self._store[key] = (value, time.time() + ttl_seconds)
```

Activate via:
```bash
export FALLBACK_CACHE=inmemory
```

## Observability

| Metric | Description |
|--------|-------------|
| `cache_hits_total` | Successful cache reads |
| `cache_misses_total` | Cache read misses |
| `cache_puts_total` | Cache writes |
| `cache_errors_total` | Redis operation failures |
| `cache_operation_duration_seconds` | Latency histogram by op |

## Testing

```python
import pytest
from testcontainers.redis import RedisContainer

@pytest.fixture(scope="module")
def redis_container():
    with RedisContainer() as redis:
        yield redis

@pytest.mark.asyncio
async def test_put_and_get(redis_container):
    from redis.asyncio import Redis
    redis = Redis(host=redis_container.get_container_host_ip(),
                  port=redis_container.get_exposed_port(6379))
    provider = RedisCacheProvider(redis, mock_metrics())
    await provider.put("test:key", {"id": "123"}, ttl_seconds=60)
    result = await provider.get("test:key", dict)
    assert result == {"id": "123"}
```

## References

- [CacheProvider.md](../../../contracts/CacheProvider.md)
- [redis-fallback.md](../../../standards/fallbacks/redis-fallback.md)
- [config-model.md](../../../standards/config/config-model.md)
