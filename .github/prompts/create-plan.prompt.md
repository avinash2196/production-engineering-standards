---
description: "Create or update docs/.ai/Plan.md from requirements and current repository state. Planning only; do not write tests or implementation code."
argument-hint: "requirement, issue, or change request; optional files to review"
agent: "agent"
tools:
  - codebase
  - readFile
  - searchFiles
  - createFile
  - editFiles
  - problems
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
2. Review the current repository state, relevant contracts, tests, configuration, and standards.
3. If a material requirement is unclear, ask numbered clarification questions only and do not create the Plan.
4. Otherwise create a practical milestone-based Plan.
5. Keep milestones small and independently reviewable.
6. Describe milestones as delivery outcomes, not RED/GREEN execution phases.
7. Do not pull later-milestone work into an earlier milestone merely to prepare for future implementation.

## Plan Content

Include:

- objective and business/engineering outcome
- current-state summary
- explicit in-scope and out-of-scope items
- requirements and constraints supported by the input
- milestone order
- dependencies and risks
- success criteria

## Prohibited Actions

- Do not create an Implementation Plan.
- Do not write or modify production code.
- Do not write or modify tests.
- Do not invent endpoints, DTOs, database tables, packages, infrastructure, security controls, or non-functional requirements not supported by the input.
- Do not mark the Plan approved on behalf of the human reviewer.

## Output

After creating the file, summarize:

- the milestones
- any assumptions explicitly supported by current repository evidence
- questions or decisions the reviewer must resolve
