---
name: implementation-planning
description: Use when translating one approved Plan milestone into a concrete human-reviewable Implementation Plan based on the current repository state.
---

# Implementation Planning

Create an Implementation Plan for exactly one approved milestone.

Implementation Planning receives one approved milestone and its already-recorded milestone type (FOUNDATION, RED, GREEN, or REFACTOR) from `Plan.md` — it does not decide or change the milestone type; that decision belongs to planning and is fixed once `Plan.md` is approved.

## Current-State Analysis

Before planning:

- read the approved Requirements, Plan, and applicable API/external contract;
- inspect the current repository structure;
- inspect relevant existing source, tests, configuration, and completed milestone work;
- read current Plan execution status;
- read every previously approved Implementation Plan and carry its decisions (versions, mechanisms, conventions, configuration and test-infrastructure choices) forward as approved inputs;
- verify predecessor milestone evidence and actual repository progress;
- verify that the milestone type being planned matches what `Plan.md` records for this milestone.

Prefer repository evidence over assumed structure or previously proposed implementation.

Do not plan from an assumed project state.

A material ambiguity may remain unresolved while no milestone yet depends on a concrete decision about it. Before creating an Implementation Plan for a milestone whose FOUNDATION, RED, GREEN, or REFACTOR work actually depends on resolving that ambiguity, resolve it through the existing PDD clarification/human-review mechanisms rather than carrying it forward unresolved into typed code, test assertions, or configuration. Examples of such ambiguity include field representation, nullability, identifier semantics, precision, validation behavior, persistence representation, or external contract behavior — these examples are illustrative only and do not themselves introduce new requirements. Do not force premature resolution of such decisions during Requirements Capture.

If the repository materially conflicts with authoritative artifacts or predecessor evidence, stop and surface the conflict for human review. If repository evidence contradicts the milestone type `Plan.md` recorded for this milestone (for example, `Plan.md` records this milestone as RED but a genuine prerequisite is actually missing, or records a FOUNDATION milestone that the repository shows is no longer needed), do not silently plan a different milestone type — stop and report the mismatch back to planning for a `Plan.md` update and re-approval.

## Implementation Plan Content

Include:

- milestone, including its milestone type (FOUNDATION, RED, GREEN, or REFACTOR);
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
- explicit Acceptance / Completion Criteria for this specific milestone — what must be true for this FOUNDATION, RED, GREEN, or REFACTOR milestone to be considered complete;
- verification commands that demonstrate those criteria;
- expected FOUNDATION, RED, GREEN, or REFACTOR evidence;
- carried-forward decisions from earlier approved Implementation Plans;
- pre-authorized contingencies, if any;
- rollback or recovery where relevant;
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

- propose test/check changes only;
- identify why the expected failure demonstrates missing approved behavior;
- do not propose production implementation.
- In statically typed languages, RED may include a compilation failure when that failure is directly caused by an intentionally absent production type, method, or signature required by the approved behavior (for example, a test referencing `UserService` failing to compile because `UserService` does not exist yet). Do not create production-source scaffolding merely to make RED tests compile. Unrelated compilation, configuration, dependency, or environment failures are not valid RED evidence.

### GREEN

- require valid predecessor RED evidence when the PDD workflow applies;
- propose the smallest production change needed for the approved RED evidence;
- do not include unrelated refactoring or future milestone work.

### REFACTOR

- require a verified GREEN baseline;
- propose behavior-preserving changes only;
- do not add new externally observable behavior.

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

## Exact Code

An Implementation Plan is reviewed as the exact code that will be written. For every file in scope it contains the complete final content of a created file, and for a modified file either its complete final content or a complete unified diff covering every changed line with enough context to apply mechanically. Pseudocode, placeholders, ellipses, "unchanged" gaps, and partial fragments are not allowed for any code, test, configuration, or build file that will be written.

Path patterns — ignore rules, globs, and configured file or directory paths — must match only what they are intended to match; anchor a pattern to the repository root when it is meant for a root-level path.

The Proposed Changes list and the code must match exactly: every change the code makes is named in Proposed Changes, and every change named there appears in the code. A change that appears only in the code, or only in the list, is a defect.

Before stopping, check each file in scope: complete content or a complete diff is present, it contains no placeholder or pseudocode, and it matches the Proposed Changes list. Report the result per file.
