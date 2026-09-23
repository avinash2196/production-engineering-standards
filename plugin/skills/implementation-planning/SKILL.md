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
- code snippets, pseudocode, or patch-level detail where practical and useful for review;
- explicit Acceptance / Completion Criteria for this specific milestone — what must be true for this FOUNDATION, RED, GREEN, or REFACTOR milestone to be considered complete;
- verification commands that demonstrate those criteria;
- expected FOUNDATION, RED, GREEN, or REFACTOR evidence;
- rollback or recovery where relevant;
- risks;
- explicit exclusions.

Acceptance / Completion Criteria and verification are distinct: the criteria state what must be true for the milestone to be complete; verification commands and expected evidence demonstrate whether the approved changes actually satisfied those criteria. Verification does not replace stating the criteria explicitly. Do not invent or modify Acceptance / Completion Criteria during execution — that belongs to planning.

Expected evidence stated in the Implementation Plan is a prediction, not proof — label it Expected / Predicted — Not Yet Verified. Treat it as verified only when: (1) the milestone has actually been executed; (2) the stated verification commands/checks have actually been run; and (3) the resulting evidence supports the expected outcome. Running a verification command is not sufficient by itself if it fails or produces evidence that contradicts the expected outcome.

The Implementation Plan must contain enough implementation detail for a human to review the proposed change before repository code is modified. Proposed changes must be exact (e.g. the specific file and the specific change to make), not a restated intent such as "implement the feature" or "add test infrastructure."

Proposed code may be included inside the Implementation Plan. Do not apply the proposed changes while planning.

## Milestone Type Boundaries

### FOUNDATION (conditional)

Create a FOUNDATION Implementation Plan only when the milestone approved for this Implementation Plan is itself a FOUNDATION milestone, as recorded in `Plan.md`. FOUNDATION milestones exist only for a genuine executable prerequisite that prevents the following RED milestone from meaningfully beginning — not merely because the production class, service, repository, controller, method, or behavior under test does not yet exist (that absence may itself be valid RED evidence; see RED below).

A FOUNDATION Implementation Plan must:

- identify the exact prerequisite preventing meaningful RED (e.g. missing build/dependency setup, missing test infrastructure, missing required module/project structure, missing configuration, missing bootstrap/infrastructure);
- identify the exact files/artifacts allowed to change;
- contain the minimum setup required — nothing more;
- explicitly exclude the target feature/business behavior; do not propose production scaffolding for the behavior RED is meant to drive;
- define Acceptance/Completion Criteria and verification proving the prerequisite is established and the following RED milestone can now begin;
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
