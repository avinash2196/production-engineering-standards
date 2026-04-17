---
applyTo: "**/*.py"
description: "Use when writing, reviewing, or generating Python code. Enforces FastAPI layered architecture, Pydantic v2 DTOs, async patterns, dependency injection for capability interfaces, and testing with pytest-asyncio."
---

Follow all rules in [stacks/python-fastapi/python-backend.md](../../stacks/python-fastapi/python-backend.md) and [standards/coding-standards.md](../../standards/coding-standards.md).

## Layer Rules

- **API (`api/`)**: FastAPI `APIRouter`. Accept/return Pydantic models. Call service only. No business logic.
- **Service (`service/`)**: Receives capability interfaces via `Depends()`. No direct `aiokafka`, `redis.asyncio`, or `aiobotocore` imports.
- **Domain (`domain/`)**: Plain Python dataclasses or Pydantic `BaseModel` subclasses. Zero framework imports (`fastapi`, `sqlalchemy`, etc. are forbidden).
- **Repository (`repository/`)**: SQLAlchemy async sessions. One class per aggregate root. Accept `AsyncSession` via `Depends()`.
- **Infrastructure (`infrastructure/`)**: Capability implementations. Fallback selection in `infrastructure/fallback/providers.py` using settings flags.

## Naming

| Element | Convention | Example |
|---------|-----------| -------|
| Module | `snake_case` | `order_service.py` |
| Class | `PascalCase` + role suffix | `OrderService`, `OrderRepository` |
| Function | `snake_case`, verb-first | `find_order_by_id`, `publish_order_created` |
| DTO | `{Entity}Request` / `{Entity}Response` | `CreateOrderRequest` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |

## Hard Rules

- All route handlers and service methods must be `async def`.
- DTOs use `pydantic.BaseModel` (v2) with `model_config = ConfigDict(frozen=True)` for responses.
- Request DTOs use `@field_validator` or `Annotated` validators — never validate in the service layer.
- All secrets via `SecretProvider.get(key)` — never `os.environ["SECRET"]` in business logic.
- Raise domain exceptions (`OrderNotFoundError(Exception)`), not generic `Exception`.
- All errors caught and returned as `{"code": ..., "message": ..., "traceId": ...}` via exception handlers.
- Functions: **max 30 lines**. Classes: **max 300 lines**.
- Type annotations are **required** on all function signatures. `mypy --strict` must pass.

## Dependency Injection Pattern

```python
# Correct: inject via Depends()
@router.post("/orders")
async def create_order(
    body: CreateOrderRequest,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    ...

# Wrong: instantiate in handler
@router.post("/orders")
async def create_order(body: CreateOrderRequest) -> OrderResponse:
    service = OrderService(KafkaPublisher())  # ← Never do this
    ...
```

## Observability

- Use `structlog.get_logger(__name__)` — never `print()` or `logging.basicConfig()`.
- Bind trace context: `log.bind(order_id=str(order_id), trace_id=...)`.
- Prometheus metrics via `prometheus_fastapi_instrumentator` (auto-wired in `main.py`).

## Testing

- Use `pytest` + `pytest-asyncio` with `asyncio_mode = "auto"`.
- Unit tests: mock capability interfaces with `AsyncMock`. No database or network.
- Integration tests: `testcontainers-python` for real Postgres/Redis/Kafka.
- See [standards/testing/unit-testing.md](../../standards/testing/unit-testing.md).
