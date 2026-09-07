---
description: "Create or update docs/.ai/Plan.md. Planning only."
argument-hint: "approved requirements or change request"
agent: "planner"
tools:
  - read
  - search
  - edit
---
Apply `requirements-analysis` and `prompt-driven-development`.

Read the approved requirements and inspect repository evidence relevant to the requested work.

Create/update only `docs/.ai/Plan.md`.

Define approved scope, milestones, predecessors, explicit exclusions, success criteria, and execution-status tracking.

For behavior changes, keep RED and GREEN as separate milestones and add REFACTOR only when justified.

Do not implement production code or tests.
Do not create phase-specific Implementation Plans in this step.
Do not approve the Plan yourself.

If a material decision required for the Plan is unresolved, ask focused clarification questions and stop.
