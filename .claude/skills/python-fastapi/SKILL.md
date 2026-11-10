---
name: python-fastapi
description: Use for Python/FastAPI design, implementation, review, async behavior, validation, dependency management, and production configuration.
---

# Python / FastAPI

- Keep route functions thin.
- Use validated request/response models.
- Do not block the async event loop with synchronous I/O.
- Isolate provider integrations behind meaningful boundaries.
- Keep configuration explicit.
- Prefer deterministic tests without requiring external services when the behavior can be isolated.
- Test production database/provider semantics in integration tests where they matter.

## Layering

Severities follow `code-quality`. Where the repository has no service layer (for example controller → repository), its existing shape wins: LY1 is High only where a service layer exists. When new business logic would otherwise land in a controller, raise it as a decision at Plan review (Medium); do not add a service layer on your own.

| ID | Rule | Severity |
| --- | --- | --- |
| LY1 | Router → service → repository. A route function handles HTTP only: parsing, validation, and mapping to the response model. It never queries the database or calls a repository. | High |
| LY2 | Business rules, side effects (publishing events, calling other services), and transaction or session boundaries belong in the service. | Medium |
| LY3 | A service takes no FastAPI or Starlette types (`Request`, `Response`, `HTTPException`). A repository returns domain or persistence types, not response models. | High |
