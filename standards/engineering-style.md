# Engineering Style

This style guide focuses on consistent, production-oriented patterns for code and architecture across Java and Python stacks.

1. Code Organization
- Follow layered architecture: `controller` (API) → `service` (business orchestration) → `domain` (entities, value objects) → `repository` (data access).
- Keep modules small and single-responsibility. Avoid god classes.

2. Naming and DTOs
- Use explicit DTOs for requests and responses. Map DTOs to/from domain objects in the service layer.
- Use clear, domain-driven names; keep API models stable and versioned.

3. Configuration
- Centralize configuration models using `pydantic`/`spring-configuration` patterns. Avoid ad-hoc environment reads scattered through code.

4. Error Handling
- Prefer typed errors and error codes. Controllers convert domain/service errors into HTTP status + structured error payloads.

5. Asynchrony
- Explicitly mark async boundaries. Use message-driven patterns for eventual work and HTTP/REST for synchronous interactions.

6. Observability
- Inject correlation IDs at the edge (API gateway or controller) and pass them downstream. Instrument with OpenTelemetry and Micrometer where applicable.

7. Security
- Validate inputs strictly and minimize returned data. Apply field-level redaction in logs for PII/PHI.

8. Tests
- Provide unit tests for business logic, integration tests for infra wiring (use local fallbacks), and contract tests for APIs.
