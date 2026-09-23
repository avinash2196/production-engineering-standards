# Plan

## Objective

## Current State

## In Scope

## Out of Scope

## Requirements and Constraints

Include only confirmed requirements, confirmed constraints, and repository-confirmed facts.

## Non-Blocking Open Decisions

List only decisions that do not block approval or change the correctness/scope of the current Plan.

Material unresolved decisions must be clarified before this Plan is approved.

## External Contract Requirements

Identify whether an API or other external contract must be defined before implementation.

If applicable, state the required contract artifact and the approved scope it must cover.

## Milestones

Apply the `prompt-driven-development` skill's Adaptive Milestone Decomposition rules to decide how many milestones this work needs.

A milestone represents one independently approved execution boundary — FOUNDATION, RED, GREEN, REFACTOR, or OTHER. There is no containing milestone that owns several of these as internal phases; a capability or layer that needs more than one milestone type gets a separate milestone entry for each (for example: Persistence RED, then Persistence GREEN, as two entries, not one "Persistence" milestone with a RED/GREEN lifecycle).

For each milestone record:

- capability / purpose: the independently reviewable unit of behavior this milestone covers
- rationale: why this boundary was chosen
- milestone type: FOUNDATION | RED | GREEN | REFACTOR | OTHER
- predecessor (dependency/order — e.g. another milestone this one depends on, such as a preceding FOUNDATION milestone or the RED milestone a GREEN milestone depends on)
- scope
- owned requirements / concerns: the approved requirements and cross-cutting concerns (e.g. validation, authorization, error mapping, observability, persistence behavior — illustrative only) explicitly assigned to this milestone. A GREEN milestone may own delivery of an approved behavioral requirement while its predecessor RED milestone verifies that same requirement without being treated as its implementation owner.
- explicit exclusions
- success criteria: what successful completion of this milestone means

A milestone must not authorize work from a later milestone. Recording a milestone here does not itself authorize it — each milestone still requires its own Implementation Plan, Human Review, and execution, in that order.

A FOUNDATION milestone requires its own approved Implementation Plan and Human Review before any repository change, exactly like a RED, GREEN, or REFACTOR milestone. It is conditional — include one only for a genuine executable prerequisite (e.g. initial project scaffolding, required build/dependency/test-infrastructure setup) that the following RED milestone needs, never merely because a production type or behavior that RED is meant to drive does not yet exist. FOUNDATION is not a way to change code outside the RED/GREEN/REFACTOR sequence or without approval.

## Execution Status

| Milestone | Status | Evidence / Notes |
| --- | --- | --- |
|  | Pending |  |

After Plan approval, update only execution/status information unless an explicit replanning step is approved.

## Risks

## Final Acceptance Criteria
