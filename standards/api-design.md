# API Design

Purpose
- Define stable, versioned, and testable API surface contracts for services.

Mandatory Rules
- Use explicit request/response DTOs; never expose internal domain objects directly.
- Version all external APIs (URI or header-based) and maintain backwards-compatible changes.
- Return structured error payloads with machine-readable error codes and human-friendly messages.
- Enforce input validation at the edge and map failures to appropriate HTTP status codes.

Defaults
- Use camelCase for JSON fields for JavaScript/TypeScript consumers; document alternatives per stack.
- Default API version header: `X-Api-Version` and route prefix `/v1`.

Anti-patterns
- Returning partially-formed domain objects or entity models directly to clients.
- Placing business logic in controllers or relying on implicit behavior for defaults.

LLM instructions
- When scaffolding APIs, generate DTO classes/files for request and response and a mapping layer between DTOs and domain objects.
- Ask the user only if an API change affects backwards compatibility, data exposure, or retention.

Review checklist
- [ ] DTOs present for all external endpoints.
- [ ] Versioning strategy documented and applied.
- [ ] Error response schema documented and used.
- [ ] Input validation implemented and tested.

