# Prompt-Driven Development Workflow

## Purpose

This standard defines the required lifecycle for AI-assisted implementation work. It separates requirements, design decisions, tests, implementation, and refactoring so that each stage can be reviewed independently.

The workflow is:

> **Requirements → Plan → Human Review → Implementation Plan → Human Review → RED Tests → GREEN Code → Refactor → Final Review**

A prompt is not approval to skip planning. A plan is not approval to generate code. Passing tests are not approval to combine unrelated refactoring with a feature.

## When This Workflow Applies

Use the complete workflow when work does any of the following:

- adds or changes production behavior
- changes an API, event, persistence, or integration contract
- touches four or more files
- adds a new service, module, adapter, or shared standard
- fixes a defect that could regress
- changes reliability, security, compliance, or transaction behavior

For a documentation-only or configuration-only change, use the same planning gates. The RED check may be a repository validator, linter, schema check, or configuration test instead of a unit test.

## Phase 0 — Review Requirements and Current State

Before creating a plan:

1. Read the requirement or user request.
2. Read relevant source, tests, contracts, configuration, and standards.
3. Identify ambiguities that materially affect behavior.
4. Do not invent API behavior, business rules, infrastructure, or non-functional requirements.

If a critical ambiguity remains, ask numbered clarification questions only. Otherwise continue.

## Phase 1 — Create the Plan

Create:

```text
docs/.ai/Plan.md
```

The Plan defines **what** will be delivered and in what milestones. It must include:

- objective and scope
- current-state summary
- requirements and constraints
- milestone sequence
- dependencies and risks
- items explicitly out of scope
- success criteria

The Plan must not contain complete production code. It may identify likely components, but exact code belongs in the Implementation Plan.

### Gate 1 — Human Review

Do not create an Implementation Plan until the Plan is reviewed and approved, unless the user explicitly requested end-to-end execution and already supplied the required decisions.

## Phase 2 — Create the Implementation Plan

Create a milestone-specific file:

```text
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
```

The Implementation Plan defines **how** the approved milestone will be delivered. It must include:

- approved Plan milestone being implemented
- current repository state
- exact files to create or update
- exact test cases, including positive and negative behavior
- expected RED failure and why it proves the missing behavior
- exact production-code changes
- transaction, idempotency, dependency-failure/degradation, local-adapter, security, and observability decisions where applicable
- explicit refactoring boundary
- out-of-scope items
- commands and success criteria

The implementation plan must target real existing interfaces and components. It must not introduce placeholders merely to make the plan appear complete.

### Gate 2 — Human Review

Do not edit production source until the Implementation Plan is reviewed and approved.

## Phase 3 — RED: Write Tests First

Create or update test files only.

Tests must:

- express approved behavior from the Implementation Plan
- cover the primary positive and negative cases
- avoid testing invented requirements
- target real production boundaries
- fail for the expected missing behavior, not because of syntax, broken setup, or unrelated defects

Run the smallest relevant test command and record the expected failure.

A test that unexpectedly passes does not establish RED. Review whether the behavior already exists or the test is ineffective.

## Phase 4 — GREEN: Implement the Minimum Code

After RED is established:

1. Change only the production files listed in the approved Implementation Plan.
2. Implement the smallest behavior required to make the new tests pass.
3. Do not add speculative abstractions, unrelated cleanup, or new requirements.
4. Run the focused tests, then the broader relevant suite.

GREEN means the approved behavior passes and existing behavior has not regressed.

## Phase 5 — REFACTOR: Improve Without Changing Behavior

Refactoring begins only after GREEN.

During refactoring:

- preserve public behavior and contracts
- remove duplication and improve naming or boundaries only where justified
- keep each refactor small and reviewable
- run tests after every meaningful refactor
- do not add new feature behavior

If refactoring exposes a missing behavior, return to the planning and RED phases rather than silently expanding scope.

## Phase 6 — Final Review

Complete all applicable checks:

- Plan and Implementation Plan match the delivered scope
- new tests were observed RED before implementation
- focused and broader tests are GREEN
- refactoring did not change behavior
- repository validators and static checks pass
- documentation and enforcement matrix are updated when standards changed
- remaining risks or deferred work are documented

## Evidence to Preserve

For reviewable work, retain:

- approved Plan
- approved Implementation Plan
- test names and RED command/result
- GREEN command/result
- refactoring summary
- final changed-file list

Do not retain private chain-of-thought. Preserve decisions, evidence, and outcomes only.

## LLM Instructions

- Never collapse Plan and Implementation Plan into one artifact for qualifying work.
- Never generate production implementation during the planning phases.
- Write tests before production code and confirm that they fail for the intended reason.
- Implement only enough code to reach GREEN, then refactor separately.
- If the user changes scope, update the Plan and Implementation Plan before continuing.
- For documentation or tooling changes, use the most relevant executable validator as the RED/GREEN check.

## Review Checklist

- [ ] Requirements and current state were read before planning
- [ ] `docs/.ai/Plan.md` exists and was reviewed
- [ ] A milestone-specific Implementation Plan exists and was reviewed
- [ ] Tests or executable checks were created before production changes
- [ ] RED failure was caused by the missing approved behavior
- [ ] Minimal implementation reached GREEN
- [ ] Refactoring occurred only after GREEN
- [ ] Full relevant test and validation suite passes
- [ ] No unapproved requirements or unrelated changes were added

## References

- [Agent Execution Standard](agent-execution.md)
- [Definition of Done](definition-of-done.md)
- [Unit Testing](testing/unit-testing.md)
- [Integration Testing](testing/integration-testing.md)
