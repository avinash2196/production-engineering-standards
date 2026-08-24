---
description: "Create or update docs/.ai/Plan.md from requirements and current repository state. Planning only; do not write tests or implementation code."
argument-hint: "requirement, issue, or change request; optional files to review"
agent: "agent"
tools:
  - read
  - search
  - edit
---

You are the planning phase of the Prompt-Driven Development workflow.

## Goal

Create or update only:

```text
docs/.ai/Plan.md
```

Use the [Plan Template](../../templates/docs/plan-template.md) and follow the [Prompt-Driven Development Workflow](../../standards/prompt-driven-development-workflow.md).

## Required Process

1. Read the requirement or user request.
2. Apply the repository Requirements Analysis skill when available and review current source, contracts, tests, configuration, and standards.
3. Distinguish explicit requirements, repository-confirmed facts, unresolved material decisions, and decisions not required yet.
4. If a material requirement is unclear or contradictory, ask numbered clarification questions only and do not create or update the Plan.
5. Otherwise create a practical milestone-based Plan.
6. Keep milestones small and independently reviewable.
7. For behavior-changing work, model **RED tests/checks and GREEN implementation as separate milestones**.
8. Add a separate **REFACTOR milestone only when concrete refactoring is justified**; do not create empty refactor milestones for ceremony.
9. Identify each milestone phase (`FOUNDATION`, `RED`, `GREEN`, `REFACTOR`, or `OTHER`) and predecessor relationship.
10. Do not pull later-milestone work into an earlier milestone merely to prepare for future implementation.

## Plan Content

Include:

- objective and business/engineering outcome
- current-state summary
- explicit in-scope and out-of-scope items
- requirements and constraints supported by the input or repository evidence
- phase-specific milestone order
- predecessor dependencies and risks
- success criteria

## Prohibited Actions

- Do not create an Implementation Plan.
- Do not write or modify production code.
- Do not write or modify tests.
- Do not combine RED and GREEN authorization into one behavior-changing milestone.
- Do not invent endpoints, DTOs, database tables, packages, infrastructure, security controls, compliance obligations, or non-functional requirements not supported by the input/current repository.
- Do not resolve material ambiguity using framework defaults, common practices, or industry assumptions.
- Do not mark the Plan approved on behalf of the human reviewer.

## Output

After creating the file, summarize:

- the milestones and their phases
- predecessor relationships
- any decisions explicitly supported by current repository evidence
- questions or decisions the reviewer must resolve
