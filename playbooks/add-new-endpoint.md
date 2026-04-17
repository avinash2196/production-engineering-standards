# Workflow: Add New Endpoint

## Purpose

Step-by-step procedure for adding a new REST endpoint to an existing service, ensuring it follows layered architecture, observability, testing, and security standards.

## Prerequisites

- Existing service with established layered architecture
- Clear requirement for the new endpoint (resource, operation, request/response)

## Steps

### 1. Define the Endpoint Contract

Before writing code, define:

| Aspect | Decision |
|--------|----------|
| HTTP method | GET / POST / PUT / DELETE / PATCH |
| Path | `/api/v1/<resource>` following `standards/api-design.md` |
| Request DTO | Fields, validation rules, required vs optional |
| Response DTO | Fields, HTTP status codes (success + error cases) |
| Auth required? | Yes (default) — specify required role/scope |

### 2. Create DTOs

- Create request DTO with validation annotations (`@NotNull`, `@Size` / Pydantic validators)
- Create response DTO separate from domain entity
- Never expose domain entities directly in API responses

Reference: `standards/api-design.md`, `standards/dto-guidelines.md`

### 3. Implement Controller Method

- Controller receives request DTO, validates input, delegates to service layer
- No business logic in the controller — only mapping and delegation
- Return appropriate HTTP status codes (201 for create, 200 for read, 204 for delete)
- Add error handling for validation failures (400) and not-found (404)

### 4. Implement Service Method

- Service contains the business logic
- Interact with domain entities and repository interfaces
- Use capability abstractions for external calls (`CacheProvider`, `MessagePublisher`, etc.)
- Add structured logging at method entry/exit with `correlationId`
- Emit metrics: latency histogram + error counter

### 5. Update Domain Layer (if needed)

- Add or update domain entities/value objects
- Domain layer must have no infrastructure imports
- Enforce invariants in the domain model

### 6. Update Repository (if needed)

- Define repository interface in domain layer
- Implement in adapter/infra layer
- Never expose raw database entities — map to domain objects

### 7. Add Observability

- [ ] Structured log at controller entry with request metadata
- [ ] Span created for the endpoint (auto if using framework instrumentation)
- [ ] Latency histogram metric: `<service>_<resource>_<method>_duration_seconds`
- [ ] Error counter metric: `<service>_<resource>_<method>_errors_total`
- [ ] Correlation ID propagated if making downstream calls

### 8. Write Tests

Invoke **test-engineer** patterns:

- **Unit tests** for service method: mock all abstractions, test happy path + primary error cases
- **Controller test** (if stack supports it): verify request validation, status codes, DTO mapping
- **Integration test** (if endpoint involves new adapter interactions): use testcontainers or fallback

### 9. Review

Run through these checks:

- [ ] Controller is thin (no business logic)
- [ ] DTOs separate from domain entities
- [ ] Input validation at controller boundary
- [ ] Service uses abstractions (not direct SDK imports)
- [ ] Structured logging with correlation ID
- [ ] Metrics emitted
- [ ] Auth/authz configured
- [ ] Tests pass (unit + integration)

### 10. Commit

Conventional commit: `feat(<service>): add <verb> <resource> endpoint`
