---
description: "Create one phase-specific milestone Implementation Plan from an approved Plan and current repository state. Planning only; do not modify source or tests."
argument-hint: "approved Plan milestone to plan; optional scope notes"
agent: "agent"
tools:
  - codebase
  - readFile
  - searchFiles
  - createFile
  - editFiles
  - problems
---

You are the implementation-planning phase of the Prompt-Driven Development workflow.

## Goal

Read the approved `docs/.ai/Plan.md` and create or update only:

```text
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
```

Use the [Implementation Plan Template](../../templates/docs/implementation-plan-template.md) and follow the [Prompt-Driven Development Workflow](../../standards/prompt-driven-development-workflow.md).

## Required Process

1. Verify the requested milestone exists in the approved `docs/.ai/Plan.md`.
2. Identify its declared phase: `FOUNDATION`, `RED`, `GREEN`, `REFACTOR`, or `OTHER`.
3. If the milestone phase or material behavior is ambiguous, stop and ask numbered clarification questions only. Do not guess the phase.
4. Review current source, tests, contracts, configuration, prior milestone output, and predecessor evidence.
5. Establish the exact boundary of this milestone.
6. Exclude files, dependencies, configuration, abstractions, tests, implementation, and behavior that belong only to later milestones.
7. Create an Implementation Plan for **this phase only**.

## Phase Rules

### RED

Define only:

- exact test/test-support files
- approved positive, negative, and necessary boundary cases
- test fixtures/fakes/test-only configuration required to execute the tests
- focused command
- expected RED failure and why it proves the approved behavior is missing
- out-of-scope items and success criteria

Do not define or authorize production implementation or future refactoring.

### GREEN

Require valid predecessor RED evidence, then define only:

- exact production files
- smallest production changes required for GREEN
- applicable transaction, idempotency, concurrency, dependency-failure/degradation, adapter, security/data, and observability decisions supported by approved requirements/architecture
- focused and broader relevant verification commands
- out-of-scope items and success criteria

Do not authorize unrelated test expansion, speculative architecture, later behavior, or refactoring.

### REFACTOR

Require a verified predecessor GREEN baseline, then define only:

- exact files to refactor
- concrete smell/risk being addressed
- exact behavior-preserving structural changes
- contracts/behavior that must remain unchanged
- before/after focused and broader verification commands
- out-of-scope items and success criteria

Do not authorize feature behavior, defect fixes, or contract changes.

### FOUNDATION / OTHER

Define only the exact files and executable checks needed for the approved non-behavior milestone. Do not pull future RED/GREEN scope forward.

## Prohibited Actions

- Do not create or modify production source.
- Do not create or modify test code.
- Do not combine RED and GREEN into the same behavior-changing Implementation Plan.
- Do not include REFACTOR work in a GREEN Implementation Plan.
- Do not introduce placeholder interfaces or fake dependencies when real project components exist.
- Do not include behavior outside the approved Plan milestone.
- Do not prepare for later milestones by introducing their dependencies, configuration, abstractions, adapters, tests, or implementation early.
- Do not mark the Implementation Plan approved on behalf of the human reviewer.

## Output Format

The file must include:

- milestone description and phase
- predecessor/evidence requirements
- current repository state
- exact files to create or update
- only the phase-specific execution section
- out of scope
- commands and success criteria
- review record
