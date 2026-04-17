# Fallback Demo

Demonstrates toggling fallbacks: Kafka → in-memory queue, Redis → in-memory cache, Storage → local disk.

## Overview

This example service shows how fallback implementations activate when infrastructure is unavailable. It exposes simple endpoints that exercise each capability interface, letting you observe the difference between production and fallback behavior.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/messages` | Publishes a message via `MessagePublisher` |
| GET | `/api/cache/{key}` | Reads from `CacheProvider` |
| PUT | `/api/cache/{key}` | Writes to `CacheProvider` with TTL |
| POST | `/api/files/upload` | Uploads a file via `ObjectStorageProvider` |
| GET | `/api/files/{key}` | Downloads a file via `ObjectStorageProvider` |
| GET | `/api/secrets/{key}` | Reads a secret via `SecretProvider` |
| GET | `/actuator/health` | Health check |

## Running

### With All Fallbacks (Zero Infra)

```bash
cd examples/fallback-demo

# Java
FALLBACK_KAFKA=true FALLBACK_CACHE=inmemory FALLBACK_STORAGE=local FALLBACK_SECRETS=env \
  ./mvnw spring-boot:run

# Python
FALLBACK_KAFKA=true FALLBACK_CACHE=inmemory FALLBACK_STORAGE=local FALLBACK_SECRETS=env \
  uvicorn src.fallback_demo.main:app --port 8080
```

### With Real Infrastructure

```bash
# Start infra
docker compose -f docker-compose.dev.yml up -d

# Run service (no fallback toggles)
./mvnw spring-boot:run
```

## Testing the Fallbacks

```bash
# Publish a message (goes to in-memory queue)
curl -X POST http://localhost:8080/api/messages \
  -H 'Content-Type: application/json' \
  -d '{"topic": "orders", "body": {"id": "123"}}'

# Write to cache (in-memory HashMap)
curl -X PUT http://localhost:8080/api/cache/test-key \
  -H 'Content-Type: application/json' \
  -d '{"value": "hello", "ttlSeconds": 60}'

# Read from cache
curl http://localhost:8080/api/cache/test-key

# Upload a file (to ./data/fallback-storage/)
curl -X POST http://localhost:8080/api/files/upload \
  -F 'file=@README.md' -F 'key=demo/readme.md'

# Check health
curl http://localhost:8080/actuator/health
```

## What to Observe

| Scenario | Behavior |
|----------|----------|
| Message publish with fallback | Returns 200, message stored in-memory (lost on restart) |
| Cache read with fallback | Returns data from in-memory HashMap with TTL expiry |
| File upload with fallback | File appears in `./data/fallback-storage/demo/readme.md` |
| Secret read with fallback | Reads from environment variables |
| Health check | Returns `UP` regardless of fallback mode |

## References

- [Run with fallbacks workflow](../../workflows/local-dev/run-with-fallbacks.md)
- [Fallback strategy](../../standards/fallback-strategy.md)
- [Core fallbacks](../../core/fallbacks/)
