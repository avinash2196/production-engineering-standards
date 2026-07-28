# Definition of Done

A milestone is complete only when applicable items are satisfied and evidence is available.

## Planning

- [ ] Requirements and current state were reviewed
- [ ] `docs/.ai/Plan.md` contains the approved milestone and scope
- [ ] The milestone Implementation Plan names exact files, tests, RED expectation, GREEN changes, refactor boundary, exclusions, and commands

## Test → Code → Refactor

- [ ] New or updated tests/checks were created before production implementation
- [ ] RED was observed for the expected missing behavior
- [ ] Minimal production changes made focused tests GREEN
- [ ] Relevant regression tests are GREEN
- [ ] Refactoring occurred only after GREEN and preserved behavior

## Functional and Contract Behavior

- [ ] Approved acceptance criteria pass
- [ ] Positive and negative behavior is covered
- [ ] API/event/persistence contracts remain compatible or the approved breaking change is documented

## Architecture and Reliability

- [ ] Dependency direction and capability boundaries are appropriate to service complexity
- [ ] Transaction, rollback, idempotency, ordering, retry, timeout, and degradation decisions are explicit where applicable
- [ ] Local-only adapters are blocked in production

## Security and Compliance

- [ ] No secrets are committed
- [ ] External input is validated
- [ ] Sensitive data is excluded from ordinary logs
- [ ] Applicable security/compliance controls are tested or reviewed

## Operations

- [ ] Health behavior is appropriate to the runtime
- [ ] Logs, metrics, and traces support the operating model
- [ ] Dependency degradation is observable
- [ ] Deployment and rollback expectations are documented where required

## Documentation and Enforcement

- [ ] Plan and Implementation Plan contain final evidence and changed-file summary
- [ ] Relevant ADRs, integration docs, and enforcement matrix are updated
- [ ] Linters, static checks, repository validators, and CI pass
- [ ] Deferred work and residual risk are explicit

## Integrity Rule

Do not mark an item complete when the command was not run or the evidence was not observed. State “not run,” “not applicable,” or “deferred” honestly.
