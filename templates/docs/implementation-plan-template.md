# Implementation Plan: <Milestone Name>

**Date:** YYYY-MM-DD  
**Plan:** `docs/.ai/Plan.md`  
**Milestone:** <number and name>  
**Phase:** FOUNDATION | RED | GREEN | REFACTOR | OTHER  
**Status:** Draft | Approved | Implemented

## Milestone Description

<Approved outcome delivered by this milestone only.>

Only include work required to satisfy this milestone. Do not introduce files, dependencies, configuration, abstractions, tests, implementation, or behavior that belong to a later milestone.

## Preconditions and Predecessor Evidence

- Required predecessor milestone: <milestone or none>
- Required evidence: <valid RED, GREEN baseline, approved contract, or not applicable>
- Evidence reviewed: <command/result or not yet available while Draft>

## Current Repository State

- <Relevant existing source, tests, contracts, configuration, and prior milestone output>

## Files to Create or Update

| File | Change | Reason |
|---|---|---|
| `path/to/file` | Create / Update | <why required by this milestone> |

## Phase-Specific Execution Plan

Complete **only the section matching the milestone Phase**. Mark other sections `Not applicable — different milestone phase`.

### FOUNDATION / OTHER

Use only for an approved non-behavior milestone.

- Exact changes: <build/test foundation, contract artifact, documentation/tooling change, etc.>
- Executable verification: <command/check>
- Behavior explicitly excluded: <future application behavior>

A project/test foundation may include only the minimum build/runtime/test infrastructure needed for later meaningful tests. It must not implement application behavior or preload later-milestone dependencies.

### RED — Tests/Checks Only

#### Test or Check Files

- `path/to/test`

#### Approved Cases

1. **Positive:** <approved expected behavior>
2. **Negative:** <approved validation/failure behavior>
3. **Boundary/edge:** <only when explicitly required or necessary for correctness>

#### Test Support

- <fixtures/fakes/test-only configuration required to execute the approved test; no production behavior>

#### Expected RED Result

- Command: `<focused test/check command>`
- Expected failure: <specific assertion or missing behavior>
- Why this is valid RED: <why setup is correct and failure proves approved behavior is missing>

#### RED Restrictions

- No production implementation changes.
- No future GREEN design beyond what is necessary to identify the behavioral boundary being tested.
- No refactoring.

### GREEN — Minimal Production Implementation

#### Required RED Evidence

- Predecessor RED milestone: <number/name>
- RED command/result: <recorded valid RED evidence>

#### Exact Production Changes

- `path/to/source`
  - <class/function/configuration change required by approved behavior>
  - <logic and error behavior>
  - <comments only where reasoning is non-obvious>

#### Architecture and Operational Decisions

Document only decisions applicable to this milestone and already supported by approved requirements/architecture:

- Transaction boundary: <decision or not applicable>
- Idempotency/order/concurrency: <decision or not applicable>
- Dependency failure behavior: <decision or not applicable>
- Adapter selection: <decision or not applicable>
- Observability: <decision or not applicable>
- Security/data classification/compliance: <decision or not applicable>

#### Expected GREEN Result

- Focused command: `<command>`
- Broader relevant command: `<command>`

#### GREEN Restrictions

- No new requirements or later-milestone behavior.
- No unrelated test expansion.
- No speculative architecture or dependency additions.
- No refactoring; use a separately approved REFACTOR milestone when justified.

### REFACTOR — Behavior-Preserving Cleanup

#### Required GREEN Baseline

- Predecessor GREEN milestone: <number/name>
- Baseline command/result: <focused and relevant regression evidence>

#### Concrete Refactoring Need

- <duplication, naming, cohesion, dependency direction, readability, or testability issue>

#### Exact Refactoring Changes

- `path/to/source`
  - <approved structural change>

#### Behavior That Must Remain Unchanged

- <API/event/persistence/configuration/error/security behavior>

#### Verification

- Focused command before: `<command/result>`
- Focused command after: `<command>`
- Broader relevant command after: `<command>`

#### REFACTOR Restrictions

- No feature behavior.
- No defect fixes.
- No contract changes.
- No new requirement implementation.

## Out of Scope

- <Anything intentionally excluded from this milestone>

## Success Criteria

Use only criteria relevant to the selected Phase.

- [ ] Approved milestone scope only was executed
- [ ] Required predecessor evidence exists
- [ ] Phase-specific command/check produced the expected result
- [ ] No later-milestone work was pulled forward
- [ ] No files outside this plan were changed without a plan update

## Execution Evidence

Complete after execution without changing the approved scope:

- Commands run: <commands>
- Results: <summarized observed results>
- Files actually changed: <list>
- Deferred/out-of-scope work: <list or none>

## Review Record

- Reviewer: <name or role>
- Decision: Pending | Approved | Changes Requested
- Notes: <review feedback>
