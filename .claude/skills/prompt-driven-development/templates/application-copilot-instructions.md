# Application Copilot Instructions

<!-- Before finalizing this file for a specific project: do not remove, paraphrase, or weaken any section marked FIXED below — copy it verbatim. Only replace CUSTOMIZE placeholders with project-specific values. Every reference to the same artifact (e.g. Requirements, Plan, Contract) must use the same path consistently everywhere it appears in the generated file. -->

## Project Context

Technology:

<!-- CUSTOMIZE — project-specific value -->
* <runtime/version>
* <framework/version>
* <build system>
* <test framework>

Application-specific constraints:

<!-- CUSTOMIZE — project-specific value -->
* <constraint>
* <constraint>

<!-- FIXED — preserve verbatim -->
Do not introduce excluded capabilities unless explicitly approved by requirements.

<!-- FIXED — preserve verbatim -->
## Architecture

* Follow the application's approved architecture.
* Prefer the smallest design satisfying approved requirements.
* Do not introduce unnecessary abstractions, infrastructure, or distributed-system patterns.

<!-- FIXED — preserve verbatim -->
## PDD Workflow

For behavior-changing work:

```
Requirements
→ Plan
→ Human Review
→ CONTRACT milestone when applicable: API / External Contract → Human Review
→ FOR EACH SEQUENCE OF IMPLEMENTATION MILESTONES:
    optional FOUNDATION milestone: Implementation Plan → Human Review → execution → Verification
    RED milestone: Implementation Plan → Human Review → execution → Verification
    → GREEN milestone: Implementation Plan → Human Review → execution → Verification
    → optional REFACTOR milestone: Implementation Plan → Human Review → execution → Verification
→ Final Review
```

Each Implementation Plan authorizes exactly one repository-changing milestone — never RED and GREEN together, and never more than one milestone. FOUNDATION when required, RED, GREEN, and REFACTOR are each separate milestones and separate authorization boundaries.

When an API / External Contract is required, it is a CONTRACT milestone recorded in the Plan: the first milestone after Plan approval, before any FOUNDATION, RED, GREEN, or REFACTOR milestone. It changes no executable artifact and has no Implementation Plan; the contract artifact itself is the human-reviewed deliverable.

Completion of one milestone does not authorize the next.

How many milestones this work needs is decided in the Plan, based on complexity, responsibility boundaries, risk, and independent verifiability — a small cohesive change may use one RED milestone / GREEN milestone pair; larger work should use multiple sequential milestone sequences. Do not default to one pair for the whole feature. Do not mechanically create one milestone per class — but for complex requirements spanning independently testable architectural layers, create a separate RED milestone and GREEN milestone for each layer, as defined by the `prompt-driven-development` skill's Adaptive Milestone Decomposition.

## No Code Change Without Approval

<!-- PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL:START -->
Every code change must be traceable to a human-approved, milestone-specific Implementation Plan — this applies regardless of which command, prompt, or free-form request produced the change. Do not modify production source, tests, configuration, dependencies, schemas, migrations, scripts, or other executable repository artifacts from a free-form request, review finding, failing test, or inferred fix alone.

If no approved Implementation Plan authorizes the requested change, do not implement it; route the work through the appropriate PDD planning and human-review boundary first.

The size and detail of an Implementation Plan should be proportional to the change — small changes may use a very small Implementation Plan, but they do not bypass human approval. This applies to all code changes, not only behavior-changing ones.

Documentation-only changes clearly outside executable/code artifacts may follow the project's normal documentation workflow; do not invent exceptions to the above for source, tests, configuration, dependencies, or other executable artifacts.
<!-- PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL:END -->

## Planning Artifacts

<!-- CUSTOMIZE — project-specific value; use the same path everywhere this artifact is referenced in this file -->
* Plan: `docs/.ai/Plan.md`
* API / External Contract: `<path when applicable>`
* Implementation Plans: `docs/.ai/NNN_Implementation_Plan_<Milestone>.md`

<!-- FIXED — preserve verbatim -->
Plan defines WHAT is delivered. After approval it is the single source of truth for the complete development: every contract, Implementation Plan, test, and production change must trace to a milestone recorded in it.

The external contract defines approved externally observable behavior when applicable.

Each Implementation Plan defines HOW one approved milestone will change the repository.

If approved artifacts materially conflict, stop and surface the conflict for human review.

<!-- FIXED — preserve verbatim -->
## External Engineering Standards

Use externally configured agents, skills, and prompts from `production-engineering-standards`.

Do not convert recommendations from skills into project requirements without requirement or repository evidence.

<!-- FIXED — preserve verbatim -->
## Clarification Before Assumption

Do not invent or silently resolve material requirements.

If missing, ambiguous, or contradictory information materially affects the current task:

1. Ask focused clarification questions.
2. Stop the workflow.
3. Wait for the user's response before continuing.

Do not use an Open Questions section as a substitute for required clarification.

## Verification

Run the project's approved verification commands.

<!-- FIXED — preserve verbatim -->
Do not claim verification succeeded unless the commands completed successfully.
