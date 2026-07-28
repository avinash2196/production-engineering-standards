# Workflow: Refactor a Module

## Purpose

Improve structure without changing external behavior and without using refactoring as a hidden feature-delivery path.

## 1. Define the Refactoring Goal

State the concrete problem:

- mixed responsibilities
- duplicated behavior
- unclear dependency direction
- direct provider coupling
- hard-to-test transaction or mapping logic
- confusing names

A line-count threshold alone is not sufficient justification.

## 2. Plan and Review

For a qualifying refactor, update `docs/.ai/Plan.md` and create a milestone Implementation Plan containing:

- behavior/contracts that must remain unchanged
- exact files
- baseline tests
- characterization tests needed before refactor
- incremental refactor steps
- rollback approach
- success criteria

Obtain approval.

## 3. Establish GREEN Baseline

Run focused and relevant regression tests before editing. If protection is missing:

1. create characterization tests
2. confirm they pass against current behavior
3. do not “improve” behavior in those tests

A failing baseline blocks refactoring unless the failure is explicitly excluded and documented.

## 4. Refactor Incrementally

Perform one coherent change at a time, for example:

- extract business policy from transport code
- introduce a capability contract and wrap the existing provider implementation
- separate persistence mapping from domain behavior
- rename vague concepts
- extract cohesive sub-operations

Run focused tests after each step.

## 5. Do Not Mix Behavior Changes

If a defect or feature is discovered, stop and create a separate Plan/Implementation Plan/RED cycle. Do not silently change API, event, persistence, configuration, security, or error behavior.

## 6. Final Verification

- run full relevant tests
- run formatter/linter/static checks
- review the diff for unrelated changes
- record before/after commands and results

## Completion Criteria

- [ ] Concrete refactoring problem documented
- [ ] Baseline was GREEN
- [ ] Behavior and contracts preserved
- [ ] Each step was small and test-verified
- [ ] No feature or bug fix was mixed into the refactor
- [ ] Final suite and checks are GREEN
