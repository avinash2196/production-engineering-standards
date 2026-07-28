---
description: "Apply the PDD lifecycle when creating a new Java Spring Boot or Python FastAPI service."
applyTo: "**/*"
---

# New Service Instructions

Do not create a complete service directly from a short request.

## Required Sequence

1. Review requirements and current repository context.
2. Create `docs/.ai/Plan.md`; no tests or implementation.
3. Obtain human approval.
4. Create `docs/.ai/NNN_Implementation_Plan_<Milestone>.md`; define exact tests and code changes, but do not implement.
5. Obtain human approval.
6. Write milestone tests first and confirm valid RED.
7. Implement the smallest production change to reach GREEN.
8. Refactor separately and keep tests GREEN.
9. Complete final review and validation.

Reference: [Prompt-Driven Development Workflow](../../standards/prompt-driven-development-workflow.md)

## Service Decisions

Use only capabilities required by the service. Do not automatically add messaging, cache, storage, or local adapters.

When needed, adapter selection uses:

- `MESSAGING_ADAPTER`: production `kafka`/`pubsub`; local `db`/`inmemory`
- `CACHE_ADAPTER`: production `redis`; local `jsonfile`/`inmemory`
- `STORAGE_ADAPTER`: production `s3`/`gcs`; local `local`
- `SECRET_ADAPTER`: production `vault`/`secretmanager`; local `env`

Local-only adapters must fail startup in production and document reduced guarantees.

## Review Checklist

- [ ] Plan approved before Implementation Plan
- [ ] Implementation Plan approved before source changes
- [ ] Tests created and observed RED first
- [ ] Minimal GREEN implementation
- [ ] Refactor after GREEN only
- [ ] Dependencies and abstractions are justified
- [ ] Local adapter and production degradation decisions are separate
