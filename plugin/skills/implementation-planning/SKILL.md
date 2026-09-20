---
name: implementation-planning
description: Use when translating one approved Plan milestone and phase into a concrete human-reviewable Implementation Plan based on the current repository state.
---

# Implementation Planning

Create a plan for one milestone and one phase only.

## Current-State Analysis

Before planning:

- read the approved Requirements, Plan, and applicable API/external contract;
- inspect the current repository structure;
- inspect relevant existing source, tests, configuration, and completed milestone work;
- read current Plan execution status;
- verify predecessor evidence and actual repository progress.

Prefer repository evidence over assumed structure or previously proposed implementation.

Do not plan from an assumed project state.

If the repository materially conflicts with authoritative artifacts or predecessor evidence, stop and surface the conflict for human review.

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
- verification commands;
- expected RED, GREEN, or REFACTOR evidence;
- rollback or recovery where relevant;
- risks;
- explicit exclusions.

The Implementation Plan must contain enough implementation detail for a human to review the proposed change before repository code is modified.

Proposed code may be included inside the Implementation Plan. Do not apply the proposed changes while planning.

## Phase Boundaries

### RED

- propose test/check changes only;
- identify why the expected failure demonstrates missing approved behavior;
- do not propose production implementation.

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
