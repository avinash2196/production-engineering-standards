# Getting Started

This repository is intended to remain separate from the applications that use it.

The standards repository provides reusable agents, skills, prompts, engineering knowledge, and validation patterns.

The application remains responsible for its own project context, source code, tests, planning artifacts, runtime configuration, and application-specific Copilot instructions.

## 1. Keep the Standards Repository Separate

Do not make every application a Git submodule of this repository by default.

For personal or local use, keep this repository in a stable location and configure the supported Copilot or IDE customization mechanism to discover its agents and skills.

Machine-specific checkout paths belong in personal IDE or user settings.

Do not commit paths such as:

```text
C:\Users\<name>\production-engineering-standards
/Users/<name>/repos/production-engineering-standards
/home/<name>/projects/production-engineering-standards
```

into the adopting application's source control.

## 2. Let the Application Own Its Context

The adopting application should own its own:

```text
.github/copilot-instructions.md
docs/requirements.md                    # or the application's chosen requirements artifact
docs/.ai/Plan.md
docs/.ai/<API-or-external-contract>.md  # when applicable
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
```

Those files describe the current application and current work.

They do not belong in the standards repository.

## 3. Start from the PDD Application Instruction Template

For Copilot, use:

```text
.github/skills/prompt-driven-development/templates/application-copilot-instructions.md
```

as a starter for the adopting application's:

```text
.github/copilot-instructions.md
```

For Claude Code, use the equivalent template instead:

```text
.github/skills/prompt-driven-development/templates/application-claude-instructions.md
```

as a starter for the adopting application's:

```text
CLAUDE.md
```

(repo root). Both templates carry the same PDD workflow and the same no-code-change-without-approval rule — pick the one matching the tool the adopting project actually uses.

Then add only application-specific facts such as:

- runtime and framework versions,
- module or architectural boundaries,
- database and migration approach,
- API compatibility expectations,
- build and verification commands,
- application-specific conventions.

Do not copy the full engineering standards library into the application.

Reusable expertise remains in externally available skills.

## 4. Choose the Correct Primitive

Use the following rule when deciding where new content belongs:

- always-on repository rule → instruction
- path-specific rule → `.github/instructions/`
- specialized expertise → skill
- responsibility → agent
- explicit reusable command → prompt
- executable rule → tooling or tests

Examples:

```text
"Never commit secrets"
    → instruction

"How to design idempotent message processing"
    → distributed-systems skill

"Review this implementation"
    → code-reviewer agent

"Start an Oracle to PostgreSQL migration assessment"
    → migration prompt using the Oracle-to-Postgres skill

"Fail CI if skill frontmatter is invalid"
    → tooling
```

## 5. Start a New PDD Work Item

For a new application or a change whose requirements are not yet captured:

1. `/capture-requirements`
2. resolve all material ambiguity
3. human requirements review
4. `/create-plan` — the Plan decides how many implementation milestones this work needs (see step 8) based on complexity, responsibility boundaries, risk, and independent verifiability; a small cohesive change may need only one, larger work several
5. human Plan review
6. `/create-api-contract` when externally visible behavior must be defined before implementation
7. human contract review
8. for each milestone defined in the Plan, run the Behavior-Changing Milestone Flow (section 6) in sequence
9. final code and production-readiness review as applicable

For an existing application with already-approved requirements, start from the earliest artifact that needs to change.

## 6. Behavior-Changing Milestone Flow

Each milestone the Plan defines runs this flow on its own — a separate Implementation Plan per phase, never one Implementation Plan covering more than one phase.

If `Plan.md` records this milestone's `setup required` as Yes:

1. Create the FOUNDATION Implementation Plan (`/create-implementation-plan`).
2. Human reviews and approves it.
3. Execute only the approved FOUNDATION changes (`/implement-approved-plan`).
4. Verify the FOUNDATION Acceptance / Completion Criteria.
5. Stop.
6. Then proceed to the separate RED Implementation Plan below.

If `setup required` is No, proceed directly to RED.

1. `/create-implementation-plan` for RED
2. human review
3. `/generate-tests`
4. verify valid RED evidence
5. `/create-implementation-plan` for GREEN
6. human review
7. `/implement-approved-plan`
8. verify GREEN
9. create a separate REFACTOR Implementation Plan only when justified
10. `/refactor-code`
11. final review

If the Plan defines more than one milestone, repeat this entire flow for the next milestone before starting Final Review on the whole feature.

The important control is not the command names.

The important control is that:

```text
RED
GREEN
REFACTOR
```

are separate authorization boundaries.

Completing one phase does not authorize the next.

## 7. Adaptive Milestone Decomposition — Illustrative Examples

This section illustrates how the milestone boundaries in section 6 might be chosen for different kinds of work. It is documentation only — the runtime rule lives in the `prompt-driven-development` skill's Adaptive Milestone Decomposition, and `Plan.md` records the actual decision made for a given task, with its rationale.

Possible milestone boundaries include:

- persistence/data access
- domain/service behavior
- API/controller behavior
- validation
- concurrency
- integration
- migration
- infrastructure/configuration

A small, cohesive change (e.g. a single new read-only endpoint reusing existing persistence and validation) may need only one RED/GREEN pair.

A larger change (e.g. a new resource with persistence, validation rules, computed fields, and an HTTP API) is typically decomposed into several sequential RED/GREEN cycles. For requirements that span multiple independently testable architectural layers, prefer separate layer-wise milestones over one feature-wide RED/GREEN cycle — this is the common case for a layered application:

```text
Complex Spring Boot feature

Milestone 1 — Persistence / Repository
  Setup/Foundation — only if genuinely required
  RED
  GREEN
  optional REFACTOR

Milestone 2 — Domain / Service
  Setup/Foundation — only if genuinely required
  RED
  GREEN
  optional REFACTOR

Milestone 3 — API / Controller
  Setup/Foundation — only if genuinely required
  RED
  GREEN
  optional REFACTOR

Milestone 4 — Integration
  Setup/Foundation — only if genuinely required
  RED
  GREEN
  optional REFACTOR
```

This is a common layered decomposition, not a mandatory template. The real rule is independent reviewability, not architectural layering for its own sake — a different system might instead need capability-oriented milestones (e.g. one per business capability), workflow-oriented milestones (e.g. one per user journey), or milestones around a migration step, integration boundary, or concurrency concern. Choose whichever boundary makes each milestone genuinely reviewable and testable on its own. Do not mechanically create one milestone per class or file, and do not force layer boundaries onto an architecture that does not support them.

**Setup/Foundation is conditional, not automatic, for each layer:**

- Most milestones need no setup at all — proceed straight to RED.
- A missing production class, service, repository, controller, method, or interface is never, by itself, a reason for setup — that absence is the expected RED condition (a compilation failure caused by an intentionally absent approved production symbol is valid RED evidence), and creating the real thing is GREEN's job.
- Setup exists only for genuine executable prerequisites that prevent RED from meaningfully running at all — e.g. required build/dependency setup, test framework/infrastructure that doesn't exist yet, required configuration, or a prerequisite contract established by an earlier architectural decision.
- Every setup code change still requires its own approved Implementation Plan and human review, exactly like RED, GREEN, and REFACTOR — setup is never a way to change code without approval.

## 8. Clarification Is a Blocking Gate

When material information is missing, ambiguous, or contradictory:

```text
ASK
 ↓
STOP
 ↓
WAIT FOR USER
```

Do not create or finalize the dependent artifact.

Do not use an Open Questions section as a substitute for required clarification.

## 9. Artifact Authority

Use this authority model:

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

If authoritative artifacts materially conflict, stop and surface the conflict for human review.

Do not silently rewrite one artifact to match another.

## 10. Oracle to PostgreSQL Modernization

For Oracle → PostgreSQL modernization, use:

```text
/migrate-oracle-to-postgres
```

as an explicit workflow entry point when supported.

The migration capability itself lives in:

```text
.github/skills/oracle-to-postgres-modernization/
```

It may be used by multiple responsibility-focused agents during:

- assessment
- planning
- schema conversion
- SQL conversion
- Spring Boot configuration changes
- migration testing
- reconciliation
- performance validation
- cutover planning
- post-migration cleanup

Oracle → PostgreSQL is therefore a skill rather than a dedicated migration agent.

## 11. Where Examples Belong

Do not create placeholder root-level examples simply to demonstrate folder structure.

Skill-specific examples should live with the relevant skill:

```text
.github/skills/<skill-name>/examples/
```

A root-level `examples/` directory should be introduced only when there is a real, runnable whole-project demonstration.

A valid whole-project example should include meaningful source code, tests, build configuration, project-specific instructions, and realistic PDD artifacts.

Until such an example exists, the repository does not need a root `examples/` directory.

## 12. Validate Before Publishing Changes

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tooling/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python tooling/scripts/validate_repository.py
```

Repository validation confirms the customization structure itself.

Application-specific behavior must still be validated inside the adopting application.
