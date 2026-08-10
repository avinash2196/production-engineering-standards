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

Use the [Plan Template](../../templates/docs/plan-template.md), follow the [Prompt-Driven Development Workflow](../../standards/prompt-driven-development-workflow.md), and apply the [Requirements Analysis Skill](../skills/requirements-analysis/SKILL.md) before planning.

## Required Process

1. Read the requirement or user request.
2. Review the current repository state, relevant contracts, tests, configuration, and standards.
3. Classify planning inputs using the Requirements Analysis Skill: `EXPLICIT`, `REPOSITORY-CONFIRMED`, `UNRESOLVED`, or `NOT REQUIRED YET`.
4. If an `UNRESOLVED` item materially affects the current Plan, ask numbered clarification questions only and do not create or update the Plan. Do not resolve the gap using common architecture practices, framework defaults, industry assumptions, or inferred requirements.
5. Otherwise create a practical milestone-based Plan using only explicit or repository-confirmed requirements.
6. Keep milestones small and independently reviewable.
7. Describe milestones as delivery outcomes, not RED/GREEN execution phases.
8. Do not pull later-milestone work or decisions into an earlier milestone merely to prepare for future implementation.

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
- Do not invent endpoints, DTOs, database tables, packages, infrastructure, security controls, compliance obligations, SLOs, or non-functional requirements not supported by the input or repository evidence.
- Do not mark the Plan approved on behalf of the human reviewer.

## Output

After creating the file, summarize:

- the milestones
- any assumptions explicitly supported by current repository evidence
- questions or decisions the reviewer must resolve
