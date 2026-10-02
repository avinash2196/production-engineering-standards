---
description: "Create or update docs/.ai/<work-item>/Plan.md. Planning only."
---

Act as a requirements/planning expert and create or update the Plan.

Apply `requirements-analysis` and `prompt-driven-development`.

Work item: operate only on the work-item folder the user names (`prompt-driven-development` Work-Item Folders). If no work item is named, ask and stop.

Read the work item's approved `docs/.ai/<work-item>/requirements.md` (and the product-level `docs/requirements.md` as read-only context when it exists) and inspect repository evidence relevant to the requested work.

Create/update only `docs/.ai/<work-item>/Plan.md`, using the `prompt-driven-development` skill's `templates/Plan.md` structure and applying its Plan Content Rules.

Define approved scope, milestones, predecessors, explicit exclusions, success criteria, and execution-status tracking. Each milestone is CONTRACT, FOUNDATION, RED, GREEN, REFACTOR, or OTHER, chosen by the kind of change (`prompt-driven-development` Milestone Types) — never a containing milestone that owns several of these as internal phases. Every requirement that adds or changes behavior is delivered by RED then GREEN; use OTHER only for approved work with no production behavior change, and record its no-behavior-change statement, baseline evidence, preserved tests, and completion evidence.

If the work item creates or changes externally observable behavior (an HTTP API, message contract, or other stable consumer-facing interface), record a CONTRACT milestone as the first milestone after Plan approval — before any FOUNDATION, RED, GREEN, or REFACTOR milestone — with an Execution Status row. It delivers the API/external contract artifact, owns every decision the requirements defer to the contract, and has no Implementation Plan. If the work item leaves an existing contract unchanged, reference it as a constraint and record no CONTRACT milestone.

Record the verification commands in the Plan's Verification Commands section with their source (Plan Content Rule 12).

Apply the Adaptive Milestone Decomposition rules from the `prompt-driven-development` skill when creating Plan.md. A simple cohesive change may use a single RED milestone → GREEN milestone → optional REFACTOR milestone sequence. For complex requirements spanning independently testable architectural layers, create a separate RED milestone and GREEN milestone (and optional REFACTOR milestone) for each layer rather than one feature-wide RED/GREEN pair — for example: Persistence RED → Persistence GREEN → Service RED → Service GREEN → API RED → API GREEN. Explicitly document the chosen milestone boundaries and the reason for each boundary in Plan.md.

Explicitly assign each approved requirement and cross-cutting concern to an owning milestone in Plan.md.

For each RED milestone, determine whether the repository state projected after all of its predecessor milestones complete — not only the current state — provides everything its tests need to compile and run (Plan Content Rule 11). RED milestones cannot add dependencies or test infrastructure. If executable prerequisites are genuinely missing, insert a preceding FOUNDATION milestone (after any CONTRACT milestone) — its own separate milestone entry in Plan.md, with its own predecessor and its own Implementation Plan — and document why it is required. Do not add a FOUNDATION milestone merely because the production class, service, repository, controller, method, interface, or other implementation does not yet exist — that absence may itself be valid RED evidence. Do not record FOUNDATION, RED, GREEN, or REFACTOR as phases inside one containing milestone's lifecycle; represent each as its own separate milestone in the sequence.

Do not implement production code or tests.
Do not create milestone-specific Implementation Plans in this step.
Do not approve the Plan yourself.

Project-specific choices (for example a preferred decomposition) come only from the task prompt or approved project artifacts; this command stays project-neutral.

Before stopping, check the Plan against each Plan Content Rule and every milestone field the template requires. The check must be evidence-based: re-read the written Plan and search it for each prohibited item the rules name (for example HTTP methods, paths, status codes, class, package, annotation, or library names, and alternatives the requirements exclude). Fix every violation in the Plan and re-check. Report the result rule by rule — pass, or the offending text and how it was fixed. Never report a rule as passing without having searched for its violations.

If a material decision required for the Plan is unresolved, ask focused clarification questions and stop.

If the requirements neither answer nor explicitly exclude an applicable operational characteristic (`requirements-analysis` Operational Characteristics), stop and route it back to requirements capture.

When revising an existing Plan (for example to fold in clarification answers or approved replanning), treat it as a revision, not a fresh draft: find every reference to each changed item — status rows, traceability rows, milestone fields, risks, and cross-references — and update all of them; no stale text may remain. In the self-check, compare against the previous version and report what changed and that every affected reference was updated.

Before stopping, confirm that no label or identifier this artifact introduces reuses a label already defined by an approved artifact it references (`prompt-driven-development` Artifact Authority).
