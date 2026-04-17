# Coding Standards

Language-agnostic coding standards and style guidance for all enterprise services.

## Purpose

Establish consistent, readable, and maintainable code across teams and stacks by defining rules that apply regardless of language.

## Mandatory Rules

### Naming

| Element | Convention | Example |
|---------|------------|---------|
| Classes / types | PascalCase | `OrderService`, `PaymentResult` |
| Methods / functions | camelCase (Java) / snake_case (Python) | `createOrder()`, `create_order()` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Variables | camelCase (Java) / snake_case (Python) | `orderId`, `order_id` |
| Database columns | snake_case | `created_at`, `user_id` |
| REST endpoints | kebab-case nouns | `/api/v1/order-items` |
| Environment variables | UPPER_SNAKE_CASE | `KAFKA_BOOTSTRAP_SERVERS` |

### Methods

- Maximum **30 lines** per method (excluding blank lines and braces). Extract helpers if longer.
- Maximum **4 parameters**. Use an options/config object for more.
- Return early for guard clauses — avoid deep nesting.
- One level of abstraction per method.

### Classes

- Maximum **300 lines** per class/module. Split by responsibility if larger.
- **Single Responsibility Principle** — each class does one thing.
- Prefer composition over inheritance.
- No utility classes with only static methods — use module-level functions (Python) or focused services (Java).

### Error Handling

- Throw domain-specific exceptions, not generic `RuntimeException` or bare `Exception`.
- Catch at the right level — usually the service layer or a global handler.
- Never swallow exceptions silently — always log or re-throw.
- Use typed error responses for APIs (see `dto-guidelines.md`).

### Comments

- Code should be self-documenting. Comments explain **why**, not **what**.
- Delete commented-out code — use version control instead.
- Public APIs require doc comments (Javadoc, docstrings) documenting purpose, params, return, and exceptions.
- TODOs must include a ticket reference: `// TODO(PROJ-123): migrate to async`.

### Imports

- No wildcard imports (`import *`).
- Group imports: standard library → third-party → internal.
- Remove unused imports (enforced by linter).

## Defaults

- Use the stack-specific formatter/linter configured in project templates:
  - Java: `google-java-format` + `Checkstyle`
  - Python: `ruff` (format + lint)
- Format on save — no manual formatting discussions in reviews.
- Line length: 120 characters (Java), 100 characters (Python).

## Anti-Patterns

| Anti-Pattern | Why it's wrong |
|-------------|----------------|
| Magic numbers | Use named constants. `if (retries > 3)` → `if (retries > MAX_RETRIES)` |
| Boolean parameters | `createOrder(true, false)` is unreadable. Use enums or config objects. |
| String typing | Use enums or value objects instead of raw strings for states, types, categories. |
| Premature optimization | Optimize after profiling, not before. Readability first. |
| God objects | Classes with 10+ dependencies indicate design problems. |

## LLM Instructions

- When generating code, follow the naming conventions for the target language.
- Keep generated methods under 30 lines. If a method grows longer, split it.
- Never generate commented-out code blocks or TODO comments without ticket references.
- Use domain-specific exception types rather than generic exceptions.

## Review Checklist

- [ ] Naming follows conventions for the language.
- [ ] No methods exceed 30 lines.
- [ ] No classes exceed 300 lines.
- [ ] No wildcard imports.
- [ ] No magic numbers or string-typed enums.
- [ ] Error handling uses domain exceptions.
- [ ] Comments explain why, not what.

## References

- [dto-guidelines.md](dto-guidelines.md)
- [Java Spring Boot conventions](../stacks/java-springboot/java-spring.md)
- [Python FastAPI conventions](../stacks/python-fastapi/python-backend.md)
