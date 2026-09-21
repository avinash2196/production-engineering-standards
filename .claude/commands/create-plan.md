---
description: "Create or update docs/.ai/Plan.md. Planning only."
---

Act as a requirements/planning expert and create or update the Plan.

Apply `requirements-analysis` and `prompt-driven-development`.

Read the approved requirements and inspect repository evidence relevant to the requested work.

Create/update only `docs/.ai/Plan.md`.

Define approved scope, milestones, predecessors, explicit exclusions, success criteria, and execution-status tracking.

If the work involves externally observable behavior (an HTTP API, message contract, or other stable consumer-facing interface), include an API/External Contract step in the milestone sequence, positioned before the first Implementation Plan, with its own predecessor and an Execution Status row.

Apply the Adaptive Milestone Decomposition rules from the `prompt-driven-development` skill when creating Plan.md. Explicitly document the chosen milestone boundaries and the reason for that granularity.

Do not implement production code or tests.
Do not create phase-specific Implementation Plans in this step.
Do not approve the Plan yourself.

If a material decision required for the Plan is unresolved, ask focused clarification questions and stop.
