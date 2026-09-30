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

