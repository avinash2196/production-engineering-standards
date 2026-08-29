# Implementation Plan: Enforceable Engineering Standards Repository Update


## Status

Completed — historical execution artifact; not active guidance.
**Date:** 2026-07-27
**Approved Plan:** `Plan.md`

## Milestone 1 — Test the Repository Validator First

### Files to create

- `tooling/tests/test_validate_repository.py`

### Test changes

Add standard-library unit tests covering:

- required-path failures
- valid and broken Markdown links
- template-directory link exclusion
- placeholder detection without self-detection
- invalid prompt frontmatter (`mode: agent` and duplicate body metadata)
- prohibited stale references in active documentation

### Success criteria

- Tests fail against the incomplete validator for the intended missing behavior.

## Milestone 2 — Implement and Refactor Repository Validation

### Files to create or update

- `tooling/scripts/validate_repository.py`
- `tooling/scripts/validate-repo-structure.ps1`
- `.github/workflows/ci-validate.yml`

### Exact implementation

- Rename the Python validator consistently to `validate_repository.py`.
- Make validation functions accept a repository root so they are testable.
- Skip intentionally unresolved links under `templates/`.
- Exclude the validator source itself from placeholder scanning.
- Validate prompt frontmatter and stale active-document references.
- Run unit tests before repository validation in CI.

### Refactor

- Centralize path traversal and text-file reading.
- Return deterministic, sorted errors.
- Keep validator dependency-free.

## Milestone 3 — Encode the PDD Lifecycle

### Files to create

- `standards/prompt-driven-development-workflow.md`
- `templates/docs/plan-template.md`
- `templates/docs/implementation-plan-template.md`
- `.github/prompts/create-plan.prompt.md`
- `.github/prompts/create-implementation-plan.prompt.md`
- `.github/prompts/implement-approved-plan.prompt.md`

### Files to update

- `standards/agent-execution.md`
- `.github/copilot-instructions.md`
- `.github/instructions/new-service.instructions.md`
- `README.md`

### Required lifecycle

1. Requirements/context review
2. Plan creation and human review
3. Implementation Plan with exact files, code approach, tests, and exclusions
4. Tests written first and confirmed RED
5. Minimal implementation to GREEN
6. Refactor with tests remaining GREEN
7. Final review and Definition of Done

No phase may silently collapse into another.

## Milestone 4 — Update Prompts, Agents, and Playbooks

### Prompt files

- Fix frontmatter and links in all `.github/prompts/*.prompt.md`.
- Update `scaffold-service`, `generate-tests`, and `refactor-code` to follow the lifecycle.
- Make review findings classify rules as `AUTOMATED`, `REVIEWED`, or `ADVISORY`.

### Agent files

- Update `backend-service-engineer.agent.md`, `test-engineer.agent.md`, and `refactoring-engineer.agent.md`.
- Replace automatic fallback generation with explicit adapter/degradation decisions.

### Playbooks

Update:

- `playbooks/create-new-service.md`
- `playbooks/add-new-endpoint.md`
- `playbooks/fix-bug-safely.md`
- `playbooks/refactor-module.md`
- `playbooks/add-local-adapter-or-degradation-path.md`
- `playbooks/local-dev/run-with-local-adapters.md`

## Milestone 5 — Align Standards and Configuration

### Files to update

- `standards/architecture.md`
- `standards/coding-standards.md`
- `standards/engineering-principles.md`
- `standards/definition-of-done.md`
- `standards/local-adapter-strategy.md`
- `standards/fallback-strategy.md`
- stack configuration and provider files for Java and Python

### Required corrections

- Treat numeric size limits as review signals, not universal failures.
- Require documented failure behavior, not a fallback for every dependency.
- Separate local adapters from production degradation.
- Reject local-only adapters in production.
- Preserve database, Kafka, Redis, storage, and JWT settings in Python.

## Milestone 6 — Documentation Integrity and Evidence

### Files to create

- `docs/enforcement-matrix.md`

### Files to update

- `README.md`
- example READMEs
- internal links throughout active documentation

### Success criteria

- No active documentation claims that Copilot alone enforces standards.
- Every "enforced" rule names an executable mechanism.
- Examples are labeled runnable only when runnable.
- Deleted generator has no remaining references.

## Out of Scope

- Building a complete production microservice generator.
- Implementing every Java/Python cloud adapter.
- Legal or compliance certification.
- Enforcing subjective architecture decisions through brittle static checks.

## Final Verification

Run in order:

```bash
python -m unittest discover -s tooling/tests -p 'test_*.py'
python tooling/scripts/validate_repository.py
```

Then inspect repository status and package the updated source without `.git` history.

## Implementation Result

### RED evidence

- Validator suite initially failed because the completed `validate_repository.py` behavior did not exist.
- Production-adapter selection test initially raised an opaque `ModuleNotFoundError` instead of the planned actionable error.
- Local filesystem traversal test initially failed because `../outside.txt` was accepted.
- Local-adapter activation test initially failed because no warning was emitted.

### GREEN implementation

- Added dependency-free validator and CI wiring.
- Added typed Python adapter selectors and production rejection.
- Added database outbox publisher, JSON-file cache, in-memory adapters, local storage, and environment-secret provider.
- Added actionable errors for production adapters not included in the base template.
- Added local-adapter activation warnings and local-storage path containment.

### Refactoring after GREEN

- Consolidated production-adapter loading in `_load_adapter`.
- Separated local-adapter guidance from production degradation strategy.
- Replaced fixed layer/line-count mandates with evidence-based review guidance.
- Standardized `*_ADAPTER` environment values and Java `adapters.*` property names.
- Rewrote stack and example documentation to state what is executable versus reference-only.

### Final verification commands

```bash
python -m unittest discover -s tooling/tests -p 'test_*.py'
python tooling/scripts/validate_repository.py
PYTHONPATH=stacks/python-fastapi/project-template \
  python -m unittest discover \
  -s stacks/python-fastapi/project-template/tests \
  -p 'test_*.py'
python -m compileall -q tooling/scripts \
  stacks/python-fastapi/project-template/app \
  stacks/python-fastapi/project-template/tests
```

All commands passed in the final working copy.
