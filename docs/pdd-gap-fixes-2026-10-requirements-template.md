# PDD Gap Fixes — October 2026: Requirements Template

Status: proposed, not applied. Task brief for a separate session.

## Context

Found while capturing requirements for the `test-case-stabilization` work item in
`workspace-reservation-service` (worktree
`C:\Users\avina\Downloads\avinash-repo\v11\workspace-reservation-service\worktrees\test-case-stablization`,
artifact `docs/.ai/test-case-stabilization/requirements.md`), using plugin 0.11.0
`capture-requirements` in Claude Code.

Human review of that artifact found six defects. Three trace to the requirements template
and its label set (fixed below). The other three were the model breaking rules the plugin
already states (reopening a user-chosen option, miscounting Derived items in the Provenance
Check, untestable wording like "ever"/"isolated"). **Do not add more rules for those** —
human review is the control.

Keep every change project-neutral: no reference to any application, work item, or test.

## Files

Edit the canonical file, then mirror byte-identically:

- `.github/skills/prompt-driven-development/templates/requirements.md` (canonical)
- `.claude/skills/prompt-driven-development/templates/requirements.md` (mirror)

Also check `.github/skills/requirements-analysis/SKILL.md` (+ `.claude/` mirror) and the
`capture-requirements` command/prompt files for any wording that must match the new labels
or sections.

## Fix A — Template guidance leaks into the artifact

**Evidence:** the generated artifact began with the template's writer instruction
"Apply the `requirements-analysis` skill's Requirements Capture rules to every section
below. Build this artifact from this template…" — copied verbatim, because the template
puts writer guidance in the document body with no marker distinguishing it from content.

**Change:** wrap every writer-only instruction in the template (title paragraph, per-section
guidance such as "Only facts established by inspection…", "Record 'not required'…") in
HTML comments `<!-- … -->`, and add one line in the capture instructions: remove all
template comments from the finished artifact. Keep the source-label legend as real content
only if it is meant to appear in the artifact; otherwise comment it too.

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
