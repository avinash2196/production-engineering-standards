# Implementation Plan — Final Consistency Hardening

## Status

Ready for owner review.

## Milestone Description

Implement the approved final consistency-hardening plan across workflow guidance, reviewers, executable validation, language templates, and public-repository hygiene. Preserve the existing standards philosophy and avoid introducing new requirements.

## Files to Create

- `.gitignore`
- `docs/.ai/Plan.md`
- `docs/.ai/001_Implementation_Plan_Final_Consistency_Hardening.md`

## Files to Replace or Update

- `.github/prompts/scaffold-service.prompt.md`
- `.github/prompts/review-production-readiness.prompt.md`
- `.github/agents/backend-service-builder.agent.md`
- `.github/agents/code-reviewer.agent.md`
- `.github/agents/production-readiness-reviewer.agent.md`
- `standards/agent-execution.md`
- `tooling/scripts/validate_repository.py`
- `tooling/tests/test_validate_repository.py`
- `stacks/java-springboot/README.md`
- `stacks/java-springboot/java-spring.md`
- `stacks/java-springboot/project-template/pom.xml`
- `stacks/java-springboot/project-template/src/main/resources/application.yml`
- `stacks/java-springboot/project-template/src/main/resources/application-local.yml`
- `stacks/python-fastapi/README.md`
- `stacks/python-fastapi/project-template/pyproject.toml`
- `stacks/python-fastapi/project-template/app/main.py`

## Files / Artifacts to Remove

- `.ai/Plan_to_upgrade.md` after this canonical plan replaces it
- `.idea/`
- `stacks/python-fastapi/project-template/.coverage`
- all committed `__pycache__/` directories and `*.pyc` files

## Test-First / Validation Sequence

### 1. Validator RED

Add validator tests before changing validator implementation:

- malformed list marker such as `* codebase` is rejected;
- supported multiline `tools` list is accepted;
- supported inline `tools` list is accepted;
- scalar `tools` value is rejected;
- duplicate frontmatter keys are rejected;
- unexpected indentation is rejected;
- existing deprecated `mode` and duplicate body metadata checks remain covered.

Expected RED before validator implementation: one or more new malformed-frontmatter tests fail because the existing validator only extracts top-level keys.

### 2. Validator GREEN

Update `validate_repository.py` with a dependency-free parser for the repository-supported prompt-frontmatter subset: top-level scalar fields plus list-valued `tools`. Do not claim general YAML support.

Run:

```bash
python -m unittest discover -s tooling/tests -p 'test_*.py'
python tooling/scripts/validate_repository.py
```

### 3. Workflow / Reviewer Changes

Replace the affected agent and prompt files so that:

- milestones are delivery outcomes;
- each implementation milestone contains RED -> GREEN -> Refactor;
- review applies only relevant standards;
- findings use concrete evidence and governing standards/contracts/plans when they exist;
- production readiness evaluates applicability rather than requiring every mechanism;
- HIPAA/PHI review requires explicit context;
- read-before-write means modified files plus enough adjacent context, not literally the entire repository.

Validation: repository link and prompt validation must remain GREEN.

### 4. Java Template Changes

Replace the Java POM with a transport-neutral Spring Boot foundation plus test support. Remove preloaded JPA/Postgres/Flyway/Kafka/Redis/Security/OAuth2/OpenTelemetry/S3/Pact/Testcontainers dependencies from the base. Add those only through an approved service milestone.

Replace base YAML configuration with service name/port/graceful-shutdown only; local profile must not choose adapters that the service has not selected.

Validation after applying to the live repository:

```bash
mvn -f stacks/java-springboot/project-template/pom.xml test
```

If the source-free template intentionally does not execute a full Spring Boot package, validate the Maven model/test harness rather than inventing application source.

### 5. Python Template Changes

Remove production Kafka/Redis/S3 SDKs and always-on OpenTelemetry/Prometheus wiring from the base template. Retain only dependencies required by the executable reference behavior and local database-backed adapter. Keep production adapters dynamically absent until an approved milestone implements them.

Validation after applying to the live repository:

```bash
PYTHONPATH=stacks/python-fastapi/project-template \
  python -m unittest discover \
  -s stacks/python-fastapi/project-template/tests \
  -p 'test_*.py'
```

### 6. Hygiene

Add `.gitignore`, remove tracked IDE/cache/coverage artifacts, and remove the superseded root `.ai/Plan_to_upgrade.md`.

## Refactoring Boundary

No new standards, patterns, adapters, compliance rules, or architecture layers. Wording changes are limited to resolving contradictions and making applicability explicit.

## Out of Scope

- Healthcare-platform feature code.
- Production adapter implementations.
- New CI systems or third-party linters.
- Dependency upgrades except the Java Spring Boot 3.x baseline used by the minimal Java template.
- Rewriting already-consistent standards.

## Success Criteria

- Validator unit tests pass.
- Repository validator passes on the live repository.
- Java base no longer preloads unrelated capabilities.
- Python base no longer preloads absent production adapters or always-on metrics/tracing.
- Service builder and scaffold prompt agree with the core milestone model.
- General and production-readiness reviewers use risk/applicability-based review.
- No generated IDE/cache/coverage artifacts remain tracked.
- No unrelated files are modified.
