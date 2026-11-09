# PDD Gap Fixes — November 2026 (batch E): findings from the v11 project reviews

Status: draft for user review. Nothing here is applied. Proposed for 0.16.0, alongside C19, C20, lighter plans (carried from batch C) and brief D (code quality).

## Why this brief

On 2026-11-08 the user asked for a review of the plugin-review files that Claude Code and Copilot wrote in the v11 application projects. This brief logs what those files and the repositories behind them show, checked against `main` at `a7377bc` (0.15.1).

The main lesson is about evidence quality. Two of the three review files are the executing agent scoring its own session. Their recommendations are mostly tooling wishes, and their token figures are estimates, not measurements. The useful evidence is in the git history and the `docs/.ai/` artifacts.

## Evidence sources

| ID | Source | Executor | Plugin | What it is |
| --- | --- | --- | --- | --- |
| S1 | `scribbing/plugin-review.md` (787 lines), 2026-10-31 and 11-02 | Claude Code, claude-haiku-4.5 | 0.14.0 (per `scribe-architecture/docs/handover.md`) | The session's self-review (scored 8/10). Little about the plugin. |
| S2 | `Traffic/docs/PLUGIN-REVIEW.md` (1,017 lines) and `PLUGIN_REVIEW_UPDATE_SUMMARY.md` (176), 2026-11-01 to 11-04 | GitHub Copilot | 0.14.0 named, but not used (see "Out-of-plugin session") | Tooling wishes plus Copilot's own account of rule breaks. |
| S3 | `order-management-service/worktrees/oracle-persistence/docs/pdd-gap-fixes-2026-10-requirements-template.md`, 2026-10-02 | GitHub Copilot | 0.11.0 | Already consumed by batch A (0.12.0). Nothing new. |
| S4 | `Traffic` git history and `docs/.ai/initial-build/` (untracked in git) | Copilot (history); `initial-build` executor not recorded | 0.14.0 | The evidence behind S2. |

## Out-of-plugin session (no plugin change)

The Traffic drift happened in a Copilot session that did not run the plugin. The user confirmed (2026-11-08) that they did not ask for the switch.

- An approved PDD work item already existed: `docs/.ai/initial-build/` (21 milestones DP-M01–DP-M21, an approved `Architecture-Proposal.md`, DP-M01–DP-M07 completed with evidence, DP-M08 onward Pending).
- On 2026-11-01 a new Copilot session hand-wrote `.github/copilot-instructions.md` (407 lines). It did not come from `setup-copilot-instructions`: none of the template's fixed sections (Recording Approval, Clarification Before Action, the `docs/.ai/<work-item>/` layout) are in it.
- It wrote a second plan at `docs/Plan.md` (M1–M9, with Duration columns), not at `docs/.ai/<work-item>/Plan.md`. No PES command is named anywhere in its documents, and none of them mention `docs/.ai` or `initial-build`.

Everything below followed from that, so none of it is evidence about the plugin's rules:

| Observed | Why it is not a plugin gap |
| --- | --- |
| `docs/Plan.md` marked "APPROVED (2026-11-01, by Avinash … M1–M4.1 verified complete)", written after M1–M4.1 were built | D1 (0.15.0) states who approves and how it is recorded. The session never loaded it. |
| 57 commits after the M1–M4.1 status update (`6d724ae`), including `[DEFECT-FIX]` changes, with no Implementation Plan | The code-change rule is in the generated instruction file, which this session did not have. |
| M4.1 counted 10 SKIPPED tests as RED | The RED evidence rules (D5) require failing tests. Not loaded. |
| 17 summary, status and completion files (`SESSION_SUMMARY.md`, `COMPLETION.md`, …) | Copilot's own review: "PDD rules were clear; I simply did not follow them". See C29 for the one change worth making. |

## Findings Log

| ID | Phase | Finding | Kind | Fix |
| --- | --- | --- | --- | --- |
| C27 | After approval and Final Review (S2, Traffic `vehicle_number` and "Review Case" defects, 2026-11-04) | The plugin has no shape for fixing a defect found after a work item's Plan is approved or its Final Review is done. Every code change needs a milestone-specific Implementation Plan, but nothing says what a small fix looks like: a new work item, an amendment milestone (D4), or something lighter. The session's stated reason for skipping PDD was that "Writing Implementation Plan for a 1-line fix seemed inefficient". That session was out of plugin, but the reasoning applies to a proper run too, and C18 shows how heavy a small change gets today. Checked against `main`: no skill, prompt or template mentions a defect or fix path; the only guidance is the instruction templates' "small changes may use a very small Implementation Plan". | Plugin | With 0.16.0 lighter plans: a fix is its own work item with one milestone (`Decomposition: one milestone`), short requirements (the defect, the expected behavior, how to reproduce), and an Implementation Plan that is the C20 Review Summary plus the exact diff and the verification command. It still needs the user's approval. Reject S2's "Critical: auto-approved", which conflicts with D1. |
| C28 | Starting new work (Traffic, 2026-11-01) | A new chat has no step that makes it look for an existing work item. The Copilot session started a second plan beside `initial-build`, which had Pending milestones. The folder was untracked, but it was on disk. The generated instruction file is the only text a new chat always loads, and it names the `docs/.ai/<work-item>/` layout but does not say to check for open work items. Seen once, in an out-of-plugin session. | Plugin (Watch — seen once) | One line in both instruction templates: before starting new work, list `docs/.ai/*/Plan.md` files with Pending milestones and ask the user which work item this is. Decide after a second case. B5 still holds: commands do not check for the instruction file. |
| C29 | Adoption (Traffic, 2026-11-01) | A session told only to "follow PDD" can imitate it without the plugin: it writes its own instruction file and Plan, and none of the plugin's rules apply. Copilot users are the most exposed, because their commands run inline (C19) and a new chat starts from the instruction file alone. README Quickstart says to generate the instruction file "once", but not that it must come from the setup command and never be written by hand, nor that each phase starts with a command and the work-item name. | Plugin (docs) | README Quickstart and `docs/getting-started.md`: say that the instruction file must come from the setup command, and that every phase starts with a PES command and the work-item name; a chat asked to "use PDD" without them improvises. Add the same sentence on progress to both instruction templates: status and verification live only in `Plan.md` Execution Status; do not create separate summary or status files. |
| C30 | GREEN execution (S1, scribe `local-env-v1` M4, 2026-11-02) | The main session handed a `check.bat` scope fix to a `general-purpose` agent with its own brief instead of running `implement-approved-plan`. Same pattern as C25 (main conversation doing role work). This run used 0.14.0, before fresh-context forks, so it does not count as the post-C24 repeat that C25 is watching for. | Model | No change. C25 stays on Watch. |

## Evidence for items already open

| Item | New evidence |
| --- | --- |
| G1 (no reviewed home for architecture) | Traffic `initial-build` produced its own `Architecture-Proposal.md` (decisions AP-D01–AP-D06, approved 2026-10-24) before the Plan, and the Plan cites it as an approved source. The model invented the artifact the plugin lacks. Strong input for the G1 fix shape. |
| G3 (decomposition for multi-part work) | S1 F1: `platform-libs-v1` has five libraries and about 39 requirements, and the session asked whether to split per library or per layer. |
| C18 and C20 (plan weight and cost) | Traffic `initial-build` has 21 milestones. S1 reports about $445 for one week across the scribe workspace (self-reported, several work items). |

## Rejected (S1 and S2 recommendations)

| Recommendation | Reason |
| --- | --- |
| Parallel milestone rules, dependency checkers, artifact dependency declarations (S2 1, 4, 5; S1 parallel processing) | Plan Content Rule 1 keeps milestones in one linear order by design. Parallel sessions belong to the roadmap and multi-pass work, not this batch. |
| Context-window and token reporting (S2 2; both token tables) | A tool feature, not plugin text. The figures in both reviews are estimates. |
| Effort estimates in turns, contingency and rollback per milestone (S1) | Turns are not a stable unit. Rollback and recovery are already in `production-readiness`. |
| Commit-message generator, git batching (S2 3; S1) | Tool behavior. A milestone ID in commit messages is a project convention. |
| `verify-test-framework` command (S2 6) | Covered: FOUNDATION owns test infrastructure, and RED requires failing tests for the intended reason. |
| Audit, checkpoint and rollback commands, `.approvals/` folder (S2) | D1 records approval in the artifact; git holds history. |
| Prerequisite scripts, troubleshooting guide, glossary, Mermaid diagrams, `.fixtures/` folder (S1, S2) | Project documentation and conventions, not plugin rules. |
| `lint-docs` check for summary files (S2) | `tooling/` validates this repository only and cannot see application repositories. C29's template sentence covers the intent. |

## Rules for this batch

The same as batches A to C: fixes are project-neutral, only plugin gaps get a fix, structure over prose, the smallest wording that works, and every gap is checked against the latest `.github/` text before it is logged.
