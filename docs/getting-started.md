# Getting Started

This repository is intended to remain separate from the applications that use it.

The standards repository provides reusable agents, skills, prompts, engineering knowledge, and validation patterns.

The application remains responsible for its own project context, source code, tests, planning artifacts, and runtime configuration.

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
docs/.ai/Plan.md
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
```

Those files describe the current application and current work.

They do not belong in the standards repository.

## 3. Keep Application Instructions Project-Specific

The application's `.github/copilot-instructions.md` should contain stable facts and rules about that application.

It should not duplicate the full engineering standards library.

For example:

```text
# Application Context

This repository is a Java 21 / Spring Boot application.

## Architecture

- Keep business logic outside controllers.
- Preserve current module boundaries unless an approved Plan changes them.
- Access external dependencies through explicit adapters.
- Do not introduce a new service or distributed boundary without an approved architecture decision.

## Persistence

- PostgreSQL is the production database.
- Schema changes use Flyway.
- Do not rely on Hibernate auto-DDL in production.
- Database-specific SQL must be documented and tested.

## API

- Preserve existing API compatibility unless explicitly approved.
- Validate request boundaries.
- Keep API contracts separate from persistence entities.
- Use the application's established error-response model.

## Testing

- Behavior-changing work follows RED → GREEN → optional REFACTOR.
- Unit tests cover business behavior.
- Integration tests cover important persistence and infrastructure boundaries.
- Database-specific behavior must be tested against PostgreSQL when relevant.

## Verification

Run:

./mvnw test
./mvnw verify

Do not claim verification passed unless these commands were actually run.

## External Engineering Standards

Reusable engineering knowledge, review guidance, and specialist capabilities come from the externally registered production-engineering-standards agents and skills.

Do not copy those standards into this repository unless the application intentionally owns a local override.

## PDD Artifacts

Task-specific planning artifacts belong under:

docs/.ai/Plan.md
docs/.ai/NNN_Implementation_Plan_<Milestone>.md

Human review is required between authorization phases.
```

The exact content will vary by application.

The important point is that the application instruction file describes **this application**, while reusable engineering expertise remains in skills.

## 4. Choose the Correct Primitive

Use the following rule when deciding where new content belongs:

* always-on repository rule → instruction
* path-specific rule → `.github/instructions/`
* specialized expertise → skill
* responsibility → agent
* explicit reusable command → prompt
* executable rule → tooling or tests

For example:

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

## 5. Start a Behavior-Changing Work Item

A typical flow is:

1. `/review-requirements`
2. resolve material ambiguity
3. `/create-plan`
4. human Plan review
5. `/create-implementation-plan` for RED
6. human review
7. `/generate-tests`
8. verify RED
9. `/create-implementation-plan` for GREEN
10. human review
11. `/implement-approved-plan`
12. verify GREEN
13. create a separate REFACTOR milestone only when justified
14. `/review-code`
15. `/review-production-readiness` when applicable

The important control is not the command names.

The important control is that:

```text
RED
GREEN
REFACTOR
```

are separate authorization boundaries for behavior-changing work.

## 6. Oracle to PostgreSQL Modernization

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

* assessment
* planning
* schema conversion
* SQL conversion
* Spring Boot configuration changes
* migration testing
* reconciliation
* performance validation
* cutover planning
* post-migration cleanup

Oracle → PostgreSQL is therefore a skill rather than a dedicated migration agent.

## 7. Where Examples Belong

Do not create placeholder root-level examples simply to demonstrate folder structure.

Skill-specific examples should live with the relevant skill:

```text
.github/skills/<skill-name>/examples/
```

A root-level `examples/` directory should be introduced only when there is a real, runnable whole-project demonstration.

A valid whole-project example should include meaningful source code, tests, build configuration, project-specific instructions, and realistic PDD artifacts.

Until such an example exists, the repository does not need a root `examples/` directory.

## 8. Validate Before Publishing Changes

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tooling/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python tooling/scripts/validate_repository.py
```

Repository validation confirms the customization structure itself.

Application-specific behavior must still be validated inside the adopting application.
