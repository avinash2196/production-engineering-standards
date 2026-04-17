# Workflow: Fix Bug Safely

## Purpose

Step-by-step procedure for diagnosing and fixing a bug without introducing regressions, ensuring the fix is test-verified and observable.

## Prerequisites

- Bug report with reproduction steps or observed symptoms
- Access to service code and logs/metrics

## Steps

### 1. Reproduce the Issue

Before fixing anything:

- Reproduce locally using fallback mode if possible (`FALLBACK_*` toggles)
- If not reproducible locally, identify from logs/metrics:
  - Correlation ID of the failing request
  - Error logs with stack trace
  - Metrics anomalies (error rate spike, latency increase)
- Document the reproduction steps

### 2. Write a Failing Test

**Before writing the fix**, create a test that:

- Exercises the exact code path that produces the bug
- Fails with the current code (proves the bug exists)
- Will pass once the fix is applied
- For unit bugs: write a unit test with appropriate mocks
- For integration bugs: write an integration test with testcontainers or fallback adapters

This is non-negotiable. The test is proof the bug was real and proof the fix works.

### 3. Diagnose Root Cause

- Trace the code path from controller → service → domain → repository
- Check: is this a logic error, data issue, configuration problem, or race condition?
- Check: are abstractions being used correctly? (correct provider, correct semantics)
- Check: is the issue environment-specific? (fallback vs production adapter behavior difference)
- Document the root cause — not just what's wrong, but why it happened

### 4. Implement the Fix

- Fix only the bug. Do not refactor or add features in the same change.
- If the fix requires changing an abstraction contract, assess impact on other consumers.
- If the fix reveals a missing fallback behavior, add the fallback adapter update as a separate change.
- Keep the fix minimal and focused.

### 5. Verify the Fix

- [ ] The failing test from Step 2 now passes
- [ ] All existing tests still pass (no regressions)
- [ ] If the bug was in a hot path, verify no performance degradation

### 6. Add Observability for the Failure Mode

If the bug represents a failure mode that was not previously observable:

- Add or improve structured logging at the failure point
- Add a metric that would detect this failure in the future
- Ensure the correlation ID is present in error logs

### 7. Review

Invoke **code-reviewer** agent patterns. Verify:

- [ ] Fix is minimal (no unrelated changes)
- [ ] New test proves the bug existed and is now fixed
- [ ] No regressions in existing tests
- [ ] Root cause documented (in commit message or ticket)
- [ ] Observability improved for this failure mode

### 8. Commit

Conventional commit: `fix(<service>): <concise description of what was wrong>`

Include in commit body:
- Root cause (one sentence)
- What the fix changes
- Reference to bug ticket if applicable
