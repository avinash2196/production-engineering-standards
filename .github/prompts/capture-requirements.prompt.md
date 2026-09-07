---
description: "Capture or update a requirements artifact without planning or implementation."
argument-hint: "requirement source, change request, or user-provided requirements"
agent: "planner"
tools:
  - read
  - search
  - edit
---
Apply `requirements-analysis` and `prompt-driven-development`.

Capture only the requirements explicitly provided by the user or confirmed by repository evidence.

If a material unresolved decision exists, ask focused clarification questions and stop. Do not create or finalize the requirements artifact until the blocking questions are resolved.

Create or update only the requirements artifact requested by the user.

Do not create Plan.md, an API/external contract, an Implementation Plan, tests, or production code.
