# Run With Fallbacks

How to enable and test fallbacks locally so you can develop and run services without any external infrastructure.

## Overview

Every capability interface (`MessagePublisher`, `CacheProvider`, `ObjectStorageProvider`, `SecretProvider`) has a fallback implementation that runs entirely in-process. This lets you:

- Start a service with zero Docker containers.
- Run the full test suite offline.
- Develop on a plane, train, or restricted network.

## Environment Variables

| Variable | Value | Effect |
|----------|-------|--------|
| `FALLBACK_KAFKA` | `true` | Replaces Kafka with in-memory queue |
| `FALLBACK_CACHE` | `inmemory` | Replaces Redis with `ConcurrentHashMap` / `dict` |
| `FALLBACK_STORAGE` | `local` | Replaces S3/Blob with local filesystem (`./data/fallback-storage/`) |
| `FALLBACK_SECRETS` | `env` | Replaces Vault with environment variable lookup |

## Quick Start

### Java Spring Boot

```bash
# Option 1: Environment variables
FALLBACK_KAFKA=true \
FALLBACK_CACHE=inmemory \
FALLBACK_STORAGE=local \
FALLBACK_SECRETS=env \
  ./mvnw spring-boot:run -Dspring-boot.run.profiles=local

# Option 2: Use .env.local (loaded by Spring Boot DevTools)
cp .env.local.example .env.local
./mvnw spring-boot:run -Dspring-boot.run.profiles=local
```

### Python FastAPI

```bash
# Option 1: Environment variables
FALLBACK_KAFKA=true \
FALLBACK_CACHE=inmemory \
FALLBACK_STORAGE=local \
FALLBACK_SECRETS=env \
  uvicorn src.my_service.main:app --reload --port 8000

# Option 2: Use .env.local
cp .env.local.example .env.local
uvicorn src.my_service.main:app --reload --port 8000
```

## `.env.local.example`

```env
# Fallback toggles — set all to enable full local mode
FALLBACK_KAFKA=true
FALLBACK_CACHE=inmemory
FALLBACK_STORAGE=local
FALLBACK_SECRETS=env

# Application config
APP_ENV=local
LOG_LEVEL=DEBUG
SERVER_PORT=8080

# Local secrets (only used when FALLBACK_SECRETS=env)
DB_PASSWORD=local-dev-password
API_KEY=local-dev-key
```

## How Fallback Activation Works

### Java (Spring Profiles)

```java
@Component
@Profile("!fallback-kafka")          // Active when Kafka is available
public class KafkaMessagePublisher implements MessagePublisher { ... }

@Component
@Profile("fallback-kafka")           // Active when FALLBACK_KAFKA=true
public class InMemoryMessagePublisher implements MessagePublisher { ... }
```

Spring Boot reads `FALLBACK_KAFKA=true` and activates the `fallback-kafka` profile automatically.

### Python (Dependency Injection)

```python
def get_publisher(settings: Settings = Depends(get_settings)) -> MessagePublisher:
    if settings.fallback_kafka:
        return InMemoryMessagePublisher()
    return KafkaMessagePublisher(settings.kafka, get_metrics())
```

## Limitations

| Fallback | What works | What doesn't |
|----------|-----------|---------------|
| In-memory queue | Publish/subscribe within one process | Multi-instance, persistence across restarts |
| In-memory cache | Get/put/evict with TTL | Shared cache across instances, pub/sub |
| Local filesystem | Upload/download/delete | Presigned URLs (returns `file://`), multi-instance |
| Env secrets | Read secrets by key | Rotation, dynamic refresh, access audit |

See individual fallback docs for full details:
- [kafka-fallback.md](../../core/fallbacks/kafka-fallback.md)
- [redis-fallback.md](../../core/fallbacks/redis-fallback.md)
- [storage-fallback.md](../../core/fallbacks/storage-fallback.md)
- [secret-fallback.md](../../core/fallbacks/secret-fallback.md)

## Testing With Fallbacks

```bash
# Run full test suite with fallbacks (no infra needed)
FALLBACK_KAFKA=true FALLBACK_CACHE=inmemory FALLBACK_STORAGE=local FALLBACK_SECRETS=env \
  ./mvnw test

# Run integration tests with real infra (Testcontainers)
./mvnw test -Dgroups=integration
```

## Verifying Fallback Behavior

1. Start the service with all fallbacks enabled.
2. Hit `GET /actuator/health` (Java) or `GET /health` (Python) — should return `UP`.
3. Publish a message via a POST endpoint — should succeed (queued in-memory).
4. Read from cache — should return a miss (empty in-memory store).
5. Upload a file — should appear in `./data/fallback-storage/`.

## References

- [Fallback strategy](../../standards/fallback-strategy.md)
- [Start local stack](start-local-stack.md) — for running with real infra locally
