# Workflow: Fix a Bug Safely

## Purpose

Diagnose and fix a defect with a reproducible RED milestone, a separately reviewed minimal GREEN fix, and optional separately reviewed refactoring.

## 1. Reproduce and Bound the Defect

Collect evidence:

- observed and expected behavior
- reproducible input/event when available
- affected environment and adapter selection when relevant
- correlation ID, logs, metrics, or trace when available
- affected contract and regression risk

Do not change code while the defect or expected behavior is materially ambiguous.

## 2. Update and Review the Plan

Add separate milestones such as:

1. `<Defect> Regression Test — RED`
2. `<Defect> Minimal Fix — GREEN`
3. `<Defect> Refactor — REFACTOR` only when justified

The Plan must describe impact, reproduction, expected behavior, scope/exclusions, predecessor relationships, and success criteria. Obtain approval.

## 3. RED Milestone — Plan and Reproduce

Create a RED Implementation Plan with:

- exact regression test/check file
- expected approved behavior
- focused command
- expected RED assertion
- test support required to reproduce the defect
- out-of-scope work

Do not include the source fix or refactoring design.

Obtain approval, execute with `/generate-tests`, and confirm failure is caused by the reported defect. A broken fixture or unrelated environment failure is not valid RED. Stop after recording valid RED.

## 4. Diagnose Root Cause

Use the established RED reproduction and current code to identify the supported root cause. Distinguish as applicable:

- incorrect business logic
- missing validation
- transaction/rollback issue
- duplicate/ordering issue
- configuration/adapter-selection issue
- race condition
- provider-specific behavior

Do not widen scope beyond the approved defect. If diagnosis reveals a materially different requirement or larger problem, update the Plan before continuing.

## 5. GREEN Milestone — Plan and Implement the Minimal Fix

Create a separate GREEN Implementation Plan that references the RED evidence and defines:

- root cause supported by current code/evidence
- exact production files
- minimum source change
- transaction/concurrency/idempotency impact where applicable
- observability update only when required to diagnose recurrence and supported by scope
- focused/regression commands
- explicit exclusions

Obtain approval, then execute with `/implement-approved-plan`:

- change only approved files
- preserve unrelated behavior
- avoid cleanup/new features
- run regression test and relevant suite
- record GREEN evidence
- stop after GREEN

## 6. Optional REFACTOR Milestone

Only when a concrete maintainability/design issue remains after the fix:

- add a separate REFACTOR milestone
- create and approve its Implementation Plan
- start from verified GREEN
- perform behavior-preserving cleanup only
- rerun focused and relevant regression tests

Do not hide additional bug fixes inside refactoring.

## 7. Operational Follow-Up

When the approved scope includes improving detectability, add the smallest appropriate log, metric, trace attribute, or alerting signal. Do not log secrets or sensitive payloads.

## Completion Criteria

- [ ] Reproduction and expected behavior are documented
- [ ] RED regression milestone was observed failing for the expected defect
- [ ] GREEN fix had a separately reviewed Implementation Plan
- [ ] Minimal fix made the regression test GREEN
- [ ] Relevant regression suite is GREEN
- [ ] Any refactor was a separate justified milestone and preserved behavior
- [ ] Root cause and residual risk are recorded
