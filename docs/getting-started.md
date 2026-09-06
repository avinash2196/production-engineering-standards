# Getting Started

## 1. Keep the standards repository separate

Do not make every application a Git submodule of this repository by default.

For personal/local use, keep this repository in a stable location and configure the supported Copilot/IDE customization mechanism to discover its agents and skills. Store the machine-specific path in personal IDE settings.

## 2. Let the application own its task artifacts

The adopting application should own:

```text
docs/.ai/Plan.md
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
```

Those are task-specific artifacts and do not belong in this standards repository.

## 3. Choose the correct primitive

- always-on rule → instruction
- specialized expertise → skill
- responsibility → agent
- explicit reusable command → prompt
- executable rule → tooling/test

## 4. Start a change

A typical behavior-changing flow is:

1. `/review-requirements`
2. `/create-plan`
3. human Plan review
4. `/create-implementation-plan` for RED
5. human review
6. `/generate-tests`
7. verify RED
8. `/create-implementation-plan` for GREEN
9. human review
10. `/implement-approved-plan`
11. verify GREEN
12. optional separately approved REFACTOR
13. `/review-code`
14. `/review-production-readiness` when applicable

For Oracle → PostgreSQL modernization, start with `/migrate-oracle-to-postgres`.
