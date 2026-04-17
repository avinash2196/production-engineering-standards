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
| `FALLBACK_KAFKA` | `db` | Replaces Kafka with DB outbox table (`outbox_message`). Set `inmemory` for pure in-process queue (no persistence). |
| `FALLBACK_CACHE` | `jsonfile` | Replaces Redis with JSON file cache (`./data/fallback-cache/cache.json`). Set `inmemory` for in-process map (no persistence). |
| `FALLBACK_STORAGE` | `local` | Replaces S3/Blob with local filesystem (`./data/fallback-storage/`) |
| `FALLBACK_SECRETS` | `env` | Replaces Vault with environment variable lookup |

## Quick Start

### Java Spring Boot

```bash
# Option 1: Environment variables
FALLBACK_KAFKA=db \
FALLBACK_CACHE=jsonfile \
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
FALLBACK_KAFKA=db \
FALLBACK_CACHE=jsonfile \
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
FALLBACK_KAFKA=db
FALLBACK_CACHE=jsonfile
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

### Java (ConditionalOnProperty)

```java
@Component
@ConditionalOnMissingBean(condition = FallbackKafkaDbCondition.class)  // Active when Kafka is available
public class KafkaMessagePublisher implements MessagePublisher { ... }

@Component
@ConditionalOnProperty(name = "fallback.kafka", havingValue = "db")   // Active when FALLBACK_KAFKA=db
public class DbTableMessagePublisher implements MessagePublisher { ... }

@Component
@ConditionalOnProperty(name = "fallback.kafka", havingValue = "inmemory")  // Secondary: FALLBACK_KAFKA=inmemory
public class InMemoryMessagePublisher implements MessagePublisher { ... }
```

Spring Boot maps `FALLBACK_KAFKA=db` → `fallback.kafka=db` via relaxed binding. Use `@ConditionalOnProperty` rather than Spring profiles for named-value fallback selection.

### Python (Dependency Injection)

```python
def get_publisher(settings: Settings = Depends(get_settings)) -> MessagePublisher:
    if settings.fallback_kafka == "db":
        return DbTableMessagePublisher(settings.db, get_metrics())
    if settings.fallback_kafka == "inmemory":
        return InMemoryMessagePublisher()
    return KafkaMessagePublisher(settings.kafka, get_metrics())
```

## Limitations

| Fallback | What works | What doesn't |
|----------|-----------|---------------|
| DB table queue (`FALLBACK_KAFKA=db`) | Publish/subscribe, persistence across restarts, inspectable rows, retry on FAILED | Multi-instance fan-out, ordered global delivery |
| In-memory queue (`FALLBACK_KAFKA=inmemory`) | Publish/subscribe within one process | Multi-instance, persistence across restarts |
| JSON file cache (`FALLBACK_CACHE=jsonfile`) | Get/put/evict with TTL, persists across restarts, human-readable | Shared cache across instances, pub/sub, concurrent multi-process writes |
| In-memory cache (`FALLBACK_CACHE=inmemory`) | Get/put/evict with TTL within one process | Shared cache across instances, persistence across restarts |
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
FALLBACK_KAFKA=db FALLBACK_CACHE=jsonfile FALLBACK_STORAGE=local FALLBACK_SECRETS=env \
  ./mvnw test

# Run integration tests with real infra (Testcontainers)
./mvnw test -Dgroups=integration
```

## Verifying Fallback Behavior

1. Start the service with all fallbacks enabled.
2. Hit `GET /actuator/health` (Java) or `GET /health` (Python) — should return `UP`.
3. Publish a message via a POST endpoint — should succeed (row inserted into `outbox_message` table).
4. Read from cache — should return a miss (empty JSON file cache at `./data/fallback-cache/cache.json`).
5. Upload a file — should appear in `./data/fallback-storage/`.

## References

- [Fallback strategy](../../standards/fallback-strategy.md)
- [Start local stack](start-local-stack.md) — for running with real infra locally
