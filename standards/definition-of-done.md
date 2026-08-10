# Definition of Done

A milestone is complete only when the criteria for its declared phase are satisfied and evidence is available. Completing one phase milestone does not authorize the next milestone.

## Common Planning Criteria

- [ ] Requirements and current state were reviewed
- [ ] `docs/.ai/Plan.md` contains the approved milestone, phase, scope, and predecessor relationship
- [ ] The current repository-changing milestone has its own approved Implementation Plan
- [ ] The Implementation Plan contains only work permitted for its phase
- [ ] Material ambiguity was clarified rather than guessed through

## RED Milestone Done

- [ ] Milestone phase is RED
- [ ] Only approved test/test-support/executable-check files changed
- [ ] Approved positive and negative behavior is represented
- [ ] Boundary cases are included only when required by the approved behavior/correctness
- [ ] Focused test/check was executed
- [ ] RED was observed for the expected missing behavior
- [ ] Failure was not caused by broken setup, syntax, or unrelated infrastructure
- [ ] No production behavior was implemented
- [ ] RED evidence and changed files were recorded

## GREEN Milestone Done

- [ ] Milestone phase is GREEN
- [ ] Valid predecessor RED evidence exists
- [ ] GREEN Implementation Plan was separately approved after the RED milestone
- [ ] Only approved production/configuration files changed
- [ ] Minimal production changes made the approved behavior GREEN
- [ ] Focused tests/checks are GREEN
- [ ] Relevant regression suite is GREEN
- [ ] No unrelated test expansion, speculative architecture, or later-milestone work was added
- [ ] No refactoring was performed under the GREEN milestone
- [ ] GREEN evidence and changed files were recorded

## REFACTOR Milestone Done

Apply only when a separate REFACTOR milestone is justified.

- [ ] Milestone phase is REFACTOR
- [ ] Verified predecessor GREEN baseline exists
- [ ] REFACTOR Implementation Plan was separately approved
- [ ] A concrete cleanup/design issue justified the milestone
- [ ] Only approved structural changes were made
- [ ] No feature behavior, defect fix, or contract change was introduced
- [ ] Focused and relevant regression tests/checks remained GREEN
- [ ] Before/after evidence and changed files were recorded

## FOUNDATION / OTHER Milestone Done

- [ ] Approved non-behavior outcome was delivered
- [ ] Only files/dependencies/checks required by that milestone were introduced
- [ ] Future application behavior or later-milestone dependencies were not pulled forward
- [ ] Applicable executable validation passed or gaps were documented honestly

## Feature / Capability Completion

A behavior/capability is complete only when its required milestone chain is complete:

- [ ] Required RED milestone(s) completed with valid evidence
- [ ] Corresponding GREEN milestone(s) completed with relevant regression evidence
- [ ] Any justified REFACTOR milestone completed while preserving GREEN
- [ ] Approved acceptance criteria pass
- [ ] API/event/persistence/configuration contracts remain compatible or an approved breaking change is documented
- [ ] Transaction, rollback, idempotency, ordering, retry, timeout, concurrency, and degradation decisions are explicit where applicable
- [ ] Applicable security/privacy/compliance controls are implemented and reviewed/tested
- [ ] Operational behavior is appropriate to the approved runtime/support model
- [ ] Relevant documentation/ADRs/enforcement records are updated when required
- [ ] Linters, static checks, repository validators, and CI pass where applicable
- [ ] Deferred work and residual risk are explicit

## Integrity Rule

Do not mark an item complete when the command was not run or the evidence was not observed. State `not run`, `not applicable`, `needs verification`, or `deferred` honestly.
