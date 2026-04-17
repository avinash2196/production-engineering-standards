# Python FastAPI Stack

Opinionated starter templates and integration guides for Python 3.12+ FastAPI services.

## Stack Requirements

| Component | Version |
|-----------|---------|
| Python | 3.12+ |
| FastAPI | 0.110+ |
| Package manager | `pip` + `requirements.txt` (Poetry acceptable) |
| Container base | `python:3.12-slim` |
| Async runtime | `uvicorn` with `uvloop` |

## Project Structure

```
src/{service_name}/
├── api/                 # FastAPI routers — thin, delegates to service
├── service/             # Business logic — orchestrates domain + infra
├── domain/              # Pydantic models, value objects, domain events
├── repository/          # Data access (SQLAlchemy, asyncpg)
├── infrastructure/      # Capability interface implementations
│   ├── messaging/       # KafkaMessagePublisher, InMemoryMessagePublisher
│   ├── cache/           # RedisCacheProvider, InMemoryCacheProvider
│   ├── storage/         # S3ObjectStorageProvider, LocalFileStorageProvider
│   ├── config/          # Config provider wiring
│   └── secrets/         # VaultSecretProvider, EnvSecretProvider
├── config/              # Settings (pydantic-settings), env files
└── main.py              # FastAPI app with lifespan
```

See [python-backend.md](python-backend.md) for full architecture, abstractions, and coding conventions.

## Guides

| Guide | Description |
|-------|-------------|
| [Kafka Integration](integration-guides/kafka-integration.md) | Async producer/consumer with `MessagePublisher` / `MessageSubscriber` |
| [Redis Integration](integration-guides/redis-integration.md) | Caching with `CacheProvider` via `redis.asyncio` |
| [Storage Integration](integration-guides/storage-integration.md) | Object storage with `ObjectStorageProvider` via `aiobotocore` |

## Quick Start

```bash
# Clone the template
cp -r project-templates/python-fastapi my-new-service
cd my-new-service

# Setup
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run locally with fallbacks (no infra needed)
FALLBACK_KAFKA=true FALLBACK_CACHE=inmemory FALLBACK_STORAGE=local \
  uvicorn src.my_service.main:app --reload --port 8000
```

## Capability Interface Mapping

| Abstraction | Production Implementation | Fallback Implementation |
|-------------|--------------------------|-------------------------|
| `MessagePublisher` | `KafkaMessagePublisher` (aiokafka) | `InMemoryMessagePublisher` |
| `MessageSubscriber` | `KafkaMessageSubscriber` (aiokafka) | `InMemoryMessageSubscriber` |
| `CacheProvider` | `RedisCacheProvider` (redis.asyncio) | `InMemoryCacheProvider` |
| `ObjectStorageProvider` | `S3ObjectStorageProvider` (aiobotocore) | `LocalFileStorageProvider` |
| `SecretProvider` | `VaultSecretProvider` (hvac) | `EnvSecretProvider` |
| `ConfigProvider` | `CompositeConfigProvider` | same (env + file fallback) |

Fallback activation is controlled via environment variables and dependency injection.

## Key Conventions

- **Async first:** All I/O operations use `async`/`await`.
- **Pydantic everywhere:** Request/response DTOs, config, domain models.
- **Dependency injection:** Use FastAPI `Depends()` for capability interfaces.
- **No global state:** All dependencies flow through the DI container.

## References

- [python-backend.md](python-backend.md) — Full stack conventions
- [Core abstractions](../../core/abstractions/)
- [Fallback strategy](../../standards/fallback-strategy.md)
- [Observability standard](../../standards/observability.md)
