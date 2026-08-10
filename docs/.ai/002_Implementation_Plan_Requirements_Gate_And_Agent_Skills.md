# Implementation Plan — Requirements Gate and Agent Skills

## Status

Ready for owner review.

## Milestone Description

Implement the final requirements-analysis and Agent Skill hardening defined by `docs/.ai/Plan.md`. Preserve the existing PDD/TDD lifecycle and already-correct Java/Python implementation guidance.

## Files to Create

- `.github/skills/requirements-analysis/SKILL.md`
- `.github/skills/code-review/SKILL.md`
- `.github/prompts/review-requirements.prompt.md`
- `docs/.ai/002_Implementation_Plan_Requirements_Gate_And_Agent_Skills.md`
- `.gitignore` if not already present

## Files to Update

- `.github/copilot-instructions.md`
- `.github/prompts/create-plan.prompt.md`
- `.github/prompts/review-code.prompt.md`
- `standards/questioning-policy.md`
- `agents/backend-service-builder.md`
- `tooling/tests/test_validate_repository.py`
- `tooling/scripts/validate_repository.py`
- `README.md`
- `docs/enforcement-matrix.md`
- `docs/.ai/Plan.md`

## Test-First / Executable Check Sequence

### RED — Skill Validation Tests

Update `tooling/tests/test_validate_repository.py` before validator implementation with tests proving:

1. a valid `SKILL.md` is accepted;
2. a skill directory without `SKILL.md` is rejected;
3. `name` and `description` are required;
4. skill `name` must match its directory;
5. skill names use lowercase letters, numbers, and hyphens;
6. malformed list syntax in skill frontmatter is rejected.

Expected RED before validator implementation: the validator module has no `validate_skill_files` function and the new tests fail.

Also retain the existing prompt-frontmatter regression test proving `* codebase` is invalid.

### GREEN — Validator

Update `tooling/scripts/validate_repository.py` to:

- require `.github/skills` plus the two baseline skills;
- validate immediate skill directories;
- require `SKILL.md`;
- reuse the repository's dependency-free supported-frontmatter parser;
- require non-empty `name` and `description`;
- require `name` to match the directory and use lowercase/hyphen form;
- include skill validation in `validate_repository`.

Do not add a third-party YAML dependency or claim generic YAML validation.

### Requirements Workflow Changes

Add the requirements-analysis skill and `/review-requirements` prompt. Update always-on instructions, `/create-plan`, the questioning policy, and backend-service-builder so they share this contract:

- classify evidence as `EXPLICIT`, `REPOSITORY-CONFIRMED`, `UNRESOLVED`, or `NOT REQUIRED YET`;
- use only explicit/repository-confirmed facts for planning;
- material `UNRESOLVED` items cause numbered clarification questions and stop Plan creation;
- do not use common architecture practices, framework defaults, industry assumptions, or prior examples to fill gaps;
- ask the smallest set of current-boundary questions;
- defer later-milestone decisions until they become material.

### Review Changes

Add the `code-review` skill as a concise wrapper around the canonical reviewer behavior. Correct only the malformed list markers in `.github/prompts/review-code.prompt.md`; do not rewrite the already-correct review body.

### Documentation

Update README and the enforcement matrix to document repository Agent Skills and executable skill validation accurately.

## Verification Commands

Run after applying to the live repository:

```bash
python -m unittest discover -s tooling/tests -p 'test_*.py'
python tooling/scripts/validate_repository.py
```

Then run the already-required stack/template checks from the repository README. No Java/Python service behavior is changed by this milestone.

## Refactoring Boundary

No new PDD phase, architecture layer, compliance requirement, production adapter, cloud dependency, or healthcare behavior may be introduced. Keep skills concise and make canonical standards/prompts the source of truth.

## Out of Scope

- Healthcare platform implementation.
- Choosing HIPAA applicability or PHI handling before project requirements establish them.
- Adding Kafka, Redis, database, object-storage, observability, security, or deployment dependencies.
- Rewriting already-correct production-readiness or stack templates.

## Success Criteria

- New validator tests pass.
- Repository validator accepts valid skills and rejects malformed/misnamed skills.
- `review-code.prompt.md` passes the existing prompt-frontmatter validator.
- Requirements-analysis behavior is consistent across skill, prompt, always-on instructions, policy, and service builder.
- Planning stops instead of guessing when a material decision is unresolved.
- The public PDD lifecycle remains unchanged and TDD execution remains RED → minimal GREEN → refactor.
