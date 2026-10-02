---
name: implementation-planning
description: Use when translating one approved Plan milestone into a concrete human-reviewable Implementation Plan based on the current repository state.
---

# Implementation Planning

Create an Implementation Plan for exactly one approved milestone.

Implementation Planning receives one approved milestone and its already-recorded milestone type (FOUNDATION, RED, GREEN, REFACTOR, or OTHER) from `Plan.md` — it does not decide or change the milestone type; that decision belongs to planning and is fixed once `Plan.md` is approved.

## Current-State Analysis

Before planning:

- read the approved Requirements, Plan, and applicable API/external contract;
- inspect the current repository structure;
- inspect relevant existing source, tests, configuration, and completed milestone work;
- read current Plan execution status;
- read every previously approved Implementation Plan and carry its decisions (versions, mechanisms, conventions, configuration and test-infrastructure choices) forward as approved inputs;
- verify predecessor milestone evidence and actual repository progress;
- verify that the milestone type being planned matches what `Plan.md` records for this milestone.

Prefer repository evidence over assumed structure or previously proposed implementation. Repository-state claims such as "clean working tree" must come from actual inspection, not assumption.

Causal claims — why something happens, fails, or behaves a certain way (for example why a test is flaky, or how a library behaves at startup) — must cite the code, requirement, or observed output that establishes them. Label an explanation that has not been established that way as a hypothesis; a plausible but unchecked explanation is not evidence.

Do not plan from an assumed project state.

A material ambiguity may remain unresolved while no milestone yet depends on a concrete decision about it. Before creating an Implementation Plan for a milestone whose FOUNDATION, RED, GREEN, REFACTOR, or OTHER work actually depends on resolving that ambiguity, resolve it through the existing PDD clarification/human-review mechanisms rather than carrying it forward unresolved into typed code, test assertions, or configuration. Examples of such ambiguity include field representation, nullability, identifier semantics, precision, validation behavior, persistence representation, or external contract behavior — these examples are illustrative only and do not themselves introduce new requirements. Do not force premature resolution of such decisions during Requirements Capture.

If the repository materially conflicts with authoritative artifacts or predecessor evidence, stop and surface the conflict for human review. If repository evidence contradicts the milestone type `Plan.md` recorded for this milestone (for example, `Plan.md` records this milestone as RED but a genuine prerequisite is actually missing, or records a FOUNDATION milestone that the repository shows is no longer needed), do not silently plan a different milestone type — stop and report the mismatch back to planning for a `Plan.md` update and re-approval.

## Implementation Plan Content

Include:

- milestone, including its milestone type (FOUNDATION, RED, GREEN, REFACTOR, or OTHER);
- authoritative artifact references;
- predecessor evidence;
- current repository state relevant to the milestone;
- exact files/components in scope;
- files to create;
- files to modify;
- ordered proposed changes;
- concrete proposed tests or production code;
- relevant method, class, interface, schema, or configuration signatures;
- exact code: the complete final content of every file to be created, and for every file to be modified either its complete final content or a complete unified diff covering every changed line with enough context to apply mechanically — never pseudocode, placeholders, ellipses, or partial fragments;
- explicit Acceptance / Completion Criteria for this specific milestone — what must be true for this FOUNDATION, RED, GREEN, REFACTOR, or OTHER milestone to be considered complete;
- verification commands that demonstrate those criteria;
- expected FOUNDATION, RED, GREEN, REFACTOR, or OTHER evidence;
- carried-forward decisions from earlier approved Implementation Plans;
- pre-authorized contingencies, if any;
- rollback or recovery where relevant, reversing only this milestone's changes — never repository-wide reset, clean, or checkout operations that could remove unrelated or uncommitted work;
- risks;
- explicit exclusions.

Acceptance / Completion Criteria and verification are distinct: the criteria state what must be true for the milestone to be complete; verification commands and expected evidence demonstrate whether the approved changes actually satisfied those criteria. Verification does not replace stating the criteria explicitly. Do not invent or modify Acceptance / Completion Criteria during execution — that belongs to planning.

Expected evidence stated in the Implementation Plan is a prediction, not proof — label it Expected / Predicted — Not Yet Verified. Treat it as verified only when: (1) the milestone has actually been executed; (2) the stated verification commands/checks have actually been run; and (3) the resulting evidence supports the expected outcome. Running a verification command is not sufficient by itself if it fails or produces evidence that contradicts the expected outcome.

The Implementation Plan must contain enough implementation detail for a human to review the proposed change before repository code is modified. Proposed changes must be exact (e.g. the specific file and the specific change to make), not a restated intent such as "implement the feature" or "add test infrastructure."

Proposed code may be included inside the Implementation Plan. Do not apply the proposed changes while planning.

## Milestone Type Boundaries

### FOUNDATION (conditional)

Create a FOUNDATION Implementation Plan only when the milestone approved for this Implementation Plan is itself a FOUNDATION milestone, as recorded in `Plan.md`. FOUNDATION milestones exist only for a genuine executable prerequisite that prevents a RED milestone this FOUNDATION serves (as recorded in `Plan.md`) from meaningfully beginning — not merely because the production class, service, repository, controller, method, or behavior under test does not yet exist (that absence may itself be valid RED evidence; see RED below).

A FOUNDATION Implementation Plan must:

- identify the exact prerequisite preventing meaningful RED (e.g. missing build/dependency setup, missing test infrastructure, missing required module/project structure, missing configuration, missing bootstrap/infrastructure);
- identify the exact files/artifacts allowed to change;
- contain the minimum setup required — nothing more;
- explicitly exclude the target feature/business behavior; do not propose production scaffolding for the behavior RED is meant to drive;
- list, as explicit decisions for human review with their alternatives, every choice that binds the RED milestones this FOUNDATION serves and that those RED milestones cannot change themselves — for example test tooling, test libraries, test clients, and the test-isolation mechanism;
- define Acceptance/Completion Criteria and verification proving the prerequisite is established and every RED milestone this FOUNDATION serves can begin;
- stop after verification — do not propose RED, GREEN, or REFACTOR work in the same Implementation Plan. FOUNDATION never automatically continues into RED; RED is a separate milestone requiring its own RED Implementation Plan and human approval.

If the milestone approved for this Implementation Plan is a RED milestone with no preceding FOUNDATION milestone recorded in `Plan.md`, propose RED directly.

### RED

- propose test/check changes only — or, when `Plan.md` names an existing failing test as this milestone's RED evidence, propose no file changes (see below);
- identify why the expected failure demonstrates missing approved behavior;
- state the expected RED failure as a class of failure attributable to the missing behavior, not as one exact value the missing implementation happens to produce;
- map every normative rule of the approved contract that this milestone verifies to a test, or list it as not tested with the reason; never test behavior the contract leaves undefined;
- a test that asserts only that something does not happen (no event, call, write, or message) passes vacuously while the behavior is absent, so it is not RED evidence; in the same test, first exercise the positive case that proves the behavior is active, then assert the negative, so the test fails in RED for the missing behavior and still proves the negative after GREEN;
- do not propose production implementation.
- In statically typed languages, RED may include a compilation failure when that failure is directly caused by an intentionally absent production type, method, or signature required by the approved behavior (for example, a test referencing `UserService` failing to compile because `UserService` does not exist yet). Do not create production-source scaffolding merely to make RED tests compile. Unrelated compilation, configuration, dependency, or environment failures are not valid RED evidence.

When `Plan.md` names an existing failing test as this milestone's RED evidence:

- list no files to create or modify; the Exact Code requirement does not apply because no file changes;
- show, from the requirement or contract, that every assertion in the named test expresses approved behavior — if any assertion does not, stop and return to planning, because the work is OTHER, not RED;
- record the test's current failure on the unmodified baseline and why it is the missing approved behavior, not an unrelated failure;
- the Acceptance / Completion Criteria are that the named test fails for that reason on execution, and that no file changed.

### GREEN

- require valid predecessor RED evidence when the PDD workflow applies;
- propose the smallest production change needed for the approved RED evidence;
- do not include unrelated refactoring or future milestone work.

### REFACTOR

- require a verified GREEN baseline — the preceding GREEN milestone's evidence, or for a standalone REFACTOR (`prompt-driven-development` Standalone REFACTOR) the full verification suite passing on the unmodified repository, recorded in the plan before any change;
- name the existing tests that protect the code being restructured; if they do not cover the behavior the change could break, stop and return to planning for a characterization-test OTHER milestone;
- propose behavior-preserving changes only;
- do not add new externally observable behavior.

### OTHER

- confirm `Plan.md` records why no requirement this milestone owns adds or changes production behavior;
- record the baseline evidence `Plan.md` names (for example a failure rate, a timing, or the configuration in use) by observing it on the unmodified repository before proposing changes;
- propose only the approved changes — tests, build, configuration, tooling, or infrastructure — with no production behavior change;
- name the existing tests that prove behavior is preserved and must pass after the milestone;
- never weaken or remove a test assertion without a same-coverage replacement in the same plan;
- the Acceptance / Completion Criteria are the completion evidence measured against the recorded baseline plus the preserved tests passing;
- if a production behavior change turns out to be needed, stop and return to planning for RED and GREEN.

For database work, include data migration, compatibility, deployment ordering, and rollback/recovery where relevant.

For distributed changes, include idempotency, concurrency, retries, and partial failure where relevant to the approved scope.

Do not implement while creating the Implementation Plan.
Do not approve the Implementation Plan on behalf of a human reviewer.

## Dependency and Version Selection

When an Implementation Plan introduces or changes a dependency, framework, plugin, or tool version:

- choose a release that is currently supported by its maintainers and compatible with the approved technology stack;
- cite the source used to confirm support and compatibility;
- never choose a version because it is already in a local cache, offline, or otherwise convenient in the current environment — environment availability is an execution concern, not a selection criterion;
- if current support cannot be verified, ask a focused clarification question and stop instead of choosing.

## Carried-Forward Decisions

Decisions recorded in earlier approved Implementation Plans are approved inputs to every later Implementation Plan. List the ones this milestone relies on, cite the Implementation Plan that approved each, and do not reopen or silently change them. Changing one requires the user's explicit approval, recorded in the new Implementation Plan together with its reason.

## Pre-authorized Contingencies

An Implementation Plan may pre-authorize a contingency only in a dedicated Pre-authorized Contingencies section. Each contingency states an exact observable trigger, the exact file, and the exact change. Nothing broader is authorized: a change to the approach, an additional file, or an additional dependency that is not listed returns to planning for re-approval. A contingency may never remove, loosen, or otherwise weaken a test assertion or an Acceptance / Completion Criterion — relaxing a check because it fails changes the evidence rather than the code; a failing check stops execution and returns to planning. Execution reports, for each contingency, whether its trigger occurred and whether it was applied.

## File Scope and Plan Status

Acceptance criteria that limit which files may change always exclude the milestone's own Execution Status update in `Plan.md`, which the PDD workflow performs after verified execution.

## Repeatable, Isolated Verification

When tests touch persistent state (files, databases, caches, temporary directories) or override configuration, a single passing run is not sufficient evidence. Verification must show the result is repeatable and isolated: run the verification commands a second time without cleaning between runs, and have tests that override configuration assert the effective value actually in force, not only the outcome that depends on it.

Verification must not silently depend on a shared resource being available. Prefer dynamically allocated resources unless the approved artifacts explicitly require a fixed one.

## Planning-Time Dry Run

Before presenting an Implementation Plan for review, apply its exact code in a disposable copy of the repository outside the working tree and run the plan's verification commands there. Correct the plan from what the dry run shows — for example diff hunks that do not apply, verification commands the build cannot run, or claims about library or framework behavior that the output contradicts.

- For RED, also show the tests are sound: compile them against a scratch-only stub of the approved signatures, or apply a scratch-only probe of the smallest production change, and confirm the new tests fail without the behavior and can pass with it. For RED whose evidence is an existing failing test, apply the probe and confirm that test passes with it. The stub or probe never enters the repository.
- Record the result in the plan, labeled as a planning-time dry run that is not milestone evidence. The milestone's evidence comes only from execution after approval.
- Never modify the repository during a dry run, and delete the disposable copy afterward.
- If a dry run cannot be performed, state why in the plan.

## Pre-existing Failures

A check that fails on the unmodified baseline — a flaky or already-broken test outside this milestone's scope — is a finding, not noise. A test `Plan.md` names as this milestone's own subject — the existing failing test serving as RED evidence, or the test an OTHER milestone fixes — is in scope, not a pre-existing failure.

- Establish it with evidence on the baseline (for example repeated isolated runs of the single test), report it, and ask the user before approval how the Acceptance / Completion Criteria treat it. Do not decide this during execution.
- The only acceptable non-blocking form names the exact test, records its result in the milestone evidence, and accepts a run only when that named test is the sole failure.
- Never rerun verification until it happens to pass, and never skip, disable, or weaken the test to make the milestone pass. Fixing it is separate work.

## Exact Code

An Implementation Plan is reviewed as the exact code that will be written. For every file in scope it contains the complete final content of a created file, and for a modified file either its complete final content or a complete unified diff covering every changed line with enough context to apply mechanically. Pseudocode, placeholders, ellipses, "unchanged" gaps, and partial fragments are not allowed for any code, test, configuration, or build file that will be written.

Path patterns — ignore rules, globs, and configured file or directory paths — must match only what they are intended to match; anchor a pattern to the repository root when it is meant for a root-level path.

Every dependency, plugin, and configuration setting the exact code introduces must trace to an approved artifact or to an explicit decision listed in the Implementation Plan for review. A setting that appears only in the code is a defect.

The Proposed Changes list and the code must match exactly: every change the code makes is named in Proposed Changes, and every change named there appears in the code. A change that appears only in the code, or only in the list, is a defect.

Before stopping, check each file in scope: complete content or a complete diff is present, it contains no placeholder or pseudocode, it matches the Proposed Changes list, and every dependency, plugin, and configuration setting it introduces is traced. Report the result per file.
