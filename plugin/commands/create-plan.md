---
description: "Create or update docs/.ai/Plan.md. Planning only."
---

Act as a requirements/planning expert and create or update the Plan.

Apply `requirements-analysis` and `prompt-driven-development`.

Read the approved requirements and inspect repository evidence relevant to the requested work.

Create/update only `docs/.ai/Plan.md`.

Define approved scope, milestones, predecessors, explicit exclusions, success criteria, and execution-status tracking. Each milestone is FOUNDATION, RED, GREEN, or REFACTOR — never a containing milestone that owns several of these as internal phases.

If the work involves externally observable behavior (an HTTP API, message contract, or other stable consumer-facing interface), include an API/External Contract step in the milestone sequence, positioned before the first Implementation Plan, with its own predecessor and an Execution Status row.

Apply the Adaptive Milestone Decomposition rules from the `prompt-driven-development` skill when creating Plan.md. A simple cohesive change may use a single RED milestone → GREEN milestone → optional REFACTOR milestone sequence. For complex requirements spanning independently testable architectural layers, create a separate RED milestone and GREEN milestone (and optional REFACTOR milestone) for each layer rather than one feature-wide RED/GREEN pair — for example: Persistence RED → Persistence GREEN → Service RED → Service GREEN → API RED → API GREEN. Explicitly document the chosen milestone boundaries and the reason for each boundary in Plan.md.

Explicitly assign each approved requirement and cross-cutting concern to an owning milestone in Plan.md.

For each RED milestone, determine whether the current repository state is sufficient to begin RED. If executable prerequisites are genuinely missing, insert a preceding FOUNDATION milestone — its own separate milestone entry in Plan.md, with its own predecessor and its own Implementation Plan — and document why it is required. Do not add a FOUNDATION milestone merely because the production class, service, repository, controller, method, interface, or other implementation does not yet exist — that absence may itself be valid RED evidence. Do not record FOUNDATION, RED, GREEN, or REFACTOR as phases inside one containing milestone's lifecycle; represent each as its own separate milestone in the sequence.

Do not implement production code or tests.
Do not create milestone-specific Implementation Plans in this step.
Do not approve the Plan yourself.

If a material decision required for the Plan is unresolved, ask focused clarification questions and stop.
