# PDD Gap Fixes — October 2026: Artifact Templates

Status: proposed, not applied. Task brief for a separate session. This brief is updated
as each phase of the evidence work item is reviewed; check the Findings Log before applying.

## Context

Found while running the `test-case-stabilization` work item in
`workspace-reservation-service` (worktree
`C:\Users\avina\Downloads\avinash-repo\v11\workspace-reservation-service\worktrees\test-case-stablization`,
artifacts under `docs/.ai/test-case-stabilization/`), using plugin 0.11.0 in Claude Code.

Only findings that trace to a plugin gap are recorded here. Findings where the model broke
a rule the plugin already states clearly are listed in the Findings Log as "model" and need
**no plugin change** — human review is the control for those.

Keep every change project-neutral: no reference to any application, work item, or test.

## Findings Log

| Phase | Finding | Cause | Fix |
| --- | --- | --- | --- |
| Requirements | Template writer instruction copied into artifact | Plugin | A |
| Requirements | Non-blocking decisions labeled `Derived` without confirmation | Plugin | B |
| Requirements | Confirmed derived consequence filed under Repository-Confirmed Facts | Plugin | C |
| Requirements | Provenance Check miscounted Derived items | Plugin (check is a count) + model | D |
| Requirements | Reopened a user-chosen clarification option | Model | — |
| Requirements | Untestable wording ("ever", "isolated runs") | Model (partly the user prompt) | — |
| Plan | Template writer instruction copied into artifact (Plan template line 3) | Plugin | A |
| Plan | "Not required" operational characteristics traced as "exclusion, verified at Final Review"; preserved behavior also traced as an exclusion | Plugin | E |
| Plan | A Final Acceptance Criterion ("passes under both valid race outcomes") had no planned evidence; OTHER completion evidence covered only the stability bar | Plugin (weak) | F |
| Plan | Wrong line citation (`<packaging>` cited at the `<build>` range) | Model | — |
| Implementation Plan | Template guidance paraphrased into artifact ("This Implementation Plan records the baseline evidence before any change, and the existing tests that must keep passing…") | Plugin | A |
| Plan → Implementation Plan | Plan approval recorded nowhere in `Plan.md`; `create-implementation-plan` accepted a conversational "Plan.md is approved" and cited the conversation as the approval source, leaving `Plan.md` with no approval trace and its pending review fixes unapplied | Plugin | G |
| Implementation Plan | Downgraded a Plan Final Acceptance Criterion ("passes under both valid race outcomes") to "not required to occur"; 30-run loop counts pass/fail only, no outcome tally | Model (Fix F would make the gap visible) | — |
| Implementation Plan | Miscounted tests (says 20 `@Test` methods and 19 preserved; actual 21 and 20) | Model | — |
| Implementation Plan | Verification loop had no upper bound (`while :` until both outcomes seen) | Model | — |
| Execution | Implementation Plan Human Review status not updated to executed after verified execution (rule already in `prompt-driven-development` Approval Status) | Model | — |

## Files

Edit the canonical files, then mirror byte-identically to `.claude/`:

- `.github/skills/prompt-driven-development/templates/requirements.md`
- `.github/skills/prompt-driven-development/templates/Plan.md`
- `.github/skills/prompt-driven-development/templates/Implementation-Plan.md` (Fix A only)
- `.github/skills/prompt-driven-development/templates/Final-Review.md` (Fix A only)
- `.github/skills/prompt-driven-development/SKILL.md` (Fixes E, F)

Also check `.github/skills/requirements-analysis/SKILL.md` and the `capture-requirements`,
`create-plan`, `create-implementation-plan`, and review command/prompt files (+ `.claude/`
mirrors) for wording that must match the new labels, sections, or rules.

## Fix A — Template guidance leaks into the artifact (all templates)

**Evidence:** the generated requirements artifact began with the template's writer
instruction "Apply the `requirements-analysis` skill's Requirements Capture rules to every
section below…", and the generated Plan began with "Apply the `prompt-driven-development`
skill's Plan Content Rules to every section below…" — both copied verbatim, because every
template puts writer guidance in the document body with no marker distinguishing it from
content. `Implementation-Plan.md` and `Final-Review.md` follow the same pattern (per-section
prose such as "Describe the relevant current implementation…", "List every Plan-level
success criterion…"), so they will leak the same way — and the Implementation Plan
already did: its Milestone Type section paraphrased the template's "For OTHER: record the
baseline evidence…" guidance as artifact text.

**Change:** in every template under `templates/`, wrap each writer-only instruction (title
paragraph and per-section guidance) in HTML comments `<!-- … -->`, and add one line to each
artifact-creating command/prompt: remove all template comments from the finished artifact.
Keep as real content only text meant to appear in the artifact (for example the
requirements source-label legend, if intended). Consider a validator check that a template's
known guidance sentences do not appear in generated artifacts — only if the validator already
inspects generated artifacts; otherwise skip.

## Fix B — No label for an AI-left non-blocking decision

**Evidence:** Non-Blocking Decisions items were labeled `[Derived from TCS-R2]` although the
user never confirmed them, because the label set offers only `User`, `Repo`, `Artifact`, and
`Derived … confirmed Qn`. A decision deliberately left to a later phase has no honest label,
so the model used `Derived` and the Provenance Check then had to misreport.

**Change:** add a label such as
`[Left to <phase> — non-blocking]` (e.g. "Left to Implementation Plan"), state it is valid
only in Non-Blocking Decisions, and state that Non-Blocking Decisions must not use `Derived`.
Align `requirements-analysis` Non-Blocking Decisions wording if needed.

## Fix C — No home for confirmed derived consequences

**Evidence:** a user-confirmed derived consequence (an analysis inferred from code + test
fixtures) was placed under Repository-Confirmed Facts with a `Derived` label, because the
template has no section for confirmed derived consequences.

**Change:** add a section `## Confirmed Derived Consequences` (between Repository-Confirmed
Facts and Requirements, or inside Requirements as a sub-list — choose one), and state in the
Repository-Confirmed Facts guidance that it may contain only `[Repo: …]`-labeled items.

## Fix D — Provenance Check is a count, so miscounts go unnoticed

**Evidence:** the Provenance Check stated "The one `Derived` item…" while the artifact held
three `Derived` labels.

**Change:** change the Provenance Check bullets to require *listing* every `Derived` item by
ID or short name together with the question that confirmed it (and every `Left to …` item),
instead of a summary statement or count.

## Fix E — Plan traceability has no row type for "not required" or preserved behavior

**Evidence:** the generated Plan traced each "not required for this work item" operational
characteristic as "exclusion, verified at Final Review", and traced an unchanged, already-
governed behavior (consistency/concurrency, protected by the OTHER milestone's preserved
tests) the same way. This contradicts `requirements-analysis` Operational Characteristics
("'Not required' means no milestone must deliver it; it is not an exclusion"). The cause is
in the plugin: `templates/Plan.md` Requirement Traceability says "Every approved requirement
and cross-cutting concern appears exactly once with one owning milestone", and
`prompt-driven-development` Plan Content Rule 8 defines only owned requirements and
absence-stating exclusions — so the only non-owner option the model has is "exclusion".

**Change:** in Plan Content Rule 8 and the Plan template's traceability guidance, define
three non-owner row kinds and their exact Owning/Verifying text:
- exclusion (must not be introduced) → no owner, verified at Final Review;
- not required for this work item → no owner, nothing to verify; never called an exclusion;
- preserved existing behavior (unchanged; protected by named preserved tests) → no owner,
  verified by the milestone whose preserved tests cover it.

## Fix F — Acceptance criteria without planned evidence (weak; decide before applying)

**Evidence:** the generated Plan's OTHER milestone named completion evidence only for the
stability bar (N/N runs + full verify). A Final Acceptance Criterion requiring the test to
pass under *each* of two valid outcomes had no evidence that both outcomes were actually
exercised. The `prompt-driven-development` OTHER rules require "the evidence that shows
completion" but do not tie it to the work item's acceptance criteria.

**Change (proposed):** add one sentence to Plan Content Rules (or the OTHER section): every
Final Acceptance Criterion must be covered by some milestone's completion evidence or by
Final Review inspection, and the Plan names which. This may already be implied by the
Final-Review template ("A criterion without evidence is not met"); if the maintainer judges
the existing Final Review check sufficient, drop Fix F.

## Fix G — Plan approval has no recorded place

**Evidence:** the requirements template has a Status section where the user records approval,
and Implementation Plans record approval in Human Review — but `templates/Plan.md` has no
approval field (Execution Status lists milestones only). `create-implementation-plan` then
accepted "Plan.md is approved" in the conversation, cited the conversation as the approval
source in the Implementation Plan, and left `Plan.md` unchanged. Result: `Plan.md` carries no
approval trace, and review corrections requested for the Plan were silently bypassed. This
also conflicts with "Downstream artifacts trace to the requirements artifact, never to
conversation history" in spirit.

**Change:** add a `## Status` (or `## Human Review`) section to `templates/Plan.md` mirroring
the requirements template ("Awaiting human review…" → user records approval with name and
date). In `create-implementation-plan` (and every command that needs an approved Plan):
require approval to be recorded in `Plan.md`; if it is only given in conversation, record it
there first (the same rule Approval Status already applies to Implementation Plans), and if
none exists, ask and stop.

## Verification and release

Follow the repo's normal plugin release workflow:

1. Edit `.github` canonical files; mirror to `.claude/`.
2. `python tooling/scripts/validate_repository.py` and the unittest suite — both must pass.
3. Bump `.claude/.claude-plugin/plugin.json` version (currently 0.11.0).
4. Commit; then `claude plugin marketplace update pes-marketplace` and
   `claude plugin update production-engineering-standards@pes-marketplace`.

Timing: apply after the `test-case-stabilization` work item's Final Review, so its artifacts
are produced under one rule set; add any further template findings from that review to this
same release.
