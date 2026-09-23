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

Create/update only `docs/.ai/Plan.md`, using the `prompt-driven-development` skill's `templates/Plan.md` structure and applying its Plan Content Rules.

Define approved scope, milestones, predecessors, explicit exclusions, success criteria, and execution-status tracking. Each milestone is CONTRACT, FOUNDATION, RED, GREEN, or REFACTOR — never a containing milestone that owns several of these as internal phases.

If the work involves externally observable behavior (an HTTP API, message contract, or other stable consumer-facing interface), record a CONTRACT milestone as the first milestone after Plan approval — before any FOUNDATION, RED, GREEN, or REFACTOR milestone — with an Execution Status row. It delivers the API/external contract artifact, owns every decision the requirements defer to the contract, and has no Implementation Plan.

Apply the Adaptive Milestone Decomposition rules from the `prompt-driven-development` skill when creating Plan.md. A simple cohesive change may use a single RED milestone → GREEN milestone → optional REFACTOR milestone sequence. For complex requirements spanning independently testable architectural layers, create a separate RED milestone and GREEN milestone (and optional REFACTOR milestone) for each layer rather than one feature-wide RED/GREEN pair — for example: Persistence RED → Persistence GREEN → Service RED → Service GREEN → API RED → API GREEN. Explicitly document the chosen milestone boundaries and the reason for each boundary in Plan.md.

Explicitly assign each approved requirement and cross-cutting concern to an owning milestone in Plan.md.

For each RED milestone, determine whether the current repository state is sufficient to begin RED. If executable prerequisites are genuinely missing, insert a preceding FOUNDATION milestone (after any CONTRACT milestone) — its own separate milestone entry in Plan.md, with its own predecessor and its own Implementation Plan — and document why it is required. Do not add a FOUNDATION milestone merely because the production class, service, repository, controller, method, interface, or other implementation does not yet exist — that absence may itself be valid RED evidence. Do not record FOUNDATION, RED, GREEN, or REFACTOR as phases inside one containing milestone's lifecycle; represent each as its own separate milestone in the sequence.

Do not implement production code or tests.
Do not create milestone-specific Implementation Plans in this step.
Do not approve the Plan yourself.

Project-specific choices (for example a preferred decomposition) come only from the task prompt or approved project artifacts; this command stays project-neutral.

Before stopping, check the Plan against each Plan Content Rule and every milestone field the template requires. Fix any violation in the Plan, then report the result rule by rule (pass, or what was fixed) with your summary.

If a material decision required for the Plan is unresolved, ask focused clarification questions and stop.
