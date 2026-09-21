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

Apply the `prompt-driven-development` skill's Adaptive Milestone Decomposition rules to decide granularity for this work.

A milestone represents one independently reviewable capability or layer — not one execution phase. Each milestone owns a lifecycle of phases; it is not itself a phase.

For each milestone record:

- capability: the independently reviewable unit of behavior this milestone covers
- rationale: why this boundary was chosen
- predecessor (dependency/order — e.g. another milestone this one depends on)
- setup required: Yes | No
- setup reason: why prerequisite FOUNDATION work is or is not needed before this milestone's RED can meaningfully begin, determined from the current repository state — a missing production type/behavior that RED itself is meant to drive is not a reason to answer Yes
- lifecycle: the phases this milestone will go through — conditional FOUNDATION (only when setup required is Yes), RED, GREEN, optional REFACTOR
- scope
- explicit exclusions
- milestone success criteria: what successful completion of the whole milestone means

A milestone must not authorize work from a later milestone. Recording a milestone's lifecycle here does not itself authorize any phase — each phase in that lifecycle (FOUNDATION when required, RED, GREEN, optional REFACTOR) still requires its own separate phase-specific Implementation Plan, Human Review, and execution, in that order.

FOUNDATION requires its own approved Implementation Plan and Human Review before any repository change, exactly like RED/GREEN/REFACTOR. It is conditional — use it only for a genuine executable prerequisite (e.g. initial project scaffolding, required build/dependency/test-infrastructure setup), never merely because a production type or behavior that RED is meant to drive does not yet exist. FOUNDATION is not a way to change code outside the RED/GREEN/REFACTOR cycle or without approval. Whether FOUNDATION is required is a planning decision recorded here, in Plan.md — it is not decided by whoever executes an Implementation Plan.

## Execution Status

| Milestone | Status | Evidence / Notes |
| --- | --- | --- |
|  | Pending |  |

After Plan approval, update only execution/status information unless an explicit replanning step is approved.

## Risks

## Final Acceptance Criteria
