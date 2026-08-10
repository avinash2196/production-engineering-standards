---
description: "Apply the PDD lifecycle when creating a new Java Spring Boot or Python FastAPI service."
applyTo: "**/*"
---

# New Service Instructions

Do not create a complete service directly from a short request.

## Required Sequence

1. Review requirements and current repository context. Ask numbered clarification questions and stop when a material planning decision is unresolved.
2. Create `docs/.ai/Plan.md`; no tests or implementation.
3. Model behavior-changing work with separate `RED` and `GREEN` milestones. Add a separate `REFACTOR` milestone only when justified.
4. Obtain human Plan approval.
5. Create the phase-specific `docs/.ai/NNN_Implementation_Plan_<Milestone>.md` for the next approved milestone only.
6. Obtain human approval for that milestone Implementation Plan.
7. If the milestone is RED, write approved tests/checks only, confirm valid RED, record evidence, and stop.
8. Create and obtain approval for the separate GREEN milestone Implementation Plan.
9. If the milestone is GREEN, verify predecessor RED evidence, implement the smallest approved production change, confirm GREEN, record evidence, and stop.
10. If a concrete refactor is justified, create and approve a separate REFACTOR milestone/Implementation Plan and execute it from a verified GREEN baseline.
11. Complete final review and validation after the required milestone chain is complete.

Do not automatically advance from one phase to the next. An end-to-end request does not waive the Plan or per-milestone review gates for behavior-changing work.

Reference: [Prompt-Driven Development Workflow](../../standards/prompt-driven-development-workflow.md)

## Service Decisions

Use only capabilities required by approved requirements/current milestone. Do not automatically add messaging, cache, storage, security, observability dependencies, or local adapters.

When an approved service actually needs them, adapter selections may include:

- `MESSAGING_ADAPTER`: production `kafka`/`pubsub`; local `db`/`inmemory`
- `CACHE_ADAPTER`: production `redis`; local `jsonfile`/`inmemory`
- `STORAGE_ADAPTER`: production `s3`/`gcs`; local `local`
- `SECRET_ADAPTER`: production `vault`/`secretmanager`; local `env`

Local-only adapters must not silently activate in production and must document reduced guarantees.

## Review Checklist

- [ ] Material requirements were clarified rather than invented
- [ ] Plan approved before milestone Implementation Plans
- [ ] RED and GREEN are separate milestones for behavior-changing work
- [ ] Current phase Implementation Plan approved before execution
- [ ] RED changed tests/checks only and valid RED was observed
- [ ] GREEN had predecessor RED evidence and used minimum implementation
- [ ] REFACTOR, when present, was separate, justified, and behavior-preserving
- [ ] Dependencies and abstractions are justified by approved scope
- [ ] Local adapter and production degradation decisions remain separate
