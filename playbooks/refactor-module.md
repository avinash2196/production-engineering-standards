# Workflow: Refactor a Module

## Purpose

Improve structure without changing external behavior and without using refactoring as a hidden feature-delivery or defect-fix path.

## 1. Define the Refactoring Goal

State the concrete problem:

- mixed responsibilities
- duplicated behavior
- unclear dependency direction
- direct provider coupling
- hard-to-test transaction or mapping logic
- confusing names

A line-count threshold alone is not sufficient justification.

## 2. Plan a Separate REFACTOR Milestone

For a qualifying refactor:

1. update `docs/.ai/Plan.md` with a distinct `REFACTOR` milestone;
2. identify the predecessor GREEN milestone/baseline being preserved;
3. create a separate REFACTOR Implementation Plan containing only:
   - behavior/contracts that must remain unchanged;
   - exact files;
   - concrete refactoring steps;
   - baseline verification commands;
   - after-change verification commands;
   - rollback/recovery approach when material;
   - success criteria and explicit exclusions;
4. obtain human approval.

Do not include feature behavior or defect fixes in the REFACTOR Implementation Plan.

## 3. Establish the GREEN Baseline

Run focused and relevant regression tests/checks before editing. A failing baseline blocks refactoring unless the failure is explicitly out of scope and the refactor can still be proven safe.

If behavior is not adequately protected, **stop**. Create separate RED and GREEN milestones for characterization/behavior coverage first; do not add characterization tests inside the REFACTOR milestone.

## 4. Refactor Incrementally

Perform only approved structural changes, one coherent step at a time, for example:

- extract business policy from transport code;
- introduce a justified capability boundary around an existing provider;
- separate persistence mapping from domain behavior;
- rename vague concepts;
- extract cohesive sub-operations.

Run focused tests/checks after each meaningful step.

## 5. Do Not Mix Behavior Changes

If a defect or feature is discovered, stop and return to Plan → RED milestone → GREEN milestone. Do not silently change API, event, persistence, configuration, security, or error behavior.

## 6. Final Verification

- run focused and full relevant tests/checks;
- run formatter/linter/static checks when applicable;
- review the diff for unrelated changes;
- record before/after commands and results in the REFACTOR Implementation Plan Execution Evidence section;
- stop at completion of the REFACTOR milestone.

## Completion Criteria

- [ ] Concrete refactoring problem documented
- [ ] Separate REFACTOR milestone and Implementation Plan approved
- [ ] Predecessor baseline was GREEN
- [ ] Behavior and contracts preserved
- [ ] Each step was small and test-verified
- [ ] No feature or bug fix was mixed into the refactor
- [ ] Final relevant suite/checks are GREEN
