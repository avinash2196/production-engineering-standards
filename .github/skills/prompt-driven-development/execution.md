# Prompt-Driven Development — Implementation Plans, Test Scope, Plan Integrity and Plan Progress

Part of the `prompt-driven-development` skill (see its Parts table). Apply it together with the core `SKILL.md`.

## Implementation Plan

Before creating an Implementation Plan, read the approved Requirements, Plan, and applicable API/external contract, the Plan's execution status and predecessor evidence, and the current repository. Establish the milestone's actual baseline: prerequisites, the contracts or interfaces it depends on, relevant test entry points, and unresolved blockers. Do not plan from an assumed repository structure, or from the original Plan alone when earlier milestones have changed the codebase. This inspection is preparation, not a milestone; if it shows that code must change before the milestone's own work, that change needs its own approved Implementation Plan.

An Implementation Plan is a human-review artifact, not a task list. For the authorized milestone it contains:

- authoritative artifact references and predecessor evidence;
- the current repository state relevant to the milestone;
- the exact files to create, modify, or delete, and the ordered proposed changes, with the classes, methods, interfaces, signatures, structures, or configuration they touch;
- exact code: the complete final content of every file to be created, and for every file to be modified either its complete final content or a complete unified diff covering every changed line with enough context to apply mechanically — never pseudocode, placeholders, ellipses, or partial fragments;
- explicit Acceptance / Completion Criteria for the specific milestone, distinct from the verification that demonstrates them;
- verification commands and expected milestone evidence;
- risks and explicit exclusions.

The planner writes the proposed code in the Implementation Plan for review, and never applies it to production source, tests, or build, deployment, or runtime configuration.

## Test Scope and Output

Run tests scoped to the change, and the full suite once per milestone that changes production or build code.

| Step | Tests run |
| --- | --- |
| RED dry run and RED execution | Compile everything; only the new tests, each failing for the intended reason; plus tests that use a shared test file the milestone changes |
| GREEN, FOUNDATION, OTHER, REFACTOR dry run | Compile; the new and affected tests, once |
| GREEN execution | The full suite once; a second run only for tests that touch persistent state or override configuration (`implementation-planning` Repeatable, Isolated Verification) |
| FOUNDATION, OTHER execution | Build and the checks the plan names; the full suite once when production or build files change |
| REFACTOR execution | The full suite once after the change; the baseline is the recorded GREEN run unless the repository changed since |
| `prepare-pr` | The full suite once, unless the working tree is clean apart from `docs/.ai/` and `Plan.md` records a full run at the current commit; always once in branch mode |
| Final Review | Rerun only when no full run is recorded for the current repository state |

The Implementation Plan lists the affected tests and how they were found (tests in the changed packages, tests that reference changed classes, tests the contract names); the user approves the list with the plan. A known flaky test follows `implementation-planning` Pre-existing Failures.

Test output:

- Write each verification command's output to a log file, and record only its summary (for example `Tests run`, `BUILD SUCCESS`) and the failing tests. Never copy the full log into the conversation or an artifact.
- Run a long command in the background with a completion notice where the tool supports it. Do not poll.
- The gate still waits: a milestone is complete only after the result is read and recorded in `Plan.md`.

## Plan Integrity

Before approval, the Plan is a working proposal and may be revised freely in response to human review. Human approval makes it the execution baseline: an authorization artifact and a living execution-status record that the AI never changes silently. Material unresolved decisions are resolved before approval. After approval, never rewrite the Plan to match implementation, change milestone definitions during execution, or expand scope for a technically useful improvement; only execution status changes (Plan Progress). Scope, milestone, architecture, or success-criteria changes need explicit replanning and human review.

If execution reveals that the approved Plan itself must change, stop for replanning and human review. Replanning is allowed at any point, including after implementation has started; the control is human approval, not immutability. When a blocker materially invalidates approved scope, milestone order, architecture, assumptions, or acceptance criteria:

1. The execution command stops. It records the milestone in `Plan.md` Execution Status as `Blocked — <reason>`, with its evidence below the table, and records in the Implementation Plan's Human Review status: `Execution stopped at a blocker — see Plan.md. Re-approval required before execution.` It describes the minimum Plan revision in its report and changes nothing else in `Plan.md`.
2. Any change to scope, milestones, architecture, or acceptance criteria is made only through `create-plan` revision mode, which addresses every `Blocked` row, replaces it with the revised milestone's Pending row, and keeps executed milestones and their evidence unchanged.
3. The revised Plan returns to awaiting human review.
4. Execution resumes only after the user approves the revised Plan, and the affected milestone runs only from a new Implementation Plan or the user's recorded re-approval of the existing one.

When execution shows that an approved contract decision cannot be met, use the same stop (step 1), naming the contract decision and the evidence. Then:

1. `create-api-contract` revision mode changes only that decision and records it in the contract's Amendments section: the change, the reason with its evidence, the impact, and the executed milestones whose tests or code encode the old decision. The amended contract returns to awaiting review.
2. `create-plan` revision mode adds new Pending milestones that bring the executed work the amendment lists into line with the amended contract. Each has its own name and is typed by the kind of change it makes (Milestone Types) — for example, a test that encodes the old decision is updated in an OTHER or RED milestone, and a production change is a RED and GREEN pair. None is labelled or numbered as part of an executed milestone. They are placed before the revised Blocked milestone, each with its own Implementation Plan numbered as the next `NNN`. The executed milestones' rows and evidence stay unchanged.
3. Execution resumes only after the user approves both the amended contract and the revised Plan.

Never replan and continue executing without that approval.

## Plan Progress

After an approved milestone is executed and verified, update only the Execution Status section of `Plan.md`: record the completed milestone and its evidence, and never rewrite requirements, scope, architecture, exclusions, success criteria, or future milestones. After `prepare-pr` commits the milestone, add `Committed as <hash>` to its row; changes only under `docs/.ai/` since that commit count as the same tested state. If verification fails or does not show the intended evidence, the milestone is not complete.

Execution Status values are `Pending`, `Waiting — <named input> from <who>`, `Blocked — <reason>`, and completed with evidence. `Waiting` records that an approved milestone cannot start or continue until the user supplies a named input or performs a named action (for example images, a deployment, or credentials the user enters). The Plan stays valid and the milestone resumes on the same approved Implementation Plan once the input exists; only `Blocked` needs replanning.

Evidence is each command as actually run with its trimmed real output (its summary and failing tests, never the full log; Test Scope and Output), stored in `Plan.md` below the Execution Status table (or in a file it links) — never a statement that output was recorded elsewhere. Each Execution Status row stays on one line and points to its evidence. Any difference between a planned and an executed command (arguments, port, profile, order) is listed as a deviation with its reason. Every process the executor started (servers, containers, background jobs) is stopped before reporting, and the report says so.
