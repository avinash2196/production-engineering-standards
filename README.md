# Production Engineering Standards

A Copilot-native engineering standards repository for production-oriented Java, Python, distributed-system, and database-modernization work.

The repository separates five concerns:

* **Instructions** — standing rules that should apply automatically.
* **Skills** — reusable engineering and domain knowledge loaded when relevant.
* **Agents** — responsibility-focused roles for planning, implementation, testing, refactoring, and review.
* **Prompts** — explicit entry points for repeatable Prompt-Driven Development workflows.
* **Tooling** — executable repository checks. Guidance is not described as enforcement unless a check can actually fail.

## Core Development Lifecycle

For behavior-changing work that adopts this repository's Prompt-Driven Development model:

> **Requirements → Plan → Human Review → Implementation Plan → Human Review → RED → GREEN → optional REFACTOR → Final Review**

RED, GREEN, and optional REFACTOR are separate authorization boundaries.

Completing one phase does not automatically authorize the next.

## Repository Structure

```text
.github/
  copilot-instructions.md
  instructions/            Path-scoped standing rules
  agents/                  Responsibility-focused custom agents
  skills/                  Domain knowledge + reusable engineering capabilities
  prompts/                 Explicit reusable workflow entry points
  workflows/               Repository validation CI

tooling/
  scripts/                 Dependency-free validators
  tests/                   Repository contract tests

docs/
  getting-started.md
  customization-model.md
  migration-from-v1.md
```

There are intentionally no top-level:

```text
standards/
playbooks/
stacks/
contracts/
templates/
examples/
```

Knowledge and supporting assets live with the skill that owns them.

Whole-project examples should be added only when they provide a runnable, end-to-end demonstration rather than acting as placeholders for folder structure.

## Mental Model

| Need                                          | Location                          |
| --------------------------------------------- | --------------------------------- |
| Rule that should almost always apply          | `.github/copilot-instructions.md` |
| Rule for Java, Python, SQL, or specific paths | `.github/instructions/`           |
| Specialized engineering or domain expertise   | `.github/skills/`                 |
| Responsibility or review role                 | `.github/agents/`                 |
| Explicit repeatable task                      | `.github/prompts/`                |
| Executable verification                       | `tooling/`                        |
| Human setup and repository explanation        | `docs/`                           |

A simple way to think about the model is:

> **Instructions = rules**
> **Skills = knowledge and capability**
> **Agents = responsibility**
> **Prompts = explicit workflow entry points**
> **Tooling = enforcement**

## Skills as the Knowledge Layer

Skills are the primary home for reusable engineering knowledge.

A skill may contain:

```text
SKILL.md
references/
templates/
checklists/
examples/
scripts/
```

This keeps specialized knowledge close to the capability that uses it instead of creating parallel root-level taxonomies.

Examples include:

* architecture design
* distributed systems
* API design
* testing
* resilience and degradation
* observability
* security
* compliance engineering
* production readiness
* Java and Spring Boot
* Python and FastAPI
* Oracle to PostgreSQL modernization

## Oracle to PostgreSQL Modernization

Oracle → PostgreSQL is modeled as a **skill**, not a standalone agent:

```text
.github/skills/oracle-to-postgres-modernization/
  SKILL.md
  references/
    assessment.md
    schema-and-sql-mapping.md
    spring-boot-migration.md
    verification-and-cutover.md
  templates/
  examples/
```

The distinction is intentional:

> **An agent represents responsibility. A skill represents reusable expertise.**

The planner, implementation engineer, test engineer, architecture reviewer, and code reviewer may all use the Oracle → PostgreSQL skill during different phases of a modernization effort.

Use:

```text
/migrate-oracle-to-postgres
```

when an explicit workflow entry point is useful.

## Prompt-Driven Development

The repository preserves the same controlled development lifecycle used throughout the Prompt-Driven Development approach.

For behavior-changing work:

```text
Requirements
    ↓
Plan
    ↓
Human Review
    ↓
RED Implementation Plan
    ↓
Human Review
    ↓
RED tests/checks
    ↓
Verified RED evidence
    ↓
GREEN Implementation Plan
    ↓
Human Review
    ↓
Minimum implementation
    ↓
Verified GREEN evidence
    ↓
Optional REFACTOR
    ↓
Final Review
```

The separation matters because planning, testing, implementation, and refactoring represent different authorization boundaries.

A single end-to-end request does not automatically remove those boundaries.

## Adopting the Standards Repository

An application using these standards should remain its own repository.

The application owns:

```text
.github/copilot-instructions.md
docs/.ai/Plan.md
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
source code
tests
build configuration
application-specific CI
```

The standards repository provides reusable:

```text
agents
skills
prompts
engineering knowledge
repository validation patterns
```

Do not commit machine-specific paths to a local checkout of this standards repository.

See:

* [Getting Started](docs/getting-started.md)
* [Customization Model](docs/customization-model.md)

## Validation

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tooling/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python tooling/scripts/validate_repository.py
```

CI runs the same repository-level checks.

Application-specific enforcement such as:

* unit and integration tests
* architecture tests
* migration tests
* dependency scanning
* secret scanning
* database compatibility checks
* performance tests

belongs in the adopting application.

## Human Review

Agents, skills, prompts, and instructions may accelerate engineering work, but they do not approve requirements, plans, architecture decisions, or production changes on behalf of a human reviewer.

Do not claim that tests, validators, builds, migrations, or commands passed unless they were actually executed or the result was explicitly supplied.
