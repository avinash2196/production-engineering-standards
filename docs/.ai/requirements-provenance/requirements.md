# Requirements — requirements-provenance

## Context

A PDD evaluation run of `capture-requirements` (plugin 0.8.0, Claude Code) on an enhancement work item
produced a requirements artifact that was faithful in scope (no invented features, correct stop before
planning) but drifted in provenance. The 0.8.1 Requirements Capture rules (`capture-requirements-drift`)
close part of this; the gaps below remain. A follow-up `review-requirements` run on the same artifact
also missed an unbounded qualitative term.

Observed drift (0.8.0 run):

1. A rule the user never stated was recorded as a requirement and attributed to the user's brief; it was
   an extrapolation from another work item's approved exclusion.
2. A constraint contained only in the wording of a clarification option the agent itself wrote became a
   requirement once the user picked that option, without separate confirmation.
3. Consequences the agent derived from user answers were recorded as explicit requirements or as
   repository facts.
4. A user answer "X is not required" was recorded as "X is excluded".
5. File:line citations were copied from a sibling work item's requirements artifact and were stale
   against the current code.
6. A closing statement copied from the sibling artifact ("no requirement was inferred …") was false for
   this artifact.
7. `review-requirements` did not flag "unavailable or slow" as untestable without a bound on "slow".

## Requirements

### RP-1 — Every recorded item names its source

Each requirement, constraint, exclusion, resolved decision, and repository fact in a work item's
requirements artifact carries a source: the user (brief or numbered answer), repository inspection
(with location), an approved artifact of another work item that this work item explicitly depends on,
or derivation.

### RP-2 — Derived consequences are a separate category and need confirmation

A statement the agent derives from user input or repository evidence is classified as a derived
consequence, labelled as such with what it is derived from, and confirmed by the user before the
artifact is finalized. It is never labelled as a user requirement or a repository fact.

### RP-3 — Options the agent writes do not smuggle requirements

When the user picks a clarification option the agent wrote, only what the user confirmed is recorded as
the user's decision. Further constraints implied by the option's wording are derived consequences
(RP-2).

### RP-4 — "Not required" is not "excluded"

An answer that a capability is not required is recorded as not required. A capability is recorded as
excluded (must not be introduced) only when the user excludes it or an approved artifact does.

### RP-5 — Other work items are context, not templates or sources

Other work items' artifacts may be read for context. Their structure, wording, citations, and closing
statements are not copied into the current artifact; any fact taken from them is re-verified against the
current repository before it is recorded.

### RP-6 — Self-check before finalizing

Before finalizing a requirements artifact, the agent checks that every item has a source (RP-1), every
derived consequence is confirmed (RP-2), every repository citation was verified against the current
repository during this capture, and any absolute statement about the artifact (for example "nothing was
inferred") is true.

### RP-7 — Requirements template

The plugin provides a requirements template that carries source labels, so capture does not fall back
to imitating another work item's artifact.

### RP-8 — Unbounded qualitative terms are material

A qualitative term in a requirement that decides testable behavior (for example "slow", "large",
"soon", "high volume") without a bound is a material unresolved decision for both requirements capture
and requirements review: it is bounded, or explicitly deferred to a named later decision.

### RP-9 — Both platforms

The fix applies to the Copilot prompts and the Claude commands, and to the mirrored skills.

## Repository-Confirmed Facts

- `.github/skills/` is canonical and `.claude/skills/` is its byte-identical mirror; the validator
  enforces this (`tooling/scripts/validate_repository.py`, skill mirror check).
- `.github/prompts/capture-requirements.prompt.md` and `.claude/commands/capture-requirements.md` have
  identical instruction bodies; the same holds for `review-requirements`.
- `prompt-driven-development/templates/` has Plan, Implementation Plan, Final Review, and application
  instruction templates, and no requirements template.
- `requirements-analysis` classifies information into four categories with no derived-consequence
  category, and its Operational Characteristics rules say a "not required" answer is recorded as an
  explicit exclusion.
- The validator's required-template list does not need to change for a new template to be added.

## Operational Characteristics

This work item changes plugin instruction text only and no running system.

- Scale, deployment, availability and latency, consistency and concurrency, dependency failure,
  observability: not required for this work item.

## Acceptance Criteria

- AC-1: Re-running `capture-requirements` (Claude Code) on the evaluation brief produces an artifact in
  which every item carries a source label, derived consequences are listed and confirmed, "not required"
  answers are not recorded as exclusions, and no citation or closing statement is copied from a sibling
  work item.
- AC-2: `review-requirements` on an artifact containing an unbounded qualitative term flags it.
- AC-3: `python tooling/scripts/validate_repository.py` and the unittest suite pass.
