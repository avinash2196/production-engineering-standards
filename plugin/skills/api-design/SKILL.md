---
name: api-design
description: Use when creating or changing HTTP/API contracts, DTOs, validation, errors, pagination, versioning, or compatibility.
---

# API Design

- Keep transport models explicit.
- Validate input at the boundary.
- Use stable error contracts where clients depend on them.
- Distinguish absent, null, empty, and default semantics.
- Preserve backward compatibility unless an approved plan changes it.
- Make pagination, idempotency, retryability, and concurrency semantics explicit where relevant.
- Avoid leaking persistence entities directly as public API contracts.

