# DTO Guidelines

Rules for request/response DTOs, validation, and mapping to domain objects.

## Purpose

Standardize how data crosses service boundaries (HTTP, messaging) to ensure consistent validation, versioning, and separation from domain models.

## Mandatory Rules

### Separation

- **DTOs and domain objects are separate classes.** Never expose JPA entities or SQLAlchemy models directly as API responses.
- Request DTOs live in the controller/API layer.
- Domain objects live in the domain layer.
- Mapping happens in the service layer or a dedicated mapper.

### Request DTOs

```java
// Java: immutable record with validation
public record CreateOrderRequest(
    @NotBlank String customerId,
    @NotNull @Size(min = 1) List<OrderItemRequest> items,
    @Email String notificationEmail
) {}
```

```python
# Python: Pydantic model with validation
class CreateOrderRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    items: list[OrderItemRequest] = Field(..., min_length=1)
    notification_email: EmailStr
```

**Rules:**
- All fields validated at the boundary — no invalid data reaches the service layer.
- Use framework validation annotations (`@NotBlank`, `@Size`, Pydantic `Field`).
- Immutable — records (Java) or frozen Pydantic models (Python).
- No business logic in DTOs.

### Response DTOs

```java
public record OrderResponse(
    String id,
    String status,
    BigDecimal totalAmount,
    Instant createdAt
) {
    public static OrderResponse from(Order order) {
        return new OrderResponse(order.getId(), order.getStatus().name(),
            order.getTotalAmount(), order.getCreatedAt());
    }
}
```

```python
class OrderResponse(BaseModel):
    id: str
    status: str
    total_amount: Decimal
    created_at: datetime

    @classmethod
    def from_domain(cls, order: Order) -> "OrderResponse":
        return cls(id=order.id, status=order.status.value,
                   total_amount=order.total_amount, created_at=order.created_at)
```

**Rules:**
- Include only fields the consumer needs — no internal IDs, audit columns, or secrets.
- Use explicit mapping methods (`from()` / `from_domain()`).
- Dates as ISO 8601 strings or `Instant` / `datetime` (serialized to ISO 8601).
- Money as `BigDecimal` / `Decimal` — never `float`.

### Error Response DTOs

All errors return a consistent envelope:

```json
{
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "Order with ID abc-123 not found",
    "traceId": "4bf92f3577b34da6",
    "timestamp": "2026-04-16T10:30:00Z"
  }
}
```

**Rules:**
- `code`: machine-readable, UPPER_SNAKE_CASE.
- `message`: human-readable, no stack traces or internal details.
- `traceId`: from the distributed tracing context.
- Never expose exception class names, SQL errors, or file paths in error responses.

### Pagination

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 142,
    "totalPages": 8
  }
}
```

Default page size: 20. Maximum page size: 100.

## Defaults

- Use `record` types (Java 17+) or Pydantic `BaseModel` (Python) for all DTOs.
- Date/time serialization: ISO 8601 with UTC timezone.
- Enum serialization: string value (not ordinal).
- JSON property naming: camelCase for API responses.

## Anti-Patterns

| Anti-Pattern | Why it's wrong |
|-------------|----------------|
| Exposing JPA entities as JSON | Leaks internal structure, breaks when schema changes |
| Mutable DTOs with setters | Allows partial construction, race conditions |
| Validation in the service layer only | Invalid data reaches business logic |
| `Map<String, Object>` as response | No type safety, no documentation, no validation |
| Float for money | Precision loss — use `BigDecimal` / `Decimal` |

## LLM Instructions

- When generating an endpoint, always create separate request and response DTO classes.
- Include validation annotations on all request DTO fields.
- Map domain objects to response DTOs via explicit factory methods.
- Never return domain objects or entities directly from controllers.

## Review Checklist

- [ ] Request DTOs have validation on all fields.
- [ ] Response DTOs are separate from domain objects.
- [ ] Error responses follow the standard envelope.
- [ ] No floats for monetary values.
- [ ] No internal details exposed in error messages.

## References

- [coding-standards.md](coding-standards.md)
- [security-standards.md](security/security-standards.md)
