---
description: "Create or update docs/.ai/Plan.md. Planning only."
---

Act as a requirements/planning expert and create or update the Plan.

Apply `requirements-analysis` and `prompt-driven-development`.

Read the approved requirements and inspect repository evidence relevant to the requested work.

Create/update only `docs/.ai/Plan.md`.

Define approved scope, milestones, predecessors, explicit exclusions, success criteria, and execution-status tracking.

If the work involves externally observable behavior (an HTTP API, message contract, or other stable consumer-facing interface), include an API/External Contract step in the milestone sequence, positioned before the first Implementation Plan, with its own predecessor and an Execution Status row.

Apply the Adaptive Milestone Decomposition rules from the `prompt-driven-development` skill when creating Plan.md. For complex requirements spanning independently testable architectural layers, prefer separate layer-wise milestones rather than one feature-wide RED/GREEN cycle. Explicitly document the chosen milestone boundaries and the reason for each boundary in Plan.md.

For each milestone, determine whether the current repository state is sufficient to begin RED. If executable prerequisites must first be established, create a preceding SETUP/FOUNDATION milestone with its own approved Implementation Plan, and document why setup is required. Do not create a SETUP/FOUNDATION milestone merely because the production type or behavior under test does not yet exist — that absence may itself be valid RED evidence. Preserve a separate RED → GREEN → optional REFACTOR cycle for each independently reviewable layer.

Do not implement production code or tests.
Do not create phase-specific Implementation Plans in this step.
Do not approve the Plan yourself.

If a material decision required for the Plan is unresolved, ask focused clarification questions and stop.
