# Production Engineering Standards

Practical engineering standards for building production-oriented backend and distributed systems in Java and Python with AI-assisted development.

The repository is intentionally not a promise that AI-generated code is automatically production-ready. Copilot instructions guide decisions, prompts make reviews repeatable, and tests, validators, and CI enforce the rules that can be checked automatically.

## Why This Repository Exists

A single `copilot-instructions.md` file is useful for persistent context, but it is not enough for engineering governance. This repository separates:

1. **Stable standards** — architecture, testing, security, observability, local adapters, and production degradation.
2. **Task workflows** — requirements analysis, Plan, Implementation Plan, tests, implementation, refactoring, and review through prompt files, Agent Skills, and GitHub Copilot custom agents.
3. **Executable enforcement** — repository tests, validators, stack-specific tests, and CI gates.
4. **Human judgment** — architecture, trade-offs, operational safety, and exceptions that cannot be reduced to a brittle rule.

## Required Development Lifecycle

Qualifying implementation work follows the same high-level PDD/TDD sequence used throughout this repository:

> **Requirements → Plan → Human Review → Implementation Plan → Human Review → RED Tests → GREEN Code → Refactor → Final Review**

The important control boundary is that **RED, GREEN, and optional REFACTOR are separate Plan milestones for behavior-changing work**:

```text
Approved Plan
  → RED milestone
      → RED Implementation Plan
      → Human Review
      → Tests/checks only
      → Valid RED evidence
  → GREEN milestone
      → GREEN Implementation Plan
      → Human Review
      → Minimal production implementation
      → GREEN evidence
  → REFACTOR milestone (only when justified)
      → REFACTOR Implementation Plan
      → Human Review
      → Behavior-preserving cleanup
      → Remains GREEN
  → Final Review
```

`docs/.ai/Plan.md` defines **what** will be delivered, the phase-specific milestone order, predecessor relationships, scope, risks, and success criteria. Each repository-changing milestone then receives its own `docs/.ai/NNN_Implementation_Plan_<Milestone>.md`, which defines **how that phase only** will be executed.

This extra separation is intentional for AI-assisted development: a human can validate the RED interpretation before production code is authorized, GREEN stays minimal, and refactoring cannot be smuggled into feature implementation. An end-to-end request does not waive these review gates for behavior-changing work.

Before Plan creation, material requirement ambiguity is resolved rather than guessed through. Framework defaults, common practices, and industry assumptions do not become requirements merely because information is missing.

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
| **Repeatability** | Apply the same workflow and review structure | Prompt files, Agent Skills, custom agents, playbooks |
| **Enforcement** | Fail an executable check on violation | Unit tests, integration tests, repository validator, CI |
| **Human review** | Evaluate context-sensitive trade-offs | Architecture, resilience, security, operational readiness |

A documented rule is described as enforced only when an executable mechanism blocks the violation. Current status is tracked in the [Enforcement Matrix](docs/enforcement-matrix.md).

Repository tests also guard the canonical PDD phase model so active guidance cannot silently collapse RED, GREEN, and optional REFACTOR back into one milestone or one Implementation Plan.

## Repository Structure

```text
.github/
  copilot-instructions.md       Workspace-level persistent guidance
  instructions/                Path-specific stack instructions
  agents/                      GitHub Copilot custom agent profiles (`*.agent.md`)
  prompts/                     Reusable PDD and review workflows
  skills/                      Task-specific Agent Skills for requirements and review
  workflows/                   Repository validation CI
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

GitHub Copilot loads repository-wide instructions from `.github/copilot-instructions.md` on supported surfaces, while `.github/instructions/*.instructions.md` applies only to matching file paths. Prompt files under `.github/prompts/` provide explicit reusable tasks in supported VS Code local-agent workflows; specialist prompts bind to repository custom agents under `.github/agents/`, and Agent Skills under `.github/skills/` provide reusable capabilities that Copilot can load when relevant. GitHub Copilot Agent Host does not consume prompt files, so cross-surface governance must remain in repository instructions, skills, custom agents, standards, tests, and CI rather than relying on prompts alone. See [Copilot Customization Model](docs/copilot-customizations.md).

Prompt workflows include:

- `/review-requirements`
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

Run the tests first without creating Python bytecode inside the repository:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tooling/tests -p 'test_*.py'
```

Then run the repository validator:

```bash
PYTHONDONTWRITEBYTECODE=1 python tooling/scripts/validate_repository.py
```

Run the canonical minimal Python starter checks after installing its minimal dependencies:

```bash
PYTHONPATH=stacks/python-fastapi/project-template \
  python -m unittest discover \
  -s stacks/python-fastapi/project-template/tests \
  -p 'test_*.py'
```


The Python local-adapter implementation is a separate reference under `stacks/python-fastapi/reference-implementations/local-adapters/`. Run its tests only when working on that reference and after installing its own dependencies. Passing those tests is not production-readiness evidence for managed dependencies.

Windows wrapper:

```powershell
pwsh tooling/scripts/validate-repo-structure.ps1
```

CI runs the same sequence and currently enforces:

- required repository structure
- active Markdown link integrity
- prompt frontmatter syntax, current tool-set aliases, and valid custom-agent bindings
- path-specific instruction frontmatter and rejection of repository-global `applyTo: "**/*"` files
- custom-agent profile location, `.agent.md` naming, required description, and tool-list structure
- rejection of the obsolete top-level `agents/` hierarchy
- repository-package hygiene for IDE/Python cache artifacts
- Agent Skill structure and required frontmatter
- canonical PDD phase-milestone semantics (separate RED/GREEN/optional-REFACTOR milestones and phase-specific Implementation Plans)
- absence of known placeholder implementations
- absence of deprecated active configuration terminology and legacy custom-agent references
- governance semantic checks that prevent blanket `apply all standards`, invented approval, and compliance-without-applicability behavior
- production-foundation semantic checks for minimal Python dependencies, a runnable local-adapter reference, and requirement-driven observability/configuration/security/readiness

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

Custom agents, prompts, and skills may help create plans, tests, source changes, and review reports. They must not silently broaden scope, invent requirements, commit secrets, or claim commands passed when they were not run. Human review remains required before accepting implementation and production-readiness decisions.
