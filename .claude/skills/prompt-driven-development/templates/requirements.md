# Requirements — <work-item>

Apply the `requirements-analysis` skill's Requirements Capture rules to every section below. Build this artifact from this template, the user's input, and inspection of the current repository — never from another work item's requirements artifact.

Every item ends with one source label:

- `[User: brief]` or `[User: Qn]` — stated by the user, in the brief or in the answer to clarification question n.
- `[Repo: <path>:<line>]` — established by inspecting the current repository during this capture.
- `[Artifact: <work-item>/<file> <ID>]` — an approved requirement of another work item that this work item explicitly depends on; quote it, do not extend it.
- `[Derived from <sources> — confirmed Qn]` — a consequence derived from other items; recorded only after the user confirmed it.

## Goal

## Status

Awaiting human review. This artifact does not authorize a Plan, contract, Implementation Plan, test, or code change.

## Relationship to Product-Level Requirements

State which product-level statements this work item changes or makes out of date, each with its source. Omit when there is no product-level `docs/requirements.md`.

## Repository-Confirmed Facts

Only facts established by inspection during this capture, each with `[Repo: <path>:<line>]`.

## Requirements

## Operational Characteristics

| Characteristic | Answer | Source |
|----------------|--------|--------|

Record "not required for this work item" as not required. It is not an exclusion unless the user excluded it.

## Decisions Deferred to Later Milestones

Each with the milestone that owns it (for example CONTRACT) and its source.

## Explicit Exclusions

Only what the user or an approved artifact excludes — capabilities that must not be introduced. Each with its source.

## Non-Blocking Decisions

Decisions left to later phases that do not change correctness or approved scope.

## Acceptance Criteria

Each traceable to the requirement IDs above.

## Provenance Check

Completed before finalizing (`requirements-analysis` Requirements Capture):

- every item above carries a source label;
- every `Derived` item was confirmed by the user;
- every `Repo` citation was verified against the current repository during this capture;
- no statement about this artifact as a whole (for example "nothing was inferred") is made unless it was checked.
