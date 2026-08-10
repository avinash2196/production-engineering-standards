# Agent Execution Standard

## Purpose

This standard controls how AI agents plan, implement, test, and review multi-step engineering work. It keeps scope visible, separates design from code generation, and makes each meaningful phase independently reviewable.

## Required Workflow

For qualifying implementation work, agents follow:

> **Review context → Plan → Human review → Implementation Plan → Human review → RED tests → GREEN code → Refactor → Final review**

The lifecycle line is a summary. In execution, RED, GREEN, and optional REFACTOR work are separate Plan milestones with separate milestone-specific Implementation Plans and review gates.

Full lifecycle: [Prompt-Driven Development Workflow](prompt-driven-development-workflow.md)

## When Plan and Implementation Plan Are Required

Both artifacts are required when any condition applies:

| Condition | Example |
|---|---|
| Production behavior changes | New endpoint, changed validation, bug fix |
| Four or more files are affected | Service scaffolding or cross-layer feature |
| A directory, module, adapter, or shared standard is added | New capability contract |
| An API, event, persistence, or integration contract changes | Schema or endpoint change |
| Reliability, security, compliance, or transaction behavior changes | Retry policy, outbox, access control |
| The user requests end-to-end implementation | “Implement the whole feature” |

A typo or one-line documentation correction may proceed without both artifacts, but it must still be validated.

## Required Artifacts

### Plan

Location:

```text
docs/.ai/Plan.md
```

The Plan defines scope, requirements, phase-specific milestones, predecessor relationships, dependencies, risks, exclusions, and success criteria. It must not contain complete production code.

For behavior-changing work, RED and GREEN are separate milestones. REFACTOR is a separate optional milestone only when justified.

Template: [Plan Template](../templates/docs/plan-template.md)

### Implementation Plan

Location:

```text
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
```

Each repository-changing Plan milestone has its own Implementation Plan. The plan declares its phase and authorizes only that phase:

- RED: tests/checks and valid RED evidence only
- GREEN: minimum production behavior and GREEN verification only
- REFACTOR: behavior-preserving structural changes only
- FOUNDATION/OTHER: only the approved non-behavior outcome

Template: [Implementation Plan Template](../templates/docs/implementation-plan-template.md)

## Approval Gates

1. Do not create a milestone Implementation Plan until the Plan is approved.
2. Do not execute a milestone until that milestone's Implementation Plan is reviewed and approved.
3. Do not write production behavior during a RED milestone.
4. Do not begin a GREEN milestone until valid predecessor RED evidence exists and the GREEN Implementation Plan is separately approved.
5. Do not refactor during GREEN. A REFACTOR milestone must exist, be justified, start from a verified GREEN baseline, and have its own approved Implementation Plan.
6. Do not automatically advance to the next milestone after completing the current one.

**An end-to-end request does not waive these human review gates for behavior-changing work.** It may define the overall requested scope, but the agent must still stop at the documented Plan and per-milestone approval boundaries.

## Execution Rules

- **Read before writing.** Read every existing file you intend to modify, plus enough adjacent source, tests, contracts, configuration, and call-path context to understand the current phase.
- **Scope-lock.** Update the Plan and affected milestone Implementation Plan before expanding scope.
- **One phase per milestone.** Do not combine RED, GREEN, and REFACTOR authorization for behavior-changing work.
- **Tests first.** RED milestones create/update tests or executable checks before corresponding production implementation.
- **Prove RED.** The failure must be caused by missing approved behavior, not invalid setup.
- **Minimal GREEN.** GREEN milestones implement only enough approved production behavior to satisfy the preceding RED behavior.
- **Refactor separately and optionally.** Perform cleanup only through an approved REFACTOR milestone and preserve behavior.
- **One logical concern per step.** Group files only when they form one coherent approved change.
- **No later-milestone preparation.** Do not pull future dependencies, infrastructure, abstractions, tests, or behavior forward merely because later work may need them.
- **Surface blockers.** Record missing information or unsupported assumptions rather than inventing details.
- **Preserve evidence.** Record commands and summarized outcomes, not private reasoning.

## Documentation Changes

Before creating a new document:

1. Search for an existing document covering the same concern.
2. Prefer updating an existing document over creating a duplicate.
3. Use the closest template under `templates/docs/`.
4. Add inbound and outbound links where they improve navigation.
5. Agent-facing standards must contain `## LLM Instructions` and `## Review Checklist` when the repository convention requires them.

Do not force redundant clarification questions when the required type, audience, scope, inputs, and cross-links are already clear from the request and repository context.

## Milestone Completion Record

At the end of the current milestone, update only its Implementation Plan Execution Evidence section with applicable evidence:

- files created/modified
- RED command and summarized expected failure for RED
- GREEN commands/results for GREEN
- before/after GREEN verification for REFACTOR
- validation result for FOUNDATION/OTHER
- deferred/out-of-scope work

Do not rewrite the approved scope after execution merely to make the implementation appear compliant.

## LLM Instructions

- Create and follow the approved Plan and a separate Implementation Plan for each repository-changing milestone.
- Never write implementation code in planning artifacts.
- Never write production behavior during RED.
- Never advance from RED to GREEN without a separately approved GREEN Implementation Plan.
- Never combine refactor work with GREEN; use a separate approved REFACTOR milestone when justified.
- Do not silently broaden scope or invent missing requirements.
- Use repository validators for documentation, prompt, and tooling changes when applicable.

## Review Checklist

- [ ] Current state and relevant files were reviewed
- [ ] Plan exists and matches requested scope
- [ ] RED/GREEN milestones are separate for behavior-changing work
- [ ] REFACTOR is separate and justified when present
- [ ] Current milestone has its own approved phase-specific Implementation Plan
- [ ] Approval gates were respected
- [ ] RED was verified for the intended reason before the corresponding GREEN milestone
- [ ] Minimal GREEN implementation stayed within approved scope
- [ ] REFACTOR, when used, preserved GREEN behavior
- [ ] Later-milestone work was not pulled forward
- [ ] Final validation and changed-file summary were recorded honestly

## References

- [Prompt-Driven Development Workflow](prompt-driven-development-workflow.md)
- [Definition of Done](definition-of-done.md)
- [Plan Template](../templates/docs/plan-template.md)
- [Implementation Plan Template](../templates/docs/implementation-plan-template.md)
