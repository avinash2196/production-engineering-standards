---
applyTo: "**/*.java"
description: "Use when writing, reviewing, or generating Java code. Enforces Spring Boot 3.x layered architecture, naming conventions, constructor injection, error handling, testing patterns, and capability interface usage."
---

Follow all rules in [stacks/java-springboot/java-spring.md](../../stacks/java-springboot/java-spring.md) and [standards/coding-standards.md](../../standards/coding-standards.md).

## Layer Rules

- **Controller**: annotate with `@RestController`. Accept/return DTOs (records). Delegate immediately to service. No `@Autowired` — constructor injection only.
- **Service**: annotate with `@Service`. Inject capability interfaces (`MessagePublisher`, `CacheProvider`, etc.), never `KafkaTemplate`, `RedisTemplate`, or `AmazonS3` directly.
- **Domain**: plain Java classes/records/enums. Zero Spring annotations outside of `@Entity`/`@Embeddable`. No `import org.springframework.*` in domain classes.
- **Repository**: extend `JpaRepository` or `CrudRepository`. One interface per aggregate root.
- **Infrastructure**: implement capability interfaces here. Fallback beans use `@Profile("fallback-{capability}")`.

## Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Class | `PascalCase` + role suffix | `OrderService`, `OrderController` |
| Method | `camelCase`, verb-first | `findOrderById`, `publishOrderCreated` |
| DTO | `{Entity}Request` / `{Entity}Response` | `CreateOrderRequest` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Test class | `{Subject}Test` | `OrderServiceTest` |

## Hard Rules

- **Constructor injection only** — never `@Autowired` on fields.
- Methods: **max 30 lines**. If longer, extract a private method or a domain service.
- Classes: **max 300 lines**. If longer, split responsibilities.
- Constructor parameters: **max 4**. If more, introduce a parameter object.
- DTOs are Java `record`s with `@Valid` + `@NotNull`/`@NotBlank` annotations.
- All secrets via `SecretProvider.get(key)` — never `@Value("${secret.*}")`.
- Throw domain exceptions (`OrderNotFoundException extends RuntimeException`), not raw `Exception`.
- Use `@ControllerAdvice` + `@ExceptionHandler` for error responses — never return `null`.

## Observability

- Log with SLF4J + structured MDC: `MDC.put("orderId", orderId.toString())`.
- Emit Micrometer metrics: `meterRegistry.counter("order.created").increment()`.
- Annotate service methods with `@Observed` or manually create spans for complex flows.

## Testing

- Unit tests: mock capability interfaces with `@MockBean` or Mockito. No Spring context needed for service tests.
- Integration tests: use `@SpringBootTest` + Testcontainers. Never mock the database in integration tests.
- See [standards/testing/unit-testing.md](../../standards/testing/unit-testing.md).
