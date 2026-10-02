# Requirements — <work-item>

<!-- Template guidance — remove every template comment from the finished artifact.
Apply the `requirements-analysis` skill's Requirements Capture rules to every section below. Build this artifact from this template, the user's input, and inspection of the current repository — never from another work item's requirements artifact. -->

Every item ends with one source label:

- `[User: brief]` or `[User: Qn]` — stated by the user, in the brief or in the answer to clarification question n (see Clarification Log).
- `[Repo: <path>:<line>]` — established by inspecting the current repository during this capture.
- `[Artifact: <work-item>/<file> <ID>]` — an approved requirement of another work item that this work item explicitly depends on; quote it, do not extend it.
- `[Derived from <sources> — confirmed Qn]` — a consequence derived from other items; recorded only after the user confirmed it.
- `[Left to <phase> — non-blocking]` — valid only in Non-Blocking Decisions.

## Goal

## Status

Awaiting human review. This artifact does not authorize a Plan, contract, Implementation Plan, test, or code change.

<!-- Only the user approves. On approval, replace the line above with: Approved by <name> on <date>. -->

## Relationship to Product-Level Requirements

<!-- State which product-level statements this work item changes or makes out of date, each with its source. A statement this work item contradicts or replaces is recorded as changed only after the user confirmed it (`Derived … confirmed Qn`); never record it as still in force without confirmation. Omit this section when there is no product-level `docs/requirements.md`. -->

## Repository-Confirmed Facts

<!-- Only facts established by inspection during this capture, each with `[Repo: <path>:<line>]`. No `Derived` items here — a confirmed derived consequence goes under Requirements. Existing tests and behavior are facts, not requirements. -->

## Requirements

## Operational Characteristics

| Characteristic | Answer | Source |
|----------------|--------|--------|

<!-- Record "not required for this work item" as not required. It is not an exclusion unless the user excluded it. -->

## Decisions Deferred to Later Milestones

<!-- In scope for this work item, decided by a named later milestone (for example CONTRACT). Each with that milestone and its source. Something not in this work item at all is an Explicit Exclusion, not a deferral. -->

## Explicit Exclusions

<!-- Only what the user or an approved artifact excludes — capabilities that must not be introduced. Each with its source. -->

## Non-Blocking Decisions

<!-- Decisions left to a later phase that do not change correctness or approved scope. Label each `[Left to <phase> — non-blocking]`; never `Derived`. -->

## Acceptance Criteria

<!-- Each criterion traces to the requirement IDs above, and every requirement above has at least one criterion. -->

## Clarification Log

| Q | Question | Answer |
|---|----------|--------|

<!-- One row per question asked for this work item, numbered continuously across every clarification round and every review — never restarting at 1. -->

## Provenance Check

<!-- Completed before finalizing (`requirements-analysis` Requirements Capture), and re-derived after every edit. Each line lists what was checked — a count or a restated earlier check is not a pass. -->

- Every item above carries a source label.
- `Derived` items, each with its confirming `Qn`: <list>
- `Left to` items: <list>
- `Repo` citations verified against the current repository during this capture: <list>
- Requirements without an acceptance criterion: <none, or list>
- No statement about this artifact as a whole (for example "nothing was inferred") is made unless it was checked.
