---
name: implementation-planning
description: Use when translating one approved Plan milestone and phase into a concrete human-reviewable Implementation Plan based on the current repository state.
---

# Implementation Planning

Create a plan for one milestone and one phase only.

Implementation Planning receives the approved milestone and the already-selected phase (FOUNDATION, RED, GREEN, or REFACTOR) from `Plan.md` — it does not decide which phase a milestone needs. Whether a milestone requires FOUNDATION is a planning decision recorded in `Plan.md`'s `setup required` field for that milestone, made before this skill is applied.

## Current-State Analysis

Before planning:

- read the approved Requirements, Plan, and applicable API/external contract;
- inspect the current repository structure;
- inspect relevant existing source, tests, configuration, and completed milestone work;
- read current Plan execution status;
- verify predecessor evidence and actual repository progress;
- verify that the requested phase matches what `Plan.md` records for this milestone.

Prefer repository evidence over assumed structure or previously proposed implementation.

Do not plan from an assumed project state.

If the repository materially conflicts with authoritative artifacts or predecessor evidence, stop and surface the conflict for human review. If repository evidence contradicts the phase `Plan.md` selected for this milestone (for example, `Plan.md` says setup is not required but a genuine prerequisite is actually missing, or says it is required but the repository already provides it), do not silently plan a different phase — stop and report the mismatch back to planning for a `Plan.md` update and re-approval.

## Implementation Plan Content

Include:

- milestone and phase;
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
- explicit Acceptance / Completion Criteria for this specific phase — what must be true for this FOUNDATION, RED, GREEN, or REFACTOR phase to be considered complete;
- verification commands that demonstrate those criteria;
- expected FOUNDATION, RED, GREEN, or REFACTOR evidence;
- rollback or recovery where relevant;
- risks;
- explicit exclusions.

Acceptance / Completion Criteria and verification are distinct: the criteria state what must be true for the phase to be complete; verification commands and expected evidence demonstrate whether the approved changes actually satisfied those criteria. Verification does not replace stating the criteria explicitly. Do not invent or modify Acceptance / Completion Criteria during execution — that belongs to planning.

The Implementation Plan must contain enough implementation detail for a human to review the proposed change before repository code is modified. Proposed changes must be exact (e.g. the specific file and the specific change to make), not a restated intent such as "implement the feature" or "add test infrastructure."

Proposed code may be included inside the Implementation Plan. Do not apply the proposed changes while planning.

## Phase Boundaries

### FOUNDATION (conditional)

Create a FOUNDATION Implementation Plan only when `Plan.md` has already recorded this milestone's setup required as Yes. FOUNDATION exists for a genuine executable prerequisite that prevents the milestone's RED from meaningfully beginning — not merely because the production class, service, repository, controller, method, or behavior under test does not yet exist (that absence may itself be valid RED evidence; see RED below).

A FOUNDATION Implementation Plan must:

- identify the exact prerequisite preventing meaningful RED (e.g. missing build/dependency setup, missing test infrastructure, missing required module/project structure, missing configuration, missing bootstrap/infrastructure);
- identify the exact files/artifacts allowed to change;
- contain the minimum setup required — nothing more;
- explicitly exclude the target feature/business behavior; do not propose production scaffolding for the behavior RED is meant to drive;
- define Acceptance/Completion Criteria and verification proving the prerequisite is established and RED can now begin;
- stop after verification — do not propose RED, GREEN, or REFACTOR work in the same Implementation Plan. FOUNDATION never automatically continues into RED; RED requires its own RED Implementation Plan and human approval.

If `Plan.md` records this milestone's setup required as No, do not propose a FOUNDATION Implementation Plan; propose RED directly.

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
