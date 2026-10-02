# Requirements — milestone-types

## Context

Two enhancement work items planned with plugin 0.9.3 exposed gaps in how milestone types are chosen
(evaluation on 2026-10-01):

- A test-only work item (Claude Code) correctly typed all milestones OTHER, but OTHER has no rules,
  no Implementation Plan path, and no executor command.
- An infrastructure swap with an unchanged HTTP API (Copilot) recorded a CONTRACT milestone for a
  contract that does not change, a RED milestone that changes runtime configuration, and invented RED
  evidence.
- Since 0.9.1 the application instruction files point to the Plan for verification commands, but the
  Plan template has no place for them; one Plan cited the instruction file for commands it no longer
  contains.
- Plan Content Rule 3 ("do not name … test classes") conflicted with Rule 9 and the template's
  Current State ("list the existing tests"), producing a Current State that avoided naming tests.
- A Copilot requirements capture did not follow `templates/requirements.md` (no Operational
  Characteristics, no product-level relationship, a "Next step" section).

## Requirements

- **MT-1** — TDD stays the heart of PDD: any requirement that adds or changes behavior is delivered by
  RED then GREEN. [User, 2026-10-01: "we wanted TDD to be heart of this"]
- **MT-2** — Milestone types are chosen by the kind of change, not by whether the project is new or an
  enhancement. A new project normally needs CONTRACT, FOUNDATION, RED and GREEN; an enhancement uses
  what its requirements call for. [User: "for new project we would need everything … for enhancement,
  it should depend on kind of work"]
- **MT-3** — OTHER is defined for approved work that changes no production behavior (for example
  test-only fixes, or replacing build, configuration, or infrastructure under unchanged behavior). It
  keeps every PDD gate: own Implementation Plan, human review, verification, Final Review. [User
  approved the proposal, 2026-10-01]
- **MT-4** — OTHER guardrails: allowed only when no owned requirement adds or changes behavior; if a
  test could fail first because behavior is missing, the work is RED/GREEN; before and after evidence
  is recorded; named existing tests prove behavior is preserved; a needed behavior change stops for
  replanning. [User approved the proposal, 2026-10-01]
- **MT-5** — OTHER milestones can be planned (`create-implementation-plan`) and executed
  (`implement-approved-plan`, implementation-engineer). [Derived from MT-3 — confirmed by approval]
- **MT-6** — A CONTRACT milestone exists only when the work item creates or changes an external
  contract; an unchanged existing contract is a constraint the Plan references. [User approved]
- **MT-7** — The Plan records the verification commands, sourced from requirements or repository
  evidence; for a project with no build yet, the FOUNDATION milestone establishes them. [User approved]
- **MT-8** — Plan Content Rule 3 governs milestone descriptions; Current State and Risks may name
  existing files and tests as repository facts. [User approved]
- **MT-9** — `capture-requirements` writes the artifact using `templates/requirements.md`. [User approved]
- **MT-10** — The new-project flow (CONTRACT → FOUNDATION → RED → GREEN) must not regress. [User:
  "make sure we don't drift from new project behavior which was working well"]

## Repository-Confirmed Facts

- The Plan template already lists OTHER as a milestone type and a test requires it
  (`tooling/tests/test_pdd_controls.py:355-363`).
- A test requires the implementation-engineer description to contain "Execute an approved FOUNDATION
  or GREEN milestone's Implementation Plan" (`tooling/tests/test_pdd_controls.py:462-469`).

## Operational Characteristics

Instruction text only; no running system. All six characteristics: not required for this work item.

## Acceptance Criteria

- AC-1: A headless `create-plan` run on a new project's requirements still produces CONTRACT →
  FOUNDATION → RED → GREEN milestones (MT-10).
- AC-2: A headless `create-plan` run on a test-only enhancement produces OTHER milestones with
  before/after evidence and existing-test preservation, and no RED/GREEN (MT-3, MT-4).
- AC-3: A headless `create-plan` run on an infrastructure swap with unchanged API produces no CONTRACT
  milestone and no RED milestone that changes runtime configuration (MT-6).
- AC-4: Plans record verification commands in a Verification Commands section (MT-7).
- AC-5: Validator and unittest suite pass.
