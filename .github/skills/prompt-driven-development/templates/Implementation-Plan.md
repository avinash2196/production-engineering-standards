# Implementation Plan

<!-- Template guidance — remove every template comment from the finished artifact. Add no section beyond this template unless the milestone needs it, and then say why in one line (`implementation-planning` Plan Size). -->

## Milestone

## Milestone Type

FOUNDATION | RED | GREEN | REFACTOR | OTHER

<!-- For OTHER: record the baseline evidence before any change, and the existing tests that must keep passing.

For RED whose evidence is an existing failing test: name the test, record its current failure, and list no files to change.

For standalone REFACTOR: record the full verification suite passing on the unmodified repository as the GREEN baseline, and the existing tests that cover the code being restructured.

For a paired plan (`Decomposition: one pair, one plan`): name both milestones, for example `RED RR-M2 + GREEN RR-M3`. Files in Scope, Proposed Changes, Proposed Code / Tests, Acceptance / Completion Criteria and Verification each have a `RED` part and a `GREEN` part. -->

## Review Summary

<!-- At most about 8 lines, written last, adding no decision (`implementation-planning` Review Summary):
- Behavior change: <what changes, or "tests only", or "none">
- Requirements covered: <IDs>
- Files: created <list>; modified <list>; deleted <list>
- Tests added: <tests> — they prove <behavior>
- Verification: <command> — expected <result>
- Needs attention: <items, or "none"> -->

## Authoritative References

## Carried-Forward Decisions

<!-- List decisions from earlier approved Implementation Plans that this milestone relies on, citing the Implementation Plan that approved each, or write `None.` Do not reopen them; a change requires explicit user approval recorded here with its reason. -->

## Preconditions / Predecessor Evidence

## Current Repository State

<!-- Only the facts the exact code depends on, each with `path:line`. No inventory of the repository. -->

## Files in Scope

### Files to Create

### Files to Modify

### Files to Delete

## Proposed Changes

<!-- For each file, describe the exact intended change and why it is required by the approved milestone.

Include relevant classes, methods, interfaces, signatures, structures, or configuration changes. -->

## Proposed Code / Tests

<!-- For every file in scope, include the exact code: the complete final content of a created file, and for a modified file either its complete final content or a complete unified diff covering every changed line with enough context to apply mechanically. No pseudocode, placeholders, ellipses, or partial fragments. Every change shown here must be named in Proposed Changes, and every change named there must appear here. Notes may explain the code; they never correct or override it.

The proposed content in this section is for review only and must not be applied during Implementation Plan creation. -->

## Execution Steps

## Acceptance / Completion Criteria

<!-- State exactly what must be true for this specific milestone to be considered complete.

Criteria limiting which files may change exclude this milestone's own Execution Status update in `Plan.md`. -->

## Verification

### Commands

<!-- Write each command's output to a log file and record only its summary and failing tests (`prompt-driven-development` Test Scope and Output). When tests touch persistent state or override configuration, add a second run of only those tests, without cleaning between runs. -->

### Affected Tests

<!-- The existing tests this milestone affects and how they were found (tests in the changed packages, tests that reference changed classes, tests the contract names), or `None.` Approved with the plan; a changed file this list does not cover is a plan difference. -->

### Expected Evidence

<!-- RED only: list the preserved-behavior tests the Plan assigns to this RED milestone, which are expected to pass at RED (`implementation-planning` RED), or state none. -->

- Preserved-behavior tests (expected to pass at RED): none | `<test>` — preserved row `<requirement>`

### Planning-Time Dry Run

<!-- The result of applying this plan's exact code in a disposable copy outside the repository (`implementation-planning` Planning-Time Dry Run): each command as run and its result, not a narrative. This is not milestone evidence. If a dry run was not performed, state why. -->

## Risks

<!-- Risks specific to this milestone, or `None.` -->

## Pre-authorized Contingencies

<!-- `None.` when there are none. Each entry: exact observable trigger, exact file, exact change. Anything not listed returns to planning. A contingency may never remove, loosen, or weaken a test assertion or an Acceptance / Completion Criterion. -->

## Rollback / Recovery

<!-- `None.` when not relevant. Reverse only this milestone's changes, file by file; never use repository-wide reset, clean, or checkout operations that could remove unrelated or uncommitted work. -->

## Explicitly Out of Scope

## Human Review

<!-- The only status field in this artifact. Only the user approves; see `prompt-driven-development` Approval Status. On approval: `Status: Approved by <name> on <date>`. After verified execution: `Status: Executed — see Plan.md`. A paired plan after RED only: `Status: RED executed — see Plan.md; GREEN approved, not yet executed`. If execution stops at a blocker: `Status: Execution stopped at a blocker — see Plan.md. Re-approval required before execution.` -->

Status: Awaiting human approval
