# PDD Gap Fixes — November 2026 (batch F): large work, several work items, smaller skills

Status: draft (2026-11-10). Nothing decided, nothing applied. Target 0.17.0, on a `release/0.17.0` branch like 0.16.0.

## Why this brief

After the 0.16.0 release the user named the biggest remaining problem: large requests are built in one or two passes. One requirements file and one Plan try to hold everything, so each Plan, Implementation Plan and review is too large to review well. The user wants to:

1. plan a large request first as several separate sets of requirements, then run them one at a time;
2. run independent work, for example different services, in parallel, each with its own requirements;
3. re-review requirements capture, milestone decomposition and the phase rules together, so the levels do not overlap;
4. check whether the skill files are still too large.

This brief carries the batch C predictions G1 (no reviewed home for architecture) and G3 (decomposition of multi-part work), which now have run evidence. G4–G6 (several services, mixed stacks, several repositories) are partly covered by item 2.

## Evidence

| ID | Source | What happened |
| --- | --- | --- |
| F1 | User, 2026-11-10 | "biggest problem was doing everything together in one/two builds". |
| F2 | scribe `platform-libs-v1` (brief E, G3 row) | One work item held five libraries and about 39 requirements. The session asked whether to split per library or per layer; the plugin had no rule above the milestone level. |
| F3 | Traffic `initial-build` (brief E, G1 row) | The model wrote its own `Architecture-Proposal.md` (AP-D01–AP-D06) before the Plan, because no PDD artifact holds architecture decisions. |
| F4 | scribe platform run notes (brief C) | Seven services, one repository each. The architecture was settled in conversation and written into the product-level `docs/requirements.md`; a non-PDD `docs/roadmap.md` tracked the order across repositories (G1, G6). |
| F5 | Skill sizes on `main` at `v0.16.0` | `prompt-driven-development` 7,514 words (about 10k tokens), `implementation-planning` 3,287, `requirements-analysis` 1,996. Every PDD command loads the PDD skill in full. P3 removed only 7%, because the rest is distinct rules. |
| F6 | Brief E, rejected list | Parallel milestones inside one Plan were rejected: Plan Content Rule 1 keeps one linear order. Parallel *work items* were left to this brief. |

## Today's levels

| Level | Artifact | What splits it |
| --- | --- | --- |
| Product | optional `docs/requirements.md` (read-only to commands) | nothing |
| Work item | `docs/.ai/<work-item>/` | nothing: the user names one |
| Milestone | `Plan.md` rows | Adaptive Milestone Decomposition |

Nothing turns one large request into several work items, records their order, or says which can run at the same time.

## Proposals (to decide)

| ID | Proposal | Files when applied |
| --- | --- | --- |
| S1 | **Size check before capture.** `capture-requirements` checks whether the brief holds more than one independently deliverable piece (separate capabilities, services, libraries, or repositories). If so, it stops and proposes a split instead of capturing one work item. | `requirements-analysis`, `capture-requirements` |
| S2 | **A strategy level above work items.** A reviewed artifact lists the work items, what each owns, the order between them, which can run in parallel, and the architecture decisions they share (G1). The user approves it before any work item's requirements. | new template; new command or a `capture-requirements` mode; PDD skill levels |
| S3 | **Shared contracts first.** When parallel work items talk to each other, the contract between them is delivered first, by its own work item (or the strategy's first step), and each consumer plans against the approved contract. | PDD skill, strategy template |
| S4 | **Parallel runs.** Each work item runs in its own branch or worktree and session. A work item starts only when the strategy's predecessors are done. Command Routing lists open strategies as well as open work items. `prepare-pr` and Final Review stay per work item. | PDD skill, instruction templates, Command Routing |
| S5 | **Architecture decisions (G1).** A reviewed home for decisions shared by several work items (service boundaries, data ownership, sync or async, broker, auth). Either part of the strategy artifact or its own file. | `architecture-design`, strategy template |
| S6 | **One review of the three levels.** Requirements capture, Adaptive Milestone Decomposition and the new strategy level, reviewed together: each split reason belongs to exactly one level, and none repeats another. | `requirements-analysis`, PDD skill, `create-plan` |
| S7 | **Split the PDD skill by use.** Keep a small core (lifecycle, authority, approval, fresh context) that every command loads, and move the rest into parts loaded only by the commands that need them (Plan rules for `create-plan`; milestone execution rules for execution; Final Review rules for reviews). Measure tokens per command before and after. | PDD skill split; command `Apply` lines; validator (mirrors, references); tests updated, never deleted |

## Open questions

Asked one at a time; each answer is recorded here before anything is drafted further.

| Q | Question | Answer |
| --- | --- | --- |
| Q1 | Where is the parallel work: several services in one repository, one repository per service, or both? | |
| Q2 | Strategy artifact: a new command (`create-strategy`) with its own folder, or a mode of `capture-requirements`? | |
| Q3 | Architecture decisions (S5): inside the strategy artifact, or a separate `Architecture.md` reviewed with it? | |
| Q4 | Size check (S1): what makes a brief "too large" — a list of split reasons only, or also a number (for example more than about 15 requirements)? | |
| Q5 | When may a dependent work item start: after its predecessor's Final Review, or after its predecessor's contract is approved? | |
| Q6 | Skill split (S7): in 0.17.0 together with S1–S6, or first, as its own release? | |

## Not in this batch

- Parallel milestones inside one Plan (F6): Plan Content Rule 1 stays.
- A development loop runner that drives sessions automatically: its own repository, not the plugin (brief C).
