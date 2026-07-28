# Workflow: Fix a Bug Safely

## Purpose

Diagnose and fix a defect with a reproducible test, minimal implementation, and separate refactoring.

## 1. Reproduce and Bound the Defect

Collect evidence:

- observed and expected behavior
- reproducible input or event
- affected environment and adapter selection
- correlation ID, logs, metrics, or trace when available
- affected contract and regression risk

Do not change code while the failure is still ambiguous.

## 2. Update the Plan

Add a bug-fix milestone to `docs/.ai/Plan.md` describing:

- user/business impact
- reproduction
- expected behavior
- scope and exclusions
- success criteria

Obtain approval.

## 3. Create the Implementation Plan

Create a milestone-specific Implementation Plan with:

- root-cause hypothesis supported by current code
- exact failing test to add
- expected RED assertion
- minimal source change
- transaction/concurrency/idempotency impact
- observability update only when needed to detect recurrence
- refactoring explicitly separated

Obtain approval.

## 4. RED — Add the Regression Test

Create the smallest test that reproduces the defect:

- unit test for policy/logic defects
- controller/contract test for validation or API defects
- integration test for persistence, transaction, adapter, or concurrency defects

Run it and confirm it fails for the reported defect. A broken fixture or unrelated environment failure is not valid RED.

## 5. Diagnose Root Cause

Trace the real path and document why the defect occurred. Distinguish:

- incorrect business logic
- missing validation
- transaction/rollback issue
- duplicate or ordering issue
- configuration or adapter-selection issue
- race condition
- provider-specific behavior

Do not fix only the symptom when the approved scope covers the root cause.

## 6. GREEN — Implement the Minimal Fix

- change only files named in the Implementation Plan
- preserve unrelated behavior
- avoid cleanup or new features
- run the regression test and relevant suite

## 7. REFACTOR

Only after GREEN:

- improve names or extraction needed to make the fix maintainable
- keep behavior unchanged
- rerun tests after every meaningful change

## 8. Operational Follow-Up

When the defect was not observable, add the smallest appropriate log, metric, trace attribute, or alerting signal. Do not log secrets or sensitive payloads.

## Completion Criteria

- [ ] Reproduction and expected behavior are documented
- [ ] Regression test was observed RED
- [ ] Minimal fix made it GREEN
- [ ] Relevant regression suite is GREEN
- [ ] Refactoring was separate and preserved behavior
- [ ] Root cause and residual risk are recorded
