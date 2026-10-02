# PDD Gap Fixes — October 2026

Status: proposed, not applied. One batch, one plugin release.

Supersedes `docs/pdd-gap-fixes-2026-10-requirements-template.md` (this repo) and the
order-management gap log (`docs/pdd-gap-fixes-2026-10-requirements-template.md` in the
`order-management-service` `oracle-persistence` worktree). Source IDs below refer to those logs:
`G1`–`G27` = order-management log, `Fix A`–`Fix G` = workspace-reservation brief.

## Evidence sources

| Project | Work item | Executor | Plugin |
| --- | --- | --- | --- |
| order-management-service | `oracle-persistence` (infrastructure swap, unchanged API) | GitHub Copilot | 0.11.0 (`.github/`) |
| workspace-reservation-service | `test-case-stabilization` (test-only fix) | Claude Code | 0.11.0 (`.claude/`) |

A gap seen on both projects, with both executors, is the strongest evidence that it is a
plugin gap and not a project or model quirk.

## Rules for this batch

- **Project-neutral.** No application, work item, technology, library, image, or test name
  enters any skill, prompt, command, agent, or template. Project details stay in this brief
  as evidence only.
- **Plugin gaps only.** A finding where the model broke a rule the plugin already states
  clearly needs no plugin change — human review is the control (see "No plugin change").
- **Prefer structure over prose.** Copilot followed template structure (sections, fields,
  labels) more reliably than judgment rules. Where a gap is real, prefer a template field or
  a checklist line to another paragraph. Do not repeat rules at the top of commands.
- **Smallest wording.** Extend an existing rule before adding a new one.

## Fixes

### F1 — Template guidance in HTML comments (Fix A, G3, G19 Execution Status text)

Evidence: writer guidance copied verbatim into generated requirements, Plan,
Implementation Plan, and Final Review artifacts, on both projects.

Change: in every artifact template (`requirements.md`, `Plan.md`, `Implementation-Plan.md`,
`Final-Review.md`), wrap writer-only guidance in `<!-- … -->`. Each artifact-creating
command removes template comments from the finished artifact. Keep as real content only
text meant to appear in the artifact (for example the source-label legend, if intended).

**Exclusion:** the application instruction templates (`application-claude-instructions.md`,
`application-copilot-instructions.md`) are copied byte for byte by the setup commands,
including their `<!-- FIXED -->` and `PDD-CONTROL` comments. The strip rule must not apply
to them; say so explicitly.

### F2 — One approval rule for every predecessor artifact (G13, Fix G)

Evidence: `create-plan` ran while `requirements.md` said "Awaiting human review";
`create-implementation-plan` accepted chat approval of the Plan and cited the conversation,
leaving `Plan.md` with no approval trace and pending review fixes unapplied.

Change:
- Add a `## Status` section to `templates/Plan.md`, same form as the requirements template.
- Generalize `prompt-driven-development` Approval Status from Implementation Plans to every
  artifact a command depends on (requirements → Plan → contract → Implementation Plan).
- Each command checks its predecessor's recorded Status before working. User approval given
  in the current conversation is valid (existing rule), but is recorded in the artifact's
  Status first. No approval → ask and stop.

Correction to G13: its proposed "trust the artifact over the prompt's approval claim"
contradicts the existing Approval Status rule — the claim came from the user. The defect is
the missing record, not the conversational approval.

### F3 — Existing tests and behavior are facts, not requirements (G2)

Change (`requirements-analysis` Requirements Capture): existing tests and behavior are
repository-confirmed facts. When the work item affects behavior that existing tests assert,
ask whether each affected behavior is kept, changed, or removed; record a requirement only
after the answer.

### F4 — Product-level supersession needs confirmation (G1)

Change (`requirements-analysis` Requirements Capture; requirements template Relationship to
Product-Level Requirements guidance): a product-level statement the work item contradicts or
replaces is a derived consequence — confirm with the user before recording it as changed;
never record it as still in force without confirmation.

### F5 — Revision mode for every artifact-creating command (G6)

Evidence: an update pass left contradicted bullets and table rows in place.

Change: copy `create-plan`'s existing "treat it as a revision, not a fresh draft … no stale
text may remain" paragraph into `capture-requirements` and `create-implementation-plan`.
"Move" means remove from the source section.

### F6 — Clarification numbering across the work item (G7)

Change: `Qn` numbering is continuous across every clarification round and every review of
the work item, never restarting at 1. The requirements template gains a short
`## Clarification Log` (Qn → question → answer) so each `[User: Qn]` label is traceable.

### F7 — Define the non-delivered item kinds once (G5, Fix B, Fix E)

Evidence: out-of-scope items filed as "deferred"; non-blocking decisions labeled `Derived`
without confirmation; "not required" characteristics and preserved behavior traced as
exclusions.

Change: one definition in `requirements-analysis`, used by the requirements and Plan
templates and Plan Content Rule 8:

| Kind | Meaning | Label / traceability |
| --- | --- | --- |
| Deferred | In scope; decided by a named later milestone | owning milestone named |
| Non-blocking | Left to a later phase; no effect on correctness or scope | `[Left to <phase> — non-blocking]`; never `Derived` |
| Exclusion | Must not be introduced (user or approved artifact) | no owner; verified at Final Review |
| Not required | Nothing to deliver; never called an exclusion | no owner; nothing to verify |
| Preserved behavior | Existing behavior that must stay unchanged | no owner; verified by the milestone whose preserved tests cover it |

Also (Fix C, simplified): Repository-Confirmed Facts holds only `[Repo: …]` items; a
confirmed derived consequence goes under Requirements with its `Derived … confirmed Qn`
label. No new section.

### F8 — Requirement ↔ criterion ↔ evidence coverage (G9, G15, G18, Fix F)

Evidence: in-scope requirements without acceptance criteria; a criterion assigned to a
milestone that cannot execute its verification; a Final Acceptance Criterion with no
planned evidence; a file used in verification but in no milestone's scope. Seen on both
projects — Fix F is no longer "weak".

Change:
- Requirements template: every in-scope requirement maps to at least one acceptance
  criterion, and every criterion traces to a requirement.
- Plan traceability: include Final Acceptance Criteria; each names the milestone whose
  completion evidence demonstrates it (or Final Review inspection), and that milestone must
  be able to produce that evidence.
- Plan self-check: every artifact used in a verification step appears in some milestone's
  scope.

### F9 — Self-checks list evidence, not verdicts (Fix D, G6, G18; G21 pattern)

Evidence: Provenance Check counted "one Derived item" while three existed; a Provenance
Check restated the previous pass's labels; a Plan self-check reported "Traceability: PASS"
with a missing scope item.

Change: one rule in `prompt-driven-development`, referenced by each command's self-check: a
check passes only by quoting what it checked — each `Derived` / `Left to` item with its
confirming `Qn`; each requirement with the scope bullet that delivers it. A summary, count,
or restated earlier check is not a pass. Re-derive the check after every edit.

### F10 — Only RED may end with a failing check (G19)

Change (`prompt-driven-development` Milestone Types; `create-plan` self-check): FOUNDATION,
GREEN, REFACTOR, and OTHER end with every verification command passing. Success criteria
with "fail" / "may fail" wording outside RED are an error. A milestone that cannot pass
independently means the decomposition is wrong — re-split, or ask and stop.

### F11 — Risks and plans add no scope or process (G15)

Evidence: mitigations re-introduced removed scope at Plan and Implementation Plan level;
invented "separate PR per milestone", owners, and a commit step "per repository policy".

Change (Plan Content Rule 9; `implementation-planning`): a risk mitigation may reference
only in-scope work; a mitigation that needs new scope becomes a question. Neither the Plan
nor an Implementation Plan prescribes commits, branches, PRs, owners, or other process
unless the requirements state it. Risks cite repository evidence.

### F12 — Close the dry-run escape hatch; record real evidence (G20, G23)

Evidence: dry run skipped because "Implementation Plans must not modify repository files";
skipped again because "no new Maven artifacts" while a new non-build file was introduced;
dry-run commands reported that were not the ones run; files downloaded into the user's
personal folder.

Change (`implementation-planning` Planning-Time Dry Run):
- Not modifying the repository is never a reason to skip — the dry run runs outside it.
- It covers every artifact type the milestone introduces (build, configuration, runtime or
  infrastructure files), not only dependencies.
- Record each command verbatim with trimmed real output.
- Create nothing outside a temporary location; list anything created.

Also (Dependency and Version Selection, reconciling G20 with the existing rule): when the
build's own dependency management (parent, BOM, platform) manages a dependency, that is
the cited source — use it and do not pin over it.

### F13 — Execution evidence, deviations, cleanup (G26)

Change (`implement-approved-plan`; `implementation-engineer`; Plan template Execution
Status guidance):
- Evidence = the command as run plus trimmed real output, stored in `Plan.md` or a linked
  file — never a statement that output "was recorded".
- Any difference between the planned and executed command is listed as a deviation with its
  reason (the existing deviation rule, applied to verification commands).
- Stop every process the executor started before reporting, and say so.
- Execution Status rows stay single-line; details go below the table.

### F14 — Final Review reads recorded evidence first (G27)

Change (`review-code`; `code-reviewer`; `code-review` skill):
- Read `Plan.md` Execution Status and the approved Implementation Plans before raising a
  finding; drop findings contradicted by recorded evidence or an approved decision.
- Never recommend reverting an approved decision as a fix — raise it as a question.
- Check user-facing documentation (README, product docs) for statements the change makes
  false; today only product-level `docs/requirements.md` is covered.
- Severity only with a concrete failure scenario; cite correct paths.

Correction to G27's process note: adding the Final Review row to `Plan.md` is required by
Final Review Authority. The defect is wording it "Completed" — acceptance is the user's
decision, so the row says the review is written and awaits the user's decision.

### F15 — `review-requirements` reviews an existing artifact (G11, G12)

Evidence: the command (argument hint "requirement, issue, or change request") was run on a
captured `requirements.md`; it re-asked recorded decisions, listed nine "to record" items
already present, and missed internal inconsistencies.

Change (`review-requirements`):
- When the work item already has `requirements.md`, review that artifact: a decision
  already recorded with a user label is settled — not re-asked, not "to record".
- Run an internal-consistency pass: Provenance Check vs. actual labels, overlapping
  requirements, contradicting sections, F8 coverage.
- End with: `Verdict: Ready for human approval | Blocked`, blocking items, and
  `Next step: <exact PDD command>`.
- Questions answerable from the build file or framework defaults, or that decide HOW, are
  not asked; they belong to the Implementation Plan (G10 — existing rule, restated here
  only as one line because this command lacked it).

## No plugin change (model broke a stated rule)

| Finding | Existing rule |
| --- | --- |
| G8 invented example values in requirements | `requirements-analysis` "Requirements only", "Name every source" |
| G10 implementation-level clarification questions | "Never ask what inspection can answer"; Material Clarification Gate (one line added in F15) |
| G12 wrong next step | `review-requirements` already names `capture-requirements` before `create-plan` |
| G14 production work in RED / FOUNDATION | Plan Content Rules 4 and 6 |
| G17 infrastructure swap typed RED/GREEN | Milestone Types table ("replacing build, configuration, or infrastructure under unchanged behavior → OTHER"); the correction prompt prescribed RED/GREEN |
| G21 elided code in "complete content" | Exact Code forbids ellipses and "unchanged" gaps |
| G22 Implementation Plan numbering | Work-Item Folders: "NNN is per work item and starts at 001" |
| G24 planned deletion replaced by a stub file | `implement-approved-plan` exact-application and diff-against-plan rules |
| G25 known defect left in exact content | Exact Code |
| Workspace: reopened a chosen option; untestable wording; wrong line citation; downgraded criterion; test miscount; unbounded loop; status not set to executed; FR-3 misclassification | Requirements Capture, Material Clarification Gate, Approval Status (F8 makes the downgraded criterion visible) |

## Watch (do not hard-code unless it recurs)

- **G4** — clarification misses how a replaced dependency is provided per runtime context.
  Partly covered by Operational Characteristics "Dependency failure … run locally or in CI".
- **G16** — prior approved artifacts outside `docs/.ai/<work-item>/` (legacy flat layout)
  not cited as constraints. Specific to repositories migrating from the flat layout.

## Keep out of the plugin

Evidence only, never skill text: database product, container image, and environment
variable names; Testcontainers coordinates and annotation placement; compose-file keys;
licensing risk; test counts; legacy flat-layout paths.

## Files

Edit the canonical `.github/` files, then mirror byte-identically to `.claude/`:

- `skills/prompt-driven-development/SKILL.md` — F2, F7 (Rule 8), F9, F10, F11 (Rule 9)
- `skills/prompt-driven-development/templates/requirements.md` — F1, F4, F6, F7, F8
- `skills/prompt-driven-development/templates/Plan.md` — F1, F2, F7, F8, F13
- `skills/prompt-driven-development/templates/Implementation-Plan.md` — F1
- `skills/prompt-driven-development/templates/Final-Review.md` — F1
- `skills/requirements-analysis/SKILL.md` — F3, F4, F7
- `skills/implementation-planning/SKILL.md` — F11, F12
- `skills/code-review/SKILL.md`, `agents/code-reviewer.agent.md` — F14
- `agents/implementation-engineer.agent.md` — F13
- `prompts/capture-requirements.prompt.md` — F1, F2, F5, F6
- `prompts/review-requirements.prompt.md` — F15
- `prompts/create-plan.prompt.md` — F1, F2, F8, F9, F10
- `prompts/create-api-contract.prompt.md` — F1, F2
- `prompts/create-implementation-plan.prompt.md` — F1, F2, F5, F12
- `prompts/generate-tests.prompt.md`, `implement-approved-plan.prompt.md`,
  `refactor-code.prompt.md` — F2, F13
- `prompts/review-code.prompt.md` — F1, F14

## Verification and release

1. Edit `.github` canonical files; mirror to `.claude/`.
2. `python tooling/scripts/validate_repository.py` and the unittest suite — both pass.
3. Bump the version in `.claude/.claude-plugin/plugin.json`, `.github/plugin/plugin.json`,
   and `.github/plugin/marketplace.json` (currently 0.11.0).
4. Commit; then `claude plugin marketplace update pes-marketplace` and
   `claude plugin update production-engineering-standards@pes-marketplace`.

Timing: apply after both evidence work items finish Final Review, so each runs under one
rule set. Add further findings here, not to the superseded logs.
