# Python Microservice Example

Minimal example demonstrating `core` abstractions and fallbacks in a Python FastAPI service.

## Overview

A simple order-service that implements the standard layered architecture with all capability interfaces wired (production + fallback). Use this as a reference for how a real Python service consumes the enterprise standards.

## Structure

```
python-microservice/
├── src/order_service/
│   ├── api/
│   │   ├── orders.py                   # FastAPI router
│   │   └── dto.py                      # Request/response models
│   ├── service/
│   │   └── order_service.py            # Business logic
│   ├── domain/
│   │   ├── order.py                    # Domain model
│   │   └── order_status.py             # Enum
│   ├── repository/
│   │   └── order_repository.py         # Data access
│   ├── infrastructure/
│   │   ├── messaging/                  # KafkaMessagePublisher
│   │   ├── cache/                      # RedisCacheProvider
│   │   ├── storage/                    # S3ObjectStorageProvider
│   │   └── fallback/                   # All in-memory fallbacks
│   ├── config/
│   │   └── settings.py                 # Pydantic settings
│   └── main.py                         # FastAPI app with lifespan
├── tests/
│   ├── unit/                           # pytest with mocks
│   └── integration/                    # testcontainers-python
├── Dockerfile
├── docker-compose.dev.yml
├── requirements.txt
└── .env.local
```

## Running

```bash
cd examples/python-microservice
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# With fallbacks (zero infra)
FALLBACK_KAFKA=true FALLBACK_CACHE=inmemory FALLBACK_STORAGE=local FALLBACK_SECRETS=env \
  uvicorn src.order_service.main:app --reload --port 8000

# With real infra
docker compose -f docker-compose.dev.yml up -d
uvicorn src.order_service.main:app --reload --port 8000
```

## Key Patterns Demonstrated

| Pattern | Where |
|---------|-------|
| Layered architecture | `api/ → service/ → domain/ → repository/` |
| Capability interface usage | Service receives `MessagePublisher`, `CacheProvider` via `Depends()` |
| Fallback activation | `get_publisher()` checks `settings.fallback_kafka` |
| DTO separation | Pydantic models in `api/dto.py` |
| Structured logging | JSON format with traceId via `structlog` |
| Health checks | `/health` endpoint with readiness probes |
| Async I/O | All infrastructure calls use `async`/`await` |
| Unit testing | `pytest` + `AsyncMock` for capability interfaces |
| Integration testing | `testcontainers-python` for real infra |

## References

- [Python FastAPI stack](../../stacks/python-fastapi/README.md)
- [Core architecture](../../core/architecture.md)
- [Core abstractions](../../core/abstractions/)
