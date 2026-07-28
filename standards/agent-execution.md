# Agent Execution Standard

## Purpose

This standard controls how AI agents plan, implement, test, and review multi-step engineering work. It exists to keep scope visible, separate design from code generation, and make every meaningful change reviewable.

## Required Workflow

For qualifying implementation work, agents must follow:

> **Review context → Plan → Human review → Implementation Plan → Human review → RED tests → GREEN code → Refactor → Final review**

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

The Plan defines scope, requirements, milestones, dependencies, risks, exclusions, and success criteria. It must not contain complete production code.

Template: [Plan Template](../templates/docs/plan-template.md)

### Implementation Plan

Location:

```text
docs/.ai/NNN_Implementation_Plan_<Milestone>.md
```

The Implementation Plan defines exact files, tests, expected RED behavior, production changes, refactoring boundaries, commands, exclusions, and success criteria.

Template: [Implementation Plan Template](../templates/docs/implementation-plan-template.md)

## Approval Gates

1. Do not create an Implementation Plan until the Plan is approved.
2. Do not edit production code until the milestone Implementation Plan is approved.
3. Do not write production code before the new or updated tests demonstrate RED.
4. Do not refactor until the minimal implementation is GREEN.

When a user explicitly requests an end-to-end repository update and provides all required decisions, the request may serve as approval to proceed through the documented phases. The agent must still create and follow both artifacts.

## Execution Rules

- **Read before writing.** Read every existing file before modifying it.
- **Scope-lock.** Update both planning artifacts before expanding scope.
- **Tests first.** Test files or executable checks are changed before production implementation.
- **Prove RED.** The failure must be caused by missing behavior, not invalid setup.
- **Minimal GREEN.** Avoid speculative abstractions or unrelated improvements.
- **Refactor separately.** Preserve behavior and rerun tests after each meaningful cleanup.
- **One logical concern per step.** Group files only when they form one coherent change.
- **Surface blockers.** Record missing information or unsupported assumptions rather than inventing details.
- **Preserve evidence.** Record commands and summarized outcomes, not private reasoning.

## Documentation Changes

Before creating a new document:

1. Search for an existing document covering the same concern.
2. Prefer updating an existing document over creating a duplicate.
3. Use the closest template under `templates/docs/`.
4. Add inbound and outbound links where they improve navigation.
5. Agent-facing standards must contain `## LLM Instructions` and `## Review Checklist`.

Do not force redundant clarification questions when type, audience, scope, inputs, and cross-links are already clear from the request and repository context.

## Completion Record

At the end of qualifying work, update the Implementation Plan with:

- files created and modified
- RED command and summarized failure
- GREEN commands and summarized results
- refactoring performed
- deferred or out-of-scope work

## LLM Instructions

- Create and follow both Plan and Implementation Plan for qualifying work.
- Never write implementation code in either planning artifact.
- Modify tests before production code and verify RED before GREEN.
- Refactor only after tests pass and keep behavior unchanged.
- Do not silently broaden scope or invent missing requirements.
- Use repository validators for documentation, prompt, and tooling changes.

## Review Checklist

- [ ] Current state and relevant files were reviewed
- [ ] Plan exists and matches requested scope
- [ ] Implementation Plan exists and names exact tests and files
- [ ] Approval gates were respected
- [ ] RED was verified for the intended reason
- [ ] Minimal implementation reached GREEN
- [ ] Refactoring preserved GREEN
- [ ] Final validation and changed-file summary were recorded
- [ ] New agent-facing documents contain required instruction sections

## References

- [Prompt-Driven Development Workflow](prompt-driven-development-workflow.md)
- [Definition of Done](definition-of-done.md)
- [Plan Template](../templates/docs/plan-template.md)
- [Implementation Plan Template](../templates/docs/implementation-plan-template.md)
