# Enterprise AI Engineering Standards

A practical repository for turning persistent Copilot guidance into repeatable engineering workflows and executable quality gates for Java Spring Boot and Python FastAPI services.

The repository is intentionally not a promise that AI-generated code is automatically production-ready. Copilot instructions guide decisions, prompts make reviews repeatable, and tests, validators, static analysis, and CI enforce the rules that can be checked automatically.

## Why This Repository Exists

A single `copilot-instructions.md` file is useful for persistent context, but it is not enough for engineering governance. This repository separates:

1. **Stable standards** — architecture, testing, security, observability, local adapters, and production degradation.
2. **Task workflows** — Plan, Implementation Plan, tests, implementation, refactoring, and review.
3. **Executable enforcement** — repository tests, validators, stack-specific tests, and CI gates.
4. **Human judgment** — architecture, trade-offs, operational safety, and exceptions that cannot be reduced to a brittle rule.

## Required Development Lifecycle

Qualifying implementation work follows:

> **Requirements → Plan → Human Review → Implementation Plan → Human Review → RED Tests → GREEN Code → Refactor → Final Review**

The two planning artifacts have different responsibilities:

- `docs/.ai/Plan.md` defines **what** will be delivered, milestone order, scope, risks, and success criteria.
- `docs/.ai/NNN_Implementation_Plan_<Milestone>.md` defines **how** one approved milestone will be implemented: exact files, tests, expected RED behavior, minimal GREEN code, refactoring boundaries, and commands.

Production code is not written during either planning phase. Tests or executable checks are created first, observed RED for the intended reason, followed by the smallest implementation required for GREEN. Refactoring is separate and must preserve GREEN.

See [Prompt-Driven Development Workflow](standards/prompt-driven-development-workflow.md).

## Experience-Driven Adapter and Failure Strategy

The repository preserves a practical distinction that is often lost in generic AI guidance.

### Local adapters

Local adapters make development and CI possible without every external service:

| Capability | Production adapter examples | Local-only adapter examples |
|---|---|---|
| Messaging | Kafka, Pub/Sub | database-backed queue/outbox, in-memory queue |
| Cache | Redis | inspectable JSON-file cache, in-memory cache |
| Storage | S3, GCS | local filesystem |
| Secrets | Vault, Secret Manager | environment-variable provider |

Local adapters must be explicit, observable, testable, and blocked in production. Their reduced durability, ordering, consistency, concurrency, and security guarantees must be documented.

### Production degradation

Production dependency failure is a separate design decision. A service may fail fast, fail closed, retry, circuit-break, queue durably, serve stale data, bypass a non-critical capability, or operate with reduced functionality.

The fallback itself is not the standard. The standard is that degraded behavior is **explicit, observable, testable, and unable to activate silently**.

See:

- [Local Adapter Strategy](standards/local-adapter-strategy.md)
- [Production Dependency Failure and Degradation](standards/fallback-strategy.md)

## How Standards Are Applied

| Level | Purpose | Examples |
|---|---|---|
| **Guidance** | Influence planning, generation, and review | Copilot instructions, stack guidance |
| **Repeatability** | Apply the same workflow and review structure | Prompt files, agent specifications, playbooks |
| **Enforcement** | Fail an executable check on violation | Unit tests, integration tests, repository validator, CI |
| **Human review** | Evaluate context-sensitive trade-offs | Architecture, resilience, security, operational readiness |

A documented rule is described as enforced only when an executable mechanism blocks the violation. Current status is tracked in the [Enforcement Matrix](docs/enforcement-matrix.md).

## Repository Structure

```text
.github/
  copilot-instructions.md       Workspace-level persistent guidance
  instructions/                Stack and task-specific instructions
  prompts/                     Reusable PDD and review workflows
  workflows/                   Repository validation CI
agents/                        Agent responsibilities and review behavior
contracts/                     Capability boundaries
standards/                     Engineering rules and decision guidance
stacks/                        Java and Python stack guidance/templates
playbooks/                     Step-by-step delivery and operational workflows
templates/                     Plan, Implementation Plan, ADR, infra, and docs templates
examples/                      Reference architectures and behavior walkthroughs
tooling/                       Dependency-free validator and tests
docs/                          Overview, decisions, and enforcement status
```

## Using the Repository

### In this repository

VS Code Copilot loads `.github/copilot-instructions.md` from the workspace. Prompt files under `.github/prompts/` provide workflows such as:

- `/create-plan`
- `/create-implementation-plan`
- `/implement-approved-plan`
- `/generate-tests`
- `/refactor-code`
- `/scaffold-service`
- `/review-code`
- `/review-architecture`
- `/review-distributed-systems`
- `/review-production-readiness`

### In another project

Choose one controlled distribution approach:

1. Copy or synchronize the relevant instruction and prompt files into the target repository.
2. Open the standards repository and target repository in the same VS Code workspace and configure referenced-instruction inclusion deliberately.
3. Publish approved organization-level instructions where supported.

Do not assume that a Markdown link to an arbitrary local clone automatically distributes or enforces standards for every developer and CI environment.

Start with [`templates/docs/project-copilot-instructions-bootstrap.md`](templates/docs/project-copilot-instructions-bootstrap.md), then adapt paths and enabled prompts for the target repository.

## Validation

Run the tests first:

```bash
python -m unittest discover -s tooling/tests -p 'test_*.py'
```

Then run the repository validator:

```bash
python tooling/scripts/validate_repository.py
```

Run the executable Python template checks after installing its minimal test dependencies:

```bash
PYTHONPATH=stacks/python-fastapi/project-template \
  python -m unittest discover \
  -s stacks/python-fastapi/project-template/tests \
  -p 'test_*.py'
```

Windows wrapper:

```powershell
pwsh tooling/scripts/validate-repo-structure.ps1
```

CI runs the same sequence and currently enforces:

- required repository structure
- active Markdown link integrity
- prompt frontmatter conventions
- absence of known placeholder implementations
- absence of deprecated active configuration terminology
- Python local-adapter selection and production startup guards

Project-level enforcement such as Java architecture tests, Python import-boundary checks, secret scanning, dependency scanning, and service tests belongs in each generated or adopting project.

## Important Standards

- [Prompt-Driven Development Workflow](standards/prompt-driven-development-workflow.md)
- [Agent Execution](standards/agent-execution.md)
- [Architecture](standards/architecture.md)
- [Engineering Principles](standards/engineering-principles.md)
- [Coding Standards](standards/coding-standards.md)
- [Testing](standards/testing/unit-testing.md)
- [Security](standards/security/security-standards.md)
- [Observability](standards/observability.md)
- [Production Readiness](standards/production-readiness.md)

## Human Review

Agents may create plans, tests, source changes, and review reports. They must not silently broaden scope, invent requirements, commit secrets, or claim commands passed when they were not run. Human review remains required before accepting implementation and production-readiness decisions.
