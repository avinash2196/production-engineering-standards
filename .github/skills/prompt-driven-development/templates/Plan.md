# Plan

Apply the `prompt-driven-development` skill's Plan Content Rules to every section below. The Plan defines WHAT is delivered and in which milestone order — not HOW (Implementation Plans) and not externally observable behavior (the API/external contract). After approval it is the single source of truth for the complete development.

## Objective

## Current State

## In Scope

## Out of Scope

## Requirements and Constraints

Include only confirmed requirements, confirmed constraints, and repository-confirmed facts.

## Non-Blocking Open Decisions

List only decisions that do not block approval or change the correctness/scope of the current Plan.

Material unresolved decisions must be clarified before this Plan is approved.

Decisions the requirements explicitly defer to the API/external contract are not listed here as open — they are owned by the CONTRACT milestone and listed under External Contract Requirements.

## External Contract Requirements

Identify whether an API or other external contract must be defined before implementation.

If applicable, state the required contract artifact, the approved scope it must cover, and every decision it must resolve (including decisions the requirements defer to it). Do not resolve, narrow, or presume any of them here.

## Milestones

Apply the `prompt-driven-development` skill's Adaptive Milestone Decomposition rules to decide how many milestones this work needs, and record the reason for the chosen decomposition.

A milestone represents one independently approved execution boundary — CONTRACT, FOUNDATION, RED, GREEN, REFACTOR, or OTHER. There is no containing milestone that owns several of these as internal phases; a capability or layer that needs more than one milestone type gets a separate milestone entry for each (for example: Persistence RED, then Persistence GREEN, as two entries, not one "Persistence" milestone with a RED/GREEN lifecycle).

Record milestones in one strictly linear order. When a CONTRACT milestone exists it is the first milestone after Plan approval, and any FOUNDATION milestone follows it.

For each milestone record:

- capability / purpose: the independently reviewable unit of behavior this milestone covers
- rationale: why this boundary was chosen
- milestone type: CONTRACT | FOUNDATION | RED | GREEN | REFACTOR | OTHER
- predecessor: exactly one — Plan approval for the first milestone, otherwise one earlier milestone (e.g. the CONTRACT milestone a FOUNDATION milestone follows, or the RED milestone a GREEN milestone depends on)
- scope: the behavior or prerequisite this milestone covers, stated without naming classes, files, methods, test classes, or internal design
- owned requirements / concerns: the approved requirements and cross-cutting concerns (e.g. validation, authorization, error mapping, observability, persistence behavior — illustrative only) explicitly assigned to this milestone. A GREEN milestone may own delivery of an approved behavioral requirement while its predecessor RED milestone verifies that same requirement without being treated as its implementation owner.
- explicit exclusions
- success criteria: what successful completion of this milestone means

A milestone must not authorize work from a later milestone. Recording a milestone here does not itself authorize it — each repository-changing milestone still requires its own Implementation Plan, Human Review, and execution, in that order. A CONTRACT milestone changes no executable artifact and has no Implementation Plan; its human-reviewed deliverable is the contract artifact itself.

A FOUNDATION milestone requires its own approved Implementation Plan and Human Review before any repository change, exactly like a RED, GREEN, or REFACTOR milestone. It is conditional — include one only for a genuine executable prerequisite (e.g. initial project scaffolding, required build/dependency/test-infrastructure setup) that the following RED milestone needs, never merely because a production type or behavior that RED is meant to drive does not yet exist. FOUNDATION is not a way to change code outside the RED/GREEN/REFACTOR sequence or without approval.

## Requirement Traceability

| Requirement / Concern | Owning Milestone | Verifying Milestone |
| --- | --- | --- |
|  |  |  |

Every approved requirement and cross-cutting concern appears exactly once with one owning milestone.

## Execution Status

| Milestone | Status | Evidence / Notes |
| --- | --- | --- |
|  | Pending |  |

A newly created or revised Plan records every milestone as Pending. After Plan approval, update only execution/status information unless an explicit replanning step is approved.

## Risks

Risks and mitigations must not weaken, reinterpret, or contradict an approved requirement.

## Final Acceptance Criteria
