# Production Engineering Standards

A Copilot-native engineering standards repository for production-oriented Java, Python, distributed-system, and database-modernization work.

The repository separates five concerns:

- **Instructions** — standing rules that should apply automatically.
- **Skills** — reusable engineering and domain knowledge loaded when relevant.
- **Agents** — responsibility-focused roles for planning, implementation, testing, refactoring, and review.
- **Prompts** — explicit entry points for repeatable Prompt-Driven Development workflows.
- **Tooling** — executable repository checks. Guidance is not described as enforcement unless a check can actually fail.

## Core Development Lifecycle

For behavior-changing work that adopts this repository's Prompt-Driven Development model:

> **Requirements → Plan → Human Review → Implementation Plan → Human Review → RED → GREEN → optional REFACTOR → Final Review**

RED, GREEN, and REFACTOR are separate authorization boundaries. Completing one phase does not authorize the next.

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

examples/
  reference-service/       Small adoption example

docs/
  getting-started.md
  customization-model.md
  migration-from-v1.md
```

There are intentionally **no** top-level `standards/`, `playbooks/`, `stacks/`, `contracts/`, or `templates/` directories. Knowledge and supporting assets live with the skill that owns them.

## Mental Model

| Need | Location |
|---|---|
| Rule that should almost always apply | `.github/copilot-instructions.md` |
| Rule for Java/Python/SQL paths | `.github/instructions/` |
| Specialized engineering/domain expertise | `.github/skills/` |
| Responsibility or review role | `.github/agents/` |
| Explicit repeatable task | `.github/prompts/` |
| Executable verification | `tooling/` |
| Whole-project usage example | `examples/` |
| Human setup/explanation | `docs/` |

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
```

The reason is architectural: **an agent represents responsibility; a skill represents reusable domain capability**. The planner, implementation engineer, test engineer, architecture reviewer, and code reviewer can all apply the migration skill at different phases.

Use `/migrate-oracle-to-postgres` as the explicit prompt entry point when you want to start that workflow.

## Key Skills

- Prompt-Driven Development
- Requirements analysis
- Implementation planning
- Architecture design
- Distributed systems
- API design
- Resilience and degradation
- Observability
- Security
- Compliance engineering
- Testing
- Code review
- Production readiness
- Java/Spring Boot
- Python/FastAPI
- Oracle → PostgreSQL modernization

Each skill owns its references, templates, checklists, or examples instead of depending on parallel root-level taxonomies.

## Validation

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tooling/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python tooling/scripts/validate_repository.py
```

CI runs the same checks.

## Adoption

For another repository, register or distribute the approved agents and skills using the Copilot/IDE mechanism supported by your environment. Keep machine-specific checkout paths in personal IDE settings rather than application source control.

See [Getting Started](docs/getting-started.md) and [Customization Model](docs/customization-model.md).

## Human Review

Agents, skills, prompts, and instructions may accelerate engineering work, but they do not approve requirements, plans, production changes, or architecture decisions on behalf of a human reviewer. Do not claim commands passed unless they were actually run.
