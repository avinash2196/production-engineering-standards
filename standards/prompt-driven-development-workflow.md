# Prompt-Driven Development Workflow

## Purpose

This standard defines the required lifecycle for AI-assisted implementation work. It separates requirements, planning, tests, implementation, and refactoring into small human-controlled boundaries so each stage can be reviewed independently before the agent advances.

The high-level workflow is:

> **Requirements → Plan → Human Review → Implementation Plan → Human Review → RED Tests → GREEN Code → Refactor → Final Review**

In this repository, that high-level sequence is implemented through **separate Plan milestones for RED, GREEN, and optional REFACTOR work**. Each repository-changing milestone receives its own Implementation Plan and human review before execution.

A prompt is not approval to skip planning. A Plan is not approval to generate code. Approval of a RED milestone is not approval to implement GREEN. Passing tests are not approval to perform an unplanned refactor.

## When This Workflow Applies

Use the complete workflow when work does any of the following:

- adds or changes production behavior
- changes an API, event, persistence, or integration contract
- touches four or more files
- adds a new service, module, adapter, or shared standard
- fixes a defect that could regress
- changes reliability, security, compliance, or transaction behavior

For documentation-only or configuration-only work, use the same planning gates when the change is non-trivial. The executable RED/GREEN evidence may be a repository validator, linter, schema check, configuration test, or another relevant check instead of a unit test.

## Phase 0 — Review Requirements and Current State

Before creating a Plan:

1. Read the requirement or user request.
2. Read relevant source, tests, contracts, configuration, and standards.
3. Apply the repository requirements-analysis guidance when available.
4. Identify ambiguities that materially affect behavior, contracts, data handling, security/compliance, persistence/integration behavior, testing, or milestone boundaries.
5. Do not invent API behavior, business rules, infrastructure, compliance obligations, security mechanisms, or non-functional requirements.

If a material ambiguity remains, ask numbered clarification questions only and do not create or update the Plan. Do not use framework defaults, common architecture practice, or industry assumptions to resolve a material requirement gap.

## Phase 1 — Create the Plan

Create:

```text
docs/.ai/Plan.md
```

The Plan defines **what** will be delivered and the human-controlled milestone sequence.

### Milestone Model

PDD milestones are intentionally small execution boundaries. For behavior-changing work:

- **RED is a separate milestone** that creates or updates tests/checks only and proves the approved behavior is missing.
- **GREEN is a separate milestone** that implements only the minimum approved production behavior required to satisfy the preceding RED milestone.
- **REFACTOR is a separate milestone when refactoring is justified.** It is optional and must preserve the established GREEN behavior.

A phase milestone must trace to an approved requirement or behavior. Do not create RED, GREEN, or REFACTOR milestones merely to add ceremony or independent scope.

A Plan may also contain non-behavior milestones such as a project/test foundation or an approved contract artifact when those are real deliverables. Any milestone that changes repository files must still be independently planned and reviewed before execution.

Example:

```text
Milestone 1 — Project and Test Foundation
Milestone 2 — Document Validation Tests — RED
Milestone 3 — Document Validation Implementation — GREEN
Milestone 4 — Document Validation Refactor — REFACTOR   # only if justified
Milestone 5 — Persistence Tests — RED
Milestone 6 — Persistence Implementation — GREEN
```

Keep milestones small and independently reviewable. Do not pull configuration, dependencies, abstractions, infrastructure, tests, or behavior from a later milestone into an earlier milestone merely because later work may need it.

The Plan must include:

- objective and scope
- current-state summary
- requirements and constraints
- milestone sequence, including phase identity where applicable
- dependencies and predecessor relationships
- risks
- items explicitly out of scope
- success criteria

The Plan must not contain complete production code. It may identify likely components, but exact repository changes belong in the milestone Implementation Plan.

### Gate 1 — Human Review

Do not create the first milestone Implementation Plan until the Plan is reviewed and approved.

An end-to-end implementation request does **not** waive this gate or the per-milestone review gates below for behavior-changing work.

## Phase 2 — Create One Milestone Implementation Plan

For the next approved milestone, create:

```text
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
```

The Implementation Plan defines **how that one approved milestone will be executed**. It must identify the milestone phase and contain only work permitted for that phase.

### RED Milestone Implementation Plan

A RED Implementation Plan may define:

- exact test/test-support files to create or update
- approved positive, negative, and necessary boundary behavior
- test fixtures, fakes, or test-only configuration required to execute the tests
- focused command
- expected failure and why it proves the approved behavior is missing
- out-of-scope items and success criteria

It must **not** define or authorize production implementation or future refactoring.

### GREEN Milestone Implementation Plan

A GREEN Implementation Plan may define:

- predecessor RED milestone and recorded valid RED evidence
- exact production files to create or update
- minimum logic required to satisfy the approved behavior
- applicable transaction, idempotency, dependency-failure/degradation, adapter, security, and observability decisions already supported by requirements/approved architecture
- focused and regression verification commands
- out-of-scope items and success criteria

It must **not** authorize unrelated test expansion, speculative future architecture, or refactoring.

### REFACTOR Milestone Implementation Plan

A REFACTOR Implementation Plan may define:

- predecessor GREEN milestone and GREEN baseline evidence
- exact files and structural changes allowed
- concrete smell, duplication, cohesion, readability, or boundary issue being addressed
- behavior/contracts that must remain unchanged
- focused and regression verification commands
- out-of-scope items and success criteria

It must **not** introduce new observable behavior, feature work, or defect fixes.

### FOUNDATION / OTHER Milestones

A non-behavior milestone must define only the files and executable checks needed for its approved outcome. It must not pull future RED, GREEN, or REFACTOR scope forward.

### Gate 2 — Human Review

Do not execute a milestone until its Implementation Plan is reviewed and approved.

Approval applies only to that milestone. Completing a RED milestone does not authorize GREEN until the GREEN Implementation Plan is separately created and approved. Completing GREEN does not authorize REFACTOR until a REFACTOR milestone exists, is justified, and its Implementation Plan is separately approved.

## Bootstrap Exception for a New Project

When a repository does not yet have an executable build and test harness, a **Project/Test Foundation** milestone may create the minimum infrastructure required to execute meaningful tests.

Examples include:

- build descriptor such as `pom.xml` or `build.gradle`
- minimum compiler/runtime configuration
- test framework dependency
- test source structure

This foundation milestone must not implement application behavior or pre-install dependencies needed only by later milestones.

A failure caused only by a missing or broken build harness does not count as valid RED.

## Phase 3 — Execute a RED Milestone

For an approved RED milestone:

1. Modify only test/test-support files authorized by the RED Implementation Plan.
2. Express only approved behavior.
3. Run the smallest relevant test/check command.
4. Confirm failure is caused by the expected missing behavior, not syntax, broken setup, unavailable unrelated infrastructure, or an incorrect test.
5. Record the command, observed failure, and why RED is valid.
6. Stop after RED. Do not edit production implementation.

A test that unexpectedly passes does not establish RED. Determine whether the behavior already exists or the test is ineffective, and return to planning when scope or assumptions need to change.

## Phase 4 — Execute a GREEN Milestone

A GREEN milestone may begin only when:

- its predecessor RED milestone is complete;
- valid RED evidence is available; and
- the GREEN Implementation Plan is separately reviewed and approved.

Then:

1. Modify only production files authorized by the GREEN Implementation Plan.
2. Implement the smallest behavior required to satisfy the approved tests/behavior.
3. Do not add speculative abstractions, unrelated cleanup, new requirements, or future-milestone work.
4. Run the focused tests/checks, then the broader relevant regression suite.
5. Record commands and summarized results.
6. Stop after GREEN. Do not refactor unless a separate approved REFACTOR milestone exists.

GREEN means the approved behavior passes and relevant existing behavior has not regressed.

## Phase 5 — Execute a REFACTOR Milestone When Needed

Refactoring is optional. Create a separate REFACTOR milestone only when there is concrete cleanup or design improvement worth reviewing independently.

A REFACTOR milestone may begin only from a verified GREEN baseline and after its own Implementation Plan is approved.

During refactoring:

- preserve public behavior and contracts
- perform only the structural changes listed in the approved REFACTOR Implementation Plan
- remove duplication or improve naming/boundaries only where justified
- keep each refactor small and reviewable
- run focused tests after every meaningful refactor and the broader relevant suite at the end
- do not add feature behavior or defect fixes

If refactoring exposes missing behavior, stop and return to Plan → RED milestone → GREEN milestone rather than silently expanding scope.

## Phase 6 — Final Review

Complete all applicable checks:

- Plan matches delivered scope and milestone order
- every executed repository-changing milestone has its own approved Implementation Plan
- GREEN milestones have predecessor valid RED evidence where behavior changed
- REFACTOR milestones started from GREEN and preserved behavior
- focused and broader relevant tests/checks are GREEN
- implementation did not pull later-milestone scope forward
- repository validators and static checks pass
- documentation and enforcement matrix are updated when standards changed
- remaining risks or deferred work are documented

## Evidence to Preserve

For reviewable work, retain:

- approved Plan
- approved phase-specific Implementation Plans
- RED test/check names, command, and summarized expected failure
- GREEN command/result
- REFACTOR before/after GREEN evidence when a refactor milestone exists
- final changed-file list for each milestone
- deferred or out-of-scope work

Do not retain private chain-of-thought. Preserve decisions, evidence, and outcomes only.

## LLM Instructions

- Never collapse Plan and Implementation Plan into one artifact for qualifying work.
- Never combine RED and GREEN authorization in one behavior-changing Implementation Plan.
- Never treat approval of a RED milestone as approval to write production code.
- Never refactor under a GREEN milestone; use a separate approved REFACTOR milestone when refactoring is justified.
- Never generate production implementation during planning or RED.
- Do not advance to the next phase milestone until its own Implementation Plan is approved.
- If the user changes scope, update the Plan and the affected milestone Implementation Plan before continuing.
- For documentation or tooling changes, use the most relevant executable validator as RED/GREEN evidence when ordinary unit tests are not applicable.

## Review Checklist

- [ ] Requirements and current state were reviewed before planning
- [ ] Material ambiguity was clarified instead of guessed through
- [ ] `docs/.ai/Plan.md` exists and was reviewed
- [ ] Behavior-changing work uses separate RED and GREEN milestones
- [ ] REFACTOR is a separate milestone only when justified
- [ ] Each repository-changing milestone has its own approved Implementation Plan
- [ ] RED Implementation Plans authorize tests/checks only
- [ ] GREEN Implementation Plans reference valid predecessor RED evidence
- [ ] RED failure was caused by the missing approved behavior
- [ ] Minimal GREEN implementation stayed inside its approved milestone
- [ ] REFACTOR work, when present, started from GREEN and preserved behavior
- [ ] Full relevant test/validation suite passes
- [ ] No unapproved requirements or later-milestone work were added early
- [ ] Bootstrap work, when required, was limited to the minimum build/test foundation

## References

- [Agent Execution Standard](agent-execution.md)
- [Definition of Done](definition-of-done.md)
- [Unit Testing](testing/unit-testing.md)
- [Integration Testing](testing/integration-testing.md)
