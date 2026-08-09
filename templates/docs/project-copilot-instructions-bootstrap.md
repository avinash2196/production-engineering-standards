---
# How to use this file:
# 1. Copy it to .github/copilot-instructions.md in the target project.
# 2. Replace {STANDARDS_REPO} with a path that is available in the workspace,
#    or copy the referenced standards into the target repository.
# 3. Enable referenced instructions only when the selected editor/version
#    supports them; otherwise treat the links as human navigation.
# 4. Add project-specific constraints below rather than modifying shared rules silently.
---

# Project Engineering Instructions

This project uses the production-engineering-standards repository as a source of engineering guidance, reusable review workflows, and executable checks.

Copilot instructions guide generation and review. They do not make compliance deterministic. Tests, static analysis, startup guards, and CI enforce the rules that can be checked automatically; architecture and design decisions still require human review.

> Standards repository: `{STANDARDS_REPO}`

## Required Delivery Lifecycle

For any non-trivial behavior change, use this sequence:

1. **Plan** — define scope, requirements, constraints, risks, milestones,
   and success criteria.
2. **Human Review** — review and approve the Plan.
3. **Implementation Plan** — inspect the current repository and define
   exact milestone-level files, tests, and implementation changes.
4. **Human Review** — review and approve the Implementation Plan.
5. **RED Tests** — create the approved tests and confirm valid RED.
6. **GREEN Code** — implement the minimum approved production behavior
   required for GREEN.
7. **Refactor** — improve structure only after GREEN while preserving behavior.
8. **Final Review** — verify scope, evidence, tests, and applicable standards.

Do not combine planning and production-code generation in one step. Do not silently expand scope. Record clarifying questions instead of inventing material requirements.

Full workflow: `{STANDARDS_REPO}/standards/prompt-driven-development-workflow.md`

## Architecture Defaults

Use boundaries that match the service's business complexity:

```text
API/Transport -> Application Service -> Domain Decisions
                         |
                         v
                   Ports/Contracts
                         ^
                         |
        Persistence and Infrastructure Adapters
```

- API code handles transport, validation, and response mapping.
- Application services coordinate use cases and transactions.
- Domain code owns business rules when the domain has meaningful invariants.
- Ports protect business code from vendor-specific messaging, cache, storage, secrets, and persistence APIs.
- Infrastructure adapters implement those ports.
- A simple CRUD service may use fewer layers when the decision is documented and dependencies remain controlled.

Full rules: `{STANDARDS_REPO}/standards/architecture.md`

## Capability Contracts

Use an abstraction when it creates a stable testing, portability, or policy boundary. Available shared contracts include:

| Contract | Capability |
|---|---|
| `MessagePublisher` / `MessageSubscriber` | Durable messaging |
| `CacheProvider` | Caching |
| `ObjectStorageProvider` | Object storage |
| `SecretProvider` | Managed secret access |
| `ConfigProvider` | Typed runtime configuration |

Do not introduce an interface solely to wrap a single call without a real boundary or expected variation.

Specifications: `{STANDARDS_REPO}/contracts/`

## Local Adapters and Production Degradation

Keep these concerns separate:

- **Local adapters** make local development and selected tests possible without every managed dependency. Examples include a database outbox, JSON-file cache, local filesystem, or environment-backed secrets.
- **Production degradation** defines what happens when a live dependency fails: retry, queue, serve stale data, bypass a non-critical capability, fail closed, or fail fast.

Local adapters must be explicit, observable, document reduced guarantees, and be rejected by production startup checks. A service does not need a local adapter for every dependency.

- Local adapter guidance: `{STANDARDS_REPO}/standards/local-adapter-strategy.md`
- Production failure guidance: `{STANDARDS_REPO}/standards/fallback-strategy.md`

## Engineering Rules

1. Keep business decisions independent of transport and vendor SDK details.
2. Store secrets through an approved secret provider; do not hardcode credentials.
3. Define a timeout and explicit failure behavior for remote calls.
4. Add logs, health checks, metrics, and traces according to the service's support model and critical paths.
5. Review collection access for N+1 behavior and select joins, batching, entity graphs, or purpose-built queries based on cardinality and pagination.
6. Treat method length, class size, and constructor size as review signals. Report the concrete responsibility or testability problem rather than failing code on a number alone.
7. Keep production behavior changes separate from refactoring whenever practical.

## Standards Quick Reference

| Concern | Shared reference |
|---|---|
| Delivery lifecycle | `standards/prompt-driven-development-workflow.md` |
| Architecture | `standards/architecture.md` |
| Coding and naming | `standards/coding-standards.md`, `standards/naming.md` |
| API and DTOs | `standards/api-design.md`, `standards/dto-guidelines.md` |
| Security | `standards/security/security-standards.md` |
| Observability | `standards/observability.md` |
| Testing | `standards/testing/unit-testing.md` |
| Enforcement status | `docs/enforcement-matrix.md` |

## Stack Guidance

- Java and Spring Boot: `{STANDARDS_REPO}/stacks/java-springboot/java-spring.md`
- Python and FastAPI: `{STANDARDS_REPO}/stacks/python-fastapi/python-backend.md`

## Reusable Prompt Workflow

## Reusable Prompt Workflow

For explicit phase-by-phase execution:

1. `/create-plan`
2. review and approve the Plan
3. `/create-implementation-plan`
4. review and approve the Implementation Plan
5. `/generate-tests` — establish RED only
6. implement the smallest approved GREEN change
7. `/refactor-code` — only after GREEN
8. `/review-code` or the applicable final review

`/implement-approved-plan` is an optional orchestrated workflow that
executes RED → GREEN → REFACTOR sequentially from an already approved
Implementation Plan.

Use the phase-by-phase workflow when independent RED/GREEN evidence or
human inspection between phases is important.

Copy prompt files from `{STANDARDS_REPO}/.github/prompts/` into the target repository only after validating their relative references and supported tool names.
