# PDD Gap Fixes — November 2026 (batch E): findings from the v11 project reviews

Status: decisions recorded (user, 2026-11-09); see "Decisions". Nothing here is applied yet. Target 0.16.0, alongside C19, C20, lighter plans (carried from batch C) and brief D (code quality).

## Why this brief

On 2026-11-08 the user asked for a review of the plugin-review files that Claude Code and Copilot wrote in the v11 application projects. This brief logs what those files and the repositories behind them show, checked against `main` at `a7377bc` (0.15.1).

The main lesson is about evidence quality. Two of the three review files are the executing agent scoring its own session. Their recommendations are mostly tooling wishes, and their token figures are estimates, not measurements. The useful evidence is in the git history and the `docs/.ai/` artifacts.

## Evidence sources

| ID | Source | Executor | Plugin | What it is |
| --- | --- | --- | --- | --- |
| S1 | `scribbing/plugin-review.md` (787 lines), 2026-10-31 and 2026-11-02 | Claude Code, claude-haiku-4.5 | 0.14.0 (per `scribe-architecture/docs/handover.md`) | The session's self-review (scored 8/10). Little about the plugin. |
| S2 | `Traffic/docs/PLUGIN-REVIEW.md` (1,017 lines) and `PLUGIN_REVIEW_UPDATE_SUMMARY.md` (176), 2026-11-01 to 2026-11-04 | GitHub Copilot | 0.14.0 named, but not used (see "Out-of-plugin session") | Tooling wishes plus Copilot's own account of rule breaks. |
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
| C28 | Starting new work (Traffic, 2026-11-01) | A new chat has no step that makes it look for an existing work item. The Copilot session started a second plan beside `initial-build`, which had Pending milestones. The folder was untracked, but it was on disk. The generated instruction file is the only text a new chat always loads, and it names the `docs/.ai/<work-item>/` layout but does not say to check for open work items. Seen once, in an out-of-plugin session. | Plugin (seen once; applied by user decision, 2026-11-09) | One line in both instruction templates: before starting new work, list `docs/.ai/*/Plan.md` files with Pending milestones and ask the user which work item this is. It is the "Continuing work" row of C29's routing table. B5 still holds: commands do not check for the instruction file. |
| C29 | Adoption (Traffic, 2026-11-01) | A session told only to "follow PDD" can imitate it without the plugin: it writes its own instruction file and Plan, and none of the plugin's rules apply. Copilot users are the most exposed, because their commands run inline (C19) and a new chat starts from the instruction file alone. README Quickstart says to generate the instruction file "once", but not that it must come from the setup command and never be written by hand, nor that each phase starts with a command and the work-item name. | Plugin (instruction templates and docs) | A **Command Routing** section in the fixed part of both instruction templates (see "C29 draft" below): which command each kind of request goes to, and a no-deadlock rule for requests no command covers. README Quickstart and `docs/getting-started.md`: the instruction file must come from the setup command and never be written by hand, and every phase starts with a PES command and the work-item name; a chat asked to "use PDD" without them improvises. |
| C30 | GREEN execution (S1, scribe `local-env-v1` M4, 2026-11-02) | The main session handed a `check.bat` scope fix to a `general-purpose` agent with its own brief instead of running `implement-approved-plan`. Same pattern as C25 (main conversation doing role work). This run used 0.14.0, before fresh-context forks, so it does not count as the post-C24 repeat that C25 is watching for. | Model | No change. C25 stays on Watch. |
| C31 | Requirements capture (approval-service `initial-build` F1, F2, F4, F15; `recent-reservations-v2` Clarification Log; user request, 2026-11-09) | Capture asks only when it finds a technical ambiguity, and asks "the minimum" questions. Nothing makes it ask why the work exists, who the actors are and what each may do, or which business rules apply. In approval-service nearly every requirement is `[User: Qn — recommended]`. The identity case rule was never asked, which became F1 (High, self-approval), and actors for metrics (F2) and data durability (F4) were never asked either. `recent-reservations-v2` asked 21 questions, none about who uses the list or why. | Plugin | A **Business Intent** pass in `requirements-analysis`, asked first in the same round: the problem and why now, actors and permissions, outcome, business rules and invariants (including identity and equality), and concrete scenarios including failures. Ask every unanswered intent point; technical questions keep the minimum rule. The requirements template gains `## Business Context` and `## Scenarios`. A 7th Operational Characteristic: **data durability and retention**. `review-requirements` lists intent gaps in its "Blocking — must be answered before planning" question group (`requirements-analysis` Presenting Clarification Questions). That is a question group, not a severity; findings keep High, Medium and Low (brief D). |
| C32 | Clarification answers delegated with "use recommended" (approval-service F15) | No option was marked as recommended, so the model chose every answer, and the user approved the artifact as a whole without confirming any single choice. | Plugin | When options are offered, mark one as recommended with its reason. "Use recommended" is recorded only after one list-back confirmation, in which actor, permission, identity and data-loss items are marked. |
| C33 | Requirements consistency (workspace-reservation RE-Q2, FR-1) | `docs/requirements.md:41` ("inclusive end") contradicts `:68` (half-open overlap). Two work items saw it, and both left it open. | Plugin | The Provenance Check gains one line: no two statements contradict each other, including product-level statements this work item relies on. |
| C34 | Answers to a forked command's questions (0.15.0 trial, C25; user discussion, 2026-11-09) | Approvals are written into the artifact (D1), and requirements answers go in the Clarification Log. When a fork of `create-plan`, `create-api-contract` or `create-implementation-plan` stops with questions, Fresh Context says only "the user answers there". A fresh rerun cannot see that answer. In the trial, the main conversation edited the Implementation Plans itself after the OQ-1 and OQ-G1 answers, and once passed about 2,500 characters of its own briefing into the command. | Plugin | The rerun takes the user's answers, quoted, after the work item. The command records each one in the artifact under its question ID with the user's name and date. An answer never lives only in the conversation. |
| C35 | Artifacts not committed (v11, 2026-11-09) | `docs/.ai/` is untracked in approval-service, workspace-reservation (`recent-reservations-v2`) and Traffic, and the workspace-reservation worktree holds its own copy. A new worktree, clone or session cannot see the artifacts. Execution Status records no commit, so a later session cannot separate a milestone's diff from unplanned changes (brief D E8). | Plugin | `prepare-pr` commits `docs/.ai/<work-item>/` together with the milestone. After the commit, Execution Status records the commit hash. Every command, planning included, compares the repository with what `Plan.md` records as done, and stops and reports uncommitted or unplanned changes instead of building on them (user discussion, 2026-11-09). |
| C36 | Final Review findings with no follow-up (approval-service `initial-build`) | The Final Review's User Decision is blank, so a new session cannot tell whether F1 (High) was accepted or is still open. C28's check lists only Pending milestones. | Plugin | The C29 "Continuing work" row also lists Final Reviews whose User Decision is empty. An accepted finding becomes a C27 fix work item. |
| C37 | Command inputs (user discussion, 2026-11-09; `.github/prompts/implement-approved-plan.prompt.md:22`, `refactor-code.prompt.md:22`) | Every execution command reads "the authoritative requirements, Plan, and applicable API/external contract" (or "the authoritative artifacts"), although an approved FOUNDATION, GREEN, OTHER or REFACTOR Implementation Plan already holds the exact code, the commands and the expected evidence, and any difference stops execution. Re-reading requirements and the contract cannot change what these commands do, and costs context in every fork. | Plugin | One input table in `prompt-driven-development` Fresh Context; each command's Read list matches it. Planning commands and RED read requirements, the Plan, the contract and the repository. RED keeps them because it re-checks that each assertion matches the approved requirement or contract (`generate-tests`, test-engineer). GREEN, FOUNDATION, OTHER and REFACTOR read only `Plan.md` (status and predecessor evidence), their own Implementation Plan and the repository. `create-implementation-plan` reads earlier Implementation Plans' Review Summary and Carried-Forward Decisions, and their exact code only for files it touches. Reviews read everything. Every command reads the current repository. |

## C29 draft: Command Routing (user decision, 2026-11-09)

A new fixed section in `application-claude-instructions.md` and `application-copilot-instructions.md`. Because it is fixed, the setup command copies it verbatim and a hand-edited file is the only way to lose it. This is the instruction file pointing to the commands; B5 still holds (commands do not check for the instruction file), so nothing deadlocks at bootstrap.

**Routing.** Use the plugin's commands for PDD work, with the work-item name:

| The request is | Route |
| --- | --- |
| New work, or a change to behavior | `capture-requirements <work-item>`, then each report's `Next:` line. |
| Continuing work | First list `docs/.ai/*/Plan.md` files with Pending milestones and ask which work item this is (C28). Then run the command for that work item's next step. |
| A defect in finished work | A fix work item with one milestone (C27): `capture-requirements` with the defect, the expected behavior and how to reproduce it. |
| Review, readiness, architecture | `review-code`, `review-production-readiness`, `review-architecture`. |
| Commit and PR | `prepare-pr` (brief D). Until it exists, only when the user asks. |

**No deadlock.** When no command covers the request, say so, name the closest command, and ask. Without a command you may only:

- answer questions and investigate read-only;
- edit documentation outside executable artifacts;
- run commands the user asks for.

Never write your own requirements, Plan, Implementation Plan or approval in place of a command's artifact. Never create status or summary files; progress and verification live only in `Plan.md` Execution Status. Any change to code, tests, configuration or dependencies still needs an approved Implementation Plan, so route it through a one-milestone work item.

**Limits.** This is guidance, not enforcement. It would likely have stopped the Traffic drift, but not a model that ignores the file. The C28 row is applied although C28 was seen only once (user decision, 2026-11-09): it is one line, and the Traffic drift shows the cost of missing it.

**Files (when applied).** Both instruction templates (new fixed section); README Quickstart and `docs/getting-started.md`; validator and tests: both templates contain the section, and every command it names exists in `.github/prompts/` and `.claude/commands/`. Because the table names `prepare-pr`, apply brief D in the same release or first, or drop that row.

## Evidence for items already open

| Item | New evidence |
| --- | --- |
| G1 (no reviewed home for architecture) | Traffic `initial-build` produced its own `Architecture-Proposal.md` (decisions AP-D01–AP-D06, approved 2026-10-24) before the Plan, and the Plan cites it as an approved source. The model invented the artifact the plugin lacks. Strong input for the G1 fix shape. |
| G3 (decomposition for multi-part work) | S1 F1: `platform-libs-v1` has five libraries and about 39 requirements, and the session asked whether to split per library or per layer. |
| H4 follow-up (drop the `security` planning trigger; batch-B review) | approval-service F14(a): `security` was not applied while planning M3 and M4, which own authentication, and this contributed to F1 (High). **Closed (user, 2026-11-09): keep the trigger; no change.** |
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

## Decisions (user, 2026-11-09)

| # | Question | Decision |
| --- | --- | --- |
| 1 | C27 and C29 | Accepted as drafted. |
| 2 | C28 | Applied now, as the "Continuing work" row of C29's routing table, without waiting for a second case. |
| 3 | Brief letter | This brief keeps E. The planned roadmap and multi-pass brief takes the next letter. |
| 4 | C31–C33 (requirements capture, added 2026-11-09) | Accepted for 0.16.0, with the recommended answers to plan questions Q2–Q4: business-intent questions are exempt from "minimum", data durability and retention is a 7th characteristic, and delegated answers need one list-back confirmation. |
| 5 | C34–C36 (session hand-off, added 2026-11-09) | Accepted for 0.16.0. No hand-off or status file: the artifacts stay the only state between sessions. |
| 6 | C37 (command inputs) | Accepted for 0.16.0 as the user split it: RED needs the requirements, Plan, contract and its Implementation Plan; GREEN needs only the Plan and its Implementation Plan, because the Implementation Plan already has all the changes. Planning commands also read the current repository. |

## Lighter dry run (user decision, 2026-11-09)

Amends the 0.16.0 "lighter plans" item carried from batch C. The exact code always stays. The user approved it in the parent session with the words "yes this is good"; another session relayed it here.

- **Two writes stay, by design:** the exact code in the Implementation Plan, which the user reviews, and execution applying exactly that code. The dry run is the extra pass, and most of the cost went there.
- **RED dry run:** kept in full, but it runs only the new tests and proves they fail now and pass with the planned GREEN change (the B8 soundness proof).
- **GREEN dry run:** compile, plus only the tests the milestone adds or affects, run once. The full suite runs once, at execution only.
- **Everywhere:** no repeated dry-run runs, and no probes beyond the RED fail-and-pass proof.
- **Why the dry run stays:** in brief B it caught a contract-defined name the runtime could not produce, and the B8 RED soundness proof depends on it.
- **Cost evidence:** the GREEN planning step of trial 2 (`recent-reservations-v2`) cost $17, partly because it ran the full 117-test suite twice (C26). Its artifacts total 4,380 lines (RED plan 1,851, GREEN plan 1,294).

### Proposals (P1–P4 accepted for 0.16.0; T1 rejected; user, 2026-11-09 and 2026-11-10)

| ID | Proposal |
| --- | --- |
| P1 | A small-change track. A change with no contract change and at most about 3 files gets one Implementation Plan with RED and GREEN sections, approved once and executed in two verified steps. |
| P2 | A mechanical diff-vs-plan check that fails when the changed files or hunks do not match the approved Implementation Plan, plus a check that the RED tests fail first. |
| P3 | Shorter skill text, because Model findings (C1, C14, C25, C26) show that longer rules get skipped. |
| P4 | Test output. Verification commands write their output to a log file, and the command reads and records only the summary and the failing tests, never the full log. A long run goes to the background with a completion notice, with no polling. The gate still waits for the recorded result. (Copilot CLI background support not checked.) |

Answers (user, 2026-11-10):

| Question | Answer |
| --- | --- |
| P1: do test files count toward the "about 3 files" limit? | No. Only production and build files count. |
| P2: hook script language | Python, like the validator. When Python is missing, the hook prints a clear message and allows the edit; the `prepare-pr` diff check still catches it. |
| P2: how the hook finds the active Implementation Plan | It infers it from `docs/.ai/*/Plan.md`: the one milestone whose Implementation Plan is approved and not yet executed. When none or more than one qualifies, the hook does nothing, and only `prepare-pr` checks. |
| P3: how much to cut | Largest skills first, with the same rules: measure each skill's size as loaded in a fork, trim without dropping any rule a test checks, and report sizes before and after. No fixed cap. |
| P4 | Accepted for 0.16.0. |
| T1 | Model tiering: execution agents on a mid-tier model. **Rejected (user, 2026-11-10):** the plugin does not dictate which model runs; that stays the user's choice. |

### Test scope per step (user decision, 2026-11-09; was P5)

Run tests scoped to the change in every step, and the full suite once per milestone that changes production or build code. Extends the lighter dry run to execution and review.

| Step | Tests run |
| --- | --- |
| RED dry run | Compile everything; new tests only (fail now, pass with the planned GREEN code) |
| RED execution | Compile everything; new tests only, each failing for the intended reason; plus tests that use any shared test file the milestone changes |
| GREEN dry run | Compile; new and affected tests, once |
| GREEN execution | Full suite once; a second run only for tests that touch stored state or override configuration (L2) |
| FOUNDATION, OTHER | Build and the checks the plan names; the full suite once if production or build files change |
| REFACTOR | Full suite once after the change; the baseline is the recorded GREEN run unless the commit changed since |
| `prepare-pr` | Runs the full suite once unless `Plan.md` records a full run at the same commit hash as the diff (C35). It may run on work done outside a PDD milestone, which has no recorded run (user, 2026-11-09). |
| Final Review | Reruns only when the commit differs from the last recorded full run |
| CI (project) | The project's CI runs the full suite on the PR; named at requirements as the verification gate, never invented |

Affected tests are listed in the Implementation Plan with how they were found (changed packages, tests referencing changed classes, tests the contract names) and approved with it. A change outside that list is a plan difference and stops execution. A known flaky test follows Pre-existing Failures.

## Rules for this batch

The same as batches A to C: fixes are project-neutral, only plugin gaps get a fix, structure over prose, the smallest wording that works, and every gap is checked against the latest `.github/` text before it is logged.
