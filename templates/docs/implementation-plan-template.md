# Implementation Plan: <Milestone Name>

**Date:** YYYY-MM-DD
**Plan:** `docs/.ai/Plan.md`
**Milestone:** <number and name>
**Status:** Draft | Approved | Implemented

## Milestone Description

<Approved behavior delivered by this milestone.>

Only include work required to satisfy this milestone.

Do not introduce files, dependencies, configuration, abstractions, tests,
or behavior that belong to later milestones.

## Current Repository State

- <Relevant existing source, tests, contracts, and configuration>

## Files to Create or Update

| File | Change | Reason |
|---|---|---|
| `path/to/file` | Create / Update | <why required> |

## Build/Test Harness Prerequisite

<Not applicable, or list only the minimum build/test infrastructure that
must exist before a meaningful RED test can execute.>

This section may include build and test infrastructure only.

It must not include application behavior.

## Tests First — RED

A build-tool failure, malformed test, missing unrelated dependency, or invalid test setup does not count as valid RED.

### Test Files

- `path/to/test`

### Test Cases

1. **Positive:** <expected behavior>
2. **Negative:** <validation or failure behavior>
3. **Boundary/edge:** <only when explicitly required or necessary for correctness>

### Expected RED Result

- Command: `<focused test command>`
- Expected failure: <specific assertion or missing behavior>
- Why this is valid RED: <why setup is correct and failure proves implementation is missing>

## Production Code — GREEN

### Exact Changes

- `path/to/source`
  - <class/function/configuration change>
  - <logic and error behavior>
  - <comments only where reasoning is non-obvious>

### Architecture and Operational Decisions

- Transaction boundary: <decision or not applicable>
- Idempotency/order: <decision or not applicable>
- Dependency failure behavior: <fail fast, fail closed, retry, queue, degrade, or not applicable>
- Observability: <logs, metrics, traces required by this milestone>
- Security/compliance: <decision or not applicable>

### Expected GREEN Result

- Focused command: `<command>`
- Broader command: `<command>`

## Refactor After GREEN

- <Specific cleanup allowed after tests pass>
- <Behavior and contracts that must remain unchanged>

## Out of Scope

- <Anything intentionally excluded from this milestone>

## Success Criteria

- [ ] RED was observed for the expected reason
- [ ] Minimal implementation makes focused tests GREEN
- [ ] Relevant regression suite is GREEN
- [ ] Refactoring preserves GREEN
- [ ] No files outside this plan were changed without plan update

## Review Record

- Reviewer: <name or role>
- Decision: Pending | Approved | Changes Requested
- Notes: <review feedback>
