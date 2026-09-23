# Production Engineering Standards

A Copilot- and Claude Code-native engineering standards repository for production-oriented Java, Python, distributed-system, and database-modernization work.

The repository separates five concerns:

- **Instructions** — standing rules that should apply automatically.
- **Skills** — reusable engineering and domain knowledge loaded when relevant.
- **Agents** — responsibility-focused roles for planning, implementation, testing, refactoring, and review.
- **Prompts** — explicit entry points for repeatable Prompt-Driven Development workflows.
- **Tooling** — executable repository checks. Guidance is not described as enforcement unless a check can actually fail.

## Core Development Lifecycle

For work that adopts this repository's Prompt-Driven Development model:

```text
Requirements
→ Plan
→ Human Review
→ API / External Contract when applicable
→ Human Review
→ FOR EACH SEQUENCE OF IMPLEMENTATION MILESTONES:
    optional FOUNDATION milestone: Implementation Plan → Human Review → execution → Verification
    RED milestone: Implementation Plan → Human Review → execution → Verification
    → GREEN milestone: Implementation Plan → Human Review → execution → Verification
    → optional REFACTOR milestone: Implementation Plan → Human Review → execution → Verification
→ Final Review
```

Each Implementation Plan authorizes exactly one repository-changing milestone — never RED and GREEN together, and never more than one milestone. FOUNDATION when required, RED, GREEN, and REFACTOR are each separate milestones and separate authorization boundaries. Completing one milestone does not automatically authorize the next.

How many milestones a piece of work needs is decided in `Plan.md`, based on complexity, responsibility boundaries, risk, and independent verifiability — a small cohesive change may use a single RED milestone / GREEN milestone pair, while larger work is decomposed into multiple sequential milestone sequences, for example: `Persistence RED → Persistence GREEN → Service RED → Service GREEN → API RED → API GREEN`. See the `prompt-driven-development` skill's Adaptive Milestone Decomposition.

Material ambiguity is also a blocking boundary:

> **Material ambiguity → Ask → Stop → Wait for human clarification**

## Repository Structure

**Root-level configuration files:**

- `CLAUDE.md` — Claude Code repository-wide rules (equivalent to `.github/copilot-instructions.md` plus path-scoped rules from `.github/instructions/`)
- `.github/copilot-instructions.md` — GitHub Copilot repository-wide rules
- `CLAUDE.md` and `.claude/` directory are loaded automatically by Claude Code when this repo is opened.

**Directory structure:**

```text
.github/
  copilot-instructions.md
  instructions/            Path-scoped standing rules
  agents/                  Responsibility-focused custom agents (GitHub Copilot format)
  skills/                  Domain knowledge + reusable engineering capabilities
  prompts/                 Explicit reusable workflow entry points
  workflows/               Repository validation CI

.claude/
  agents/                  Same responsibility-focused agents, Claude Code format
  skills/                  Same domain knowledge, Claude Code format
  commands/                Same workflow entry points, Claude Code format

plugin/
  .claude-plugin/
    plugin.json            Installable Claude Code plugin manifest
  agents/                  Mirror of .claude/agents/, packaged for distribution
  skills/                  Mirror of .claude/skills/, packaged for distribution
  commands/                Mirror of .claude/commands/, packaged for distribution

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

| Need | Copilot (GitHub) | Claude Code |
| --- | --- | --- |
| Rule that should almost always apply | `.github/copilot-instructions.md` | `CLAUDE.md` |
| Rule for Java, Python, SQL, or specific paths | `.github/instructions/` | `CLAUDE.md` (path sections) |
| Specialized engineering or domain expertise | `.github/skills/` | `.claude/skills/` |
| Responsibility or review role | `.github/agents/` | `.claude/agents/` |
| Explicit repeatable task | `.github/prompts/` | `.claude/commands/` |
| Executable verification | `tooling/` | `tooling/` |
| Human setup and repository explanation | `docs/` | `docs/` |

A simple way to think about the model is:

> **Instructions = rules**  
> **Skills = knowledge and capability**  
> **Agents = responsibility**  
> **Prompts = explicit workflow entry points**  
> **Tooling = enforcement**

## Using with Claude Code

The repository provides three parallel pieces for Claude Code:

**`.claude/` directory** — Drop-in project configuration automatically loaded when this repository (or any adopting project that includes it) is opened in Claude Code. No installation step required.

**`plugin/` directory** — Packages the same skills, agents, and commands as an installable Claude Code plugin. The repository root also carries `.claude-plugin/marketplace.json`, which registers this repo itself as a Claude Code plugin marketplace with `plugin/` as its one entry.

Validate the plugin manifest:

```bash
claude plugin validate ./plugin
```

Try it ad hoc, for a single session only (must be passed every time you launch `claude`):

```bash
claude --plugin-dir ./plugin
```

Install it persistently, so it loads automatically in every future Claude Code session (`claude plugin install` takes a `<plugin>@<marketplace>` name, not a bare path — it always needs a marketplace registered first, even a local one):

```bash
# From a local checkout of this repo
claude plugin marketplace add ./
claude plugin install production-engineering-standards@pes-marketplace --scope user

# Or directly from GitHub, with no local checkout needed
claude plugin marketplace add avinash2196/production-engineering-standards
claude plugin install production-engineering-standards@pes-marketplace --scope user
```

`--scope user` makes the plugin available in every project on the current machine; use `--scope project` or `--scope local` to limit it to one repo. When installed, skills, agents, and commands are namespaced as `/production-engineering-standards:<name>` (e.g., `/production-engineering-standards:create-plan`, `/production-engineering-standards:code-review`).

**`.claude/` and `plugin/` as translations** — Both directories contain translations of `.github/` content into Claude Code's format. They are kept in sync manually; `.github/` remains the source of truth for GitHub Copilot. When an adopting project copies in this standards repository:

- Copilot pulls instructions and skills from `.github/`
- Claude Code pulls the same content from `.claude/` and `CLAUDE.md`
- Both tools load the same engineering standards, expressed in their native formats

## Prompt-Driven Development

The repository preserves the controlled development lifecycle described above under "Core Development Lifecycle" — each milestone (optional FOUNDATION, RED, GREEN, optional REFACTOR) gets its own Implementation Plan and its own Human Review gate, and a capability or layer may need a sequence of several such milestones, as `Plan.md` defines.

The separation matters because requirements, planning, contract definition, testing, implementation, and refactoring represent different authorization boundaries.

A single end-to-end request does not automatically remove those boundaries.

### Artifact authority

PDD artifacts have distinct responsibilities:

```text
Requirements
    ↓
Plan
    ↓
API / External Contract when applicable
    ↓
Milestone Implementation Plan
    ↓
Tests / Checks
    ↓
Production Implementation
```

Do not silently reconcile material conflicts between approved artifacts.

Stop and surface conflicts for human review.

### Scope control

Engineering standards are a review and design lens, not authorization to invent requirements or expand approved scope.

Do not introduce additional architecture, observability, resilience, security features, infrastructure, dependencies, or other non-functional work unless approved scope requires it.

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

Examples include:

- requirements analysis
- Prompt-Driven Development
- architecture design
- distributed systems
- API design
- testing
- resilience and degradation
- observability
- security
- compliance engineering
- production readiness
- Java and Spring Boot
- Python and FastAPI
- Oracle to PostgreSQL modernization

## Agents as Responsibilities

Agents own durable responsibilities such as:

- planner
- test engineer
- implementation engineer
- refactoring engineer
- code reviewer
- architecture reviewer
- production-readiness reviewer

A specialized topic does not automatically require a dedicated agent.

For example, Oracle → PostgreSQL is reusable expertise used by planning, implementation, testing, and review, so it remains a skill.

## Adopting the Standards Repository

An application using these standards should remain its own repository.

The application owns:

```text
.github/copilot-instructions.md (Copilot) or CLAUDE.md (Claude Code)
requirements
docs/.ai/Plan.md
docs/.ai/<API-or-external-contract>.md
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
source code
tests
build configuration
application-specific CI
```

Use whichever template matches the adopting application's tool:

```text
.github/skills/prompt-driven-development/templates/application-copilot-instructions.md  (→ .github/copilot-instructions.md)
.github/skills/prompt-driven-development/templates/application-claude-instructions.md   (→ CLAUDE.md)
```

as a starter for the adopting application's persistent PDD rules — both carry the same workflow and the same no-code-change-without-approval rule.

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

- [Getting Started](docs/getting-started.md)
- [Customization Model](docs/customization-model.md)

## Oracle to PostgreSQL Modernization

Oracle → PostgreSQL is modeled as a **skill**, not a standalone agent:

```text
.github/skills/oracle-to-postgres-modernization/
  SKILL.md
  references/
  templates/
  examples/
```

Use:

```text
/migrate-oracle-to-postgres
```

when an explicit workflow entry point is useful.

## Validation

**Python repository validation:**

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tooling/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python tooling/scripts/validate_repository.py
```

CI runs the same repository-level checks via `.github/workflows/validate.yml`.

**Claude Code plugin validation:**

```bash
claude plugin validate ./plugin
```

This validates the plugin manifest and subagent/command/skill structure. Note: `claude plugin validate` is a separate check from the Python validators above and is not currently run in CI — consider adding it to `.github/workflows/validate.yml` in a future update.

Application-specific enforcement such as:

- unit and integration tests
- architecture tests
- migration tests
- dependency scanning
- secret scanning
- database compatibility checks
- performance tests

belongs in the adopting application.

## Human Review

Agents, skills, prompts, and instructions may accelerate engineering work, but they do not approve requirements, plans, contracts, architecture decisions, or production changes on behalf of a human reviewer.

Do not claim that tests, validators, builds, migrations, or commands passed unless they were actually executed or the result was explicitly supplied.
