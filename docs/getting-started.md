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

Use:

```text
.github/skills/prompt-driven-development/templates/application-copilot-instructions.md
```

as a starter for the adopting application's:

```text
.github/copilot-instructions.md
```

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
4. `/create-plan`
5. human Plan review
6. `/create-api-contract` when externally visible behavior must be defined before implementation
7. human contract review
8. create milestone-specific Implementation Plans
9. execute RED, GREEN, and optional REFACTOR as separate authorization phases
10. final code and production-readiness review as applicable

For an existing application with already-approved requirements, start from the earliest artifact that needs to change.

## 6. Behavior-Changing Milestone Flow

A typical behavior-changing milestone is:

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

The important control is not the command names.

The important control is that:

```text
RED
GREEN
REFACTOR
```

are separate authorization boundaries.

Completing one phase does not authorize the next.

## 7. Clarification Is a Blocking Gate

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

## 8. Artifact Authority

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

## 9. Oracle to PostgreSQL Modernization

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

## 10. Where Examples Belong

Do not create placeholder root-level examples simply to demonstrate folder structure.

Skill-specific examples should live with the relevant skill:

```text
.github/skills/<skill-name>/examples/
```

A root-level `examples/` directory should be introduced only when there is a real, runnable whole-project demonstration.

A valid whole-project example should include meaningful source code, tests, build configuration, project-specific instructions, and realistic PDD artifacts.

Until such an example exists, the repository does not need a root `examples/` directory.

## 11. Validate Before Publishing Changes

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tooling/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python tooling/scripts/validate_repository.py
```

Repository validation confirms the customization structure itself.

Application-specific behavior must still be validated inside the adopting application.
