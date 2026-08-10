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

1. **Plan** — define scope, requirements, constraints, risks, and small phase-specific milestones.
2. **Human Review** — review and approve the Plan.
3. **RED Milestone Implementation Plan** — define tests/checks and expected RED only.
4. **Human Review** — approve the RED Implementation Plan.
5. **RED Execution** — create approved tests/checks, confirm valid RED, record evidence, and stop.
6. **GREEN Milestone Implementation Plan** — separately define the minimum production changes using predecessor RED evidence.
7. **Human Review** — approve the GREEN Implementation Plan.
8. **GREEN Execution** — implement only the approved minimum behavior, verify GREEN, record evidence, and stop.
9. **REFACTOR Milestone** — only when concrete cleanup is justified; create and approve a separate REFACTOR Implementation Plan, preserve behavior, and remain GREEN.
10. **Final Review** — verify scope, milestone evidence, tests/checks, and applicable standards.

An end-to-end request does not waive the Plan or per-milestone human review gates for behavior-changing work.

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

For behavior-changing work:

1. `/create-plan`
2. review and approve the Plan containing separate RED/GREEN and optional REFACTOR milestones
3. `/create-implementation-plan` for the RED milestone
4. review and approve the RED Implementation Plan
5. `/generate-tests` — establish valid RED only and stop
6. `/create-implementation-plan` for the GREEN milestone
7. review and approve the GREEN Implementation Plan
8. `/implement-approved-plan` — implement minimal GREEN only and stop
9. when justified, `/create-implementation-plan` for the REFACTOR milestone
10. review and approve the REFACTOR Implementation Plan
11. `/refactor-code` — preserve GREEN and stop
12. `/review-code` or the applicable final review

No prompt is allowed to execute RED → GREEN → REFACTOR sequentially from one Implementation Plan. Each phase milestone has its own reviewed authorization boundary.

Copy prompt files from `{STANDARDS_REPO}/.github/prompts/` into the target repository only after validating their relative references and supported tool names.
