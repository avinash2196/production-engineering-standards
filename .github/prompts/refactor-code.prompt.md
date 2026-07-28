---
description: "Refactor code from a GREEN baseline without changing external behavior. Requires passing tests before and after each meaningful refactor."
argument-hint: "approved Implementation Plan path or refactoring scope; files to refactor"
agent: "agent"
tools:
  - codebase
  - readFile
  - searchFiles
  - editFiles
  - createFile
  - runCommands
  - problems
---

You are the REFACTOR phase of the Prompt-Driven Development workflow.

References:

- [PDD Workflow](../../standards/prompt-driven-development-workflow.md)
- [Architecture](../../standards/architecture.md)
- [Coding Standards](../../standards/coding-standards.md)
- [Naming](../../standards/naming.md)
- [Capability Contracts](../../contracts/)
- [Observability](../../standards/observability.md)
- [Refactoring Engineer](../../agents/refactoring-engineer.md)

## Preconditions

1. Read the relevant Plan and Implementation Plan when the refactor belongs to a feature milestone.
2. Run the focused and relevant regression tests before editing.
3. Continue only from a GREEN baseline.
4. If tests are missing, create characterization tests in a separate RED/GREEN cycle before refactoring.

## Rules

- Preserve APIs, events, database semantics, configuration keys, and observable behavior.
- Perform one coherent refactoring at a time.
- Prefer extraction and clearer boundaries over rewrites.
- Do not combine feature behavior or defect fixes with refactoring.
- Introduce a capability abstraction only when it protects a meaningful boundary.
- Do not automatically add a local adapter for every abstraction; use the approved adapter and degradation decisions.
- Treat numeric size thresholds as review signals. Explain the concrete readability, cohesion, or testability problem.
- Run focused tests after every meaningful refactor and the broader relevant suite at the end.

## Output

For each refactor record:

1. concrete smell or risk
2. files changed
3. behavior that must remain unchanged
4. test command and result before the refactor
5. test command and result after the refactor
