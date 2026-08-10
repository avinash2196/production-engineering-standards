# Code Review Standard

## Purpose

Define how production code changes are reviewed for correctness, safety,
maintainability, and operational risk.

Code review is risk-based. Its primary purpose is to prevent defects and
unsafe changes from reaching production, not to maximize checklist compliance.

## Review Priority

Review in this order:

1. Correctness and business behavior
2. Data integrity, transactions, concurrency, and idempotency
3. API, event, persistence, and compatibility contracts
4. Security and privacy
5. Dependency and failure behavior
6. Resource usage, performance, and scalability risks
7. Testing quality and regression protection
8. Observability and operability
9. Architecture and maintainability
10. Naming and style not already enforced automatically

Correctness and production safety take precedence over style.

## Scope

Review the supplied diff together with enough surrounding code to understand
the changed execution path.

When available, also review:

- requirements
- approved Plan
- approved Implementation Plan
- relevant tests
- API/event contracts
- configuration changes
- database migrations
- dependency changes

Do not require unrelated legacy cleanup as part of the current change.

## Finding Classification

Every finding is classified as:

- `AUTOMATED` — executable tooling can verify the violation.
- `REVIEWED` — correctness requires engineering judgment or surrounding context.
- `ADVISORY` — preferred engineering guidance with a defensible exception.

## Severity

- `CRITICAL` — credible risk of severe security/privacy exposure, irreversible
  data loss/corruption, or catastrophic production failure. Blocks merge.
- `HIGH` — material correctness, contract, reliability, security, or
  operational defect. Blocks merge.
- `MEDIUM` — meaningful maintainability, testability, performance, or
  operability risk that should normally be addressed before merge.
- `LOW` — non-blocking improvement.

Severity is based on impact and likelihood, not on the number of standards violated.

## Required Review Areas

### Correctness

Verify:

- behavior matches approved requirements
- edge and error paths are correct
- null/empty/boundary conditions are handled where applicable
- state transitions and invariants remain valid
- failure paths do not report success incorrectly

### Data, Transactions, and Concurrency

When applicable verify:

- transaction boundaries
- rollback behavior
- atomicity
- duplicate handling
- idempotency
- ordering
- race conditions
- lost updates
- thread safety
- bounded queues/executors
- consistency across database and messaging operations

### Contract Compatibility

Review changes to:

- HTTP APIs
- event/message schemas
- persistence schemas
- configuration contracts

Identify backwards-incompatible changes and required migration behavior.

### Security and Privacy

Review:

- authentication and authorization
- input validation
- injection risks
- sensitive-data exposure
- secrets
- logging
- least privilege
- dependency vulnerabilities where evidence exists

### Dependency Failure

For remote or external dependencies review:

- timeout behavior
- retry safety
- idempotency implications
- backpressure
- circuit breaking where justified
- durable queueing where justified
- fail-fast/fail-closed/degraded behavior
- recovery behavior

Do not require a universal resiliency pattern.

### Performance and Resource Safety

Review when relevant:

- N+1 access
- unbounded collections
- unbounded queues
- thread/executor usage
- blocking calls on constrained execution models
- large payloads
- unnecessary repeated remote/database operations
- resource/connection leaks

Do not report speculative micro-optimizations without evidence.

### Testing

Verify that tests protect the changed behavior and important failure paths.

Look for missing tests involving:

- negative behavior
- boundaries
- duplicate/concurrent execution
- rollback
- dependency failure
- compatibility

Do not require implementation-detail tests.

### Operability

Verify changed behavior can be diagnosed where operationally important.

Review:

- useful structured logging
- correlation/trace context
- relevant metrics
- health behavior
- failure/degradation visibility

Do not require telemetry merely as boilerplate.

## Evidence Rules

Every finding must include:

- exact file and line or symbol
- triggering condition or execution path
- concrete impact/risk
- applicable requirement, contract, or standard when one exists
- smallest safe correction
- verification needed to prove the correction

A real correctness defect may be reported even when no repository standard
explicitly names it.

Do not invent evidence.

If available context is insufficient, state:

`NEEDS VERIFICATION`

and identify the missing evidence.

## Diff Discipline

Distinguish:

- defects introduced by the current change
- existing defects made worse by the change
- unrelated pre-existing issues

Do not block a focused PR on unrelated legacy cleanup unless the current
change makes that existing risk materially worse.

## Review Integrity

Never:

- manufacture findings to populate every review category
- claim a command or test passed unless it was executed
- assume an unseen implementation does not exist
- mark an area as passed unless it was actually reviewed
- convert formatter/linter findings into manual review noise
- approve code with unresolved CRITICAL or HIGH findings

## Review Checklist

- [ ] Correctness reviewed before style
- [ ] Transaction/concurrency risks reviewed where applicable
- [ ] Compatibility reviewed for changed contracts
- [ ] Security/privacy reviewed where applicable
- [ ] Failure behavior reviewed for changed dependencies
- [ ] Tests cover important changed behavior and failure paths
- [ ] Findings contain concrete evidence and smallest safe corrections
- [ ] Pre-existing issues are distinguished from introduced issues
- [ ] Uncertainty is stated rather than guessed