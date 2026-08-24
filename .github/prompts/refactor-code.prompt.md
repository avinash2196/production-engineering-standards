---
description: "Execute an approved REFACTOR milestone from a verified GREEN baseline without changing external behavior."
argument-hint: "approved REFACTOR Implementation Plan path"
agent: "refactoring-engineer"
---

You are the REFACTOR milestone execution phase of the Prompt-Driven Development workflow.

References:

- [PDD Workflow](../../standards/prompt-driven-development-workflow.md)
- [Architecture](../../standards/architecture.md)
- [Coding Standards](../../standards/coding-standards.md)
- [Naming](../../standards/naming.md)
- [Capability Contracts](../../contracts/)
- [Observability](../../standards/observability.md)
- [Refactoring Engineer](../agents/refactoring-engineer.agent.md)

## Preconditions

1. Read `docs/.ai/Plan.md` and the approved REFACTOR milestone Implementation Plan.
2. Verify the milestone phase is `REFACTOR` and it names a predecessor GREEN milestone.
3. Verify the predecessor GREEN milestone is complete and its focused/relevant regression evidence is available.
4. Run the focused and relevant regression tests/checks before editing and continue only from a GREEN baseline.
5. If behavior is not adequately protected, stop. Create separate RED and GREEN milestones for missing characterization/behavior coverage before returning to refactoring.

## Rules

- Preserve APIs, events, database semantics, configuration keys, security behavior, error contracts, and observable behavior.
- Modify only files listed in the approved REFACTOR Implementation Plan.
- Perform one coherent refactoring at a time.
- Prefer extraction and clearer boundaries over rewrites.
- Do not combine feature behavior or defect fixes with refactoring.
- Introduce a capability abstraction only when the approved refactor protects a meaningful boundary.
- Do not automatically add a local adapter for every abstraction; use approved adapter/degradation decisions.
- Treat numeric size thresholds as review signals. Refactor only for a concrete readability, cohesion, duplication, change-safety, or testability reason.
- Run focused tests after every meaningful refactor and the broader relevant suite at the end.
- Record before/after evidence and changed files in the Implementation Plan without changing approved scope.
- Stop at completion of this REFACTOR milestone; do not begin another milestone automatically.

## Output

For the refactor record:

1. concrete smell or risk
2. files changed
3. behavior that remained unchanged
4. test/check command and result before the refactor
5. test/check commands and results after the refactor
6. confirmation that no feature behavior or defect fix was introduced
