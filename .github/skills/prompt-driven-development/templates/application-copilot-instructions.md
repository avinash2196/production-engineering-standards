# Application Copilot Instructions

## Project Context

Technology:

* <runtime/version>
* <framework/version>
* <build system>
* <test framework>

Application-specific constraints:

* <constraint>
* <constraint>

Do not introduce excluded capabilities unless explicitly approved by requirements.

## Architecture

* Follow the application's approved architecture.
* Prefer the smallest design satisfying approved requirements.
* Do not introduce unnecessary abstractions, infrastructure, or distributed-system patterns.

## PDD Workflow

For behavior-changing work:

```
Requirements
→ Plan
→ Human Review
→ API / External Contract when applicable
→ Human Review
→ FOR EACH IMPLEMENTATION MILESTONE:
    RED Implementation Plan → Human Review → RED
    → GREEN Implementation Plan → Human Review → GREEN
    → optional REFACTOR Implementation Plan → Human Review → REFACTOR
→ Final Review
```

Each Implementation Plan authorizes exactly one phase of exactly one milestone — never RED and GREEN together, and never more than one milestone. RED, GREEN, and REFACTOR are separate authorization boundaries.

Completion of one phase does not authorize the next.

How many milestones this work needs is decided in the Plan, based on complexity, responsibility boundaries, risk, and independent verifiability — a small cohesive change may use one RED/GREEN pair; larger work should use multiple sequential milestone cycles. Do not default to one pair for the whole feature, and do not default to one pair per class or architectural layer.

## No Code Change Without Approval

<!-- PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL:START -->
Every code change must be traceable to a human-approved, phase-specific Implementation Plan — this applies regardless of which command, prompt, or free-form request produced the change. Do not modify production source, tests, configuration, dependencies, schemas, migrations, scripts, or other executable repository artifacts from a free-form request, review finding, failing test, or inferred fix alone.

If no approved Implementation Plan authorizes the requested change, do not implement it; route the work through the appropriate PDD planning and human-review boundary first.

The size and detail of an Implementation Plan should be proportional to the change — small changes may use a very small Implementation Plan, but they do not bypass human approval. This applies to all code changes, not only behavior-changing ones.

Documentation-only changes clearly outside executable/code artifacts may follow the project's normal documentation workflow; do not invent exceptions to the above for source, tests, configuration, dependencies, or other executable artifacts.
<!-- PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL:END -->

## Planning Artifacts

* Plan: `docs/.ai/Plan.md`
* API / External Contract: `<path when applicable>`
* Implementation Plans: `docs/.ai/NNN_Implementation_Plan_<Milestone>.md`

Plan defines WHAT is delivered.

The external contract defines approved externally observable behavior when applicable.

Each Implementation Plan defines HOW one approved milestone is executed.

If approved artifacts materially conflict, stop and surface the conflict for human review.

## External Engineering Standards

Use externally configured agents, skills, and prompts from `production-engineering-standards`.

Do not convert recommendations from skills into project requirements without requirement or repository evidence.

## Clarification Before Assumption

Do not invent or silently resolve material requirements.

If missing, ambiguous, or contradictory information materially affects the current task:

1. Ask focused clarification questions.
2. Stop the workflow.
3. Wait for the user's response before continuing.

Do not use an Open Questions section as a substitute for required clarification.

## Verification

Run the project's approved verification commands.

Do not claim verification succeeded unless the commands completed successfully.
