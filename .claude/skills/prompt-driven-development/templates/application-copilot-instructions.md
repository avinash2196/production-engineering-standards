# Application Copilot Instructions

Use this as the starting content for the adopting application's `.github/copilot-instructions.md`. It is the Copilot equivalent of `application-claude-instructions.md` — same rules, same PDD workflow.

Generate or update the file with the `setup-copilot-instructions` prompt rather than copying it by hand; rerun the prompt when this template changes.

<!-- Every section below is FIXED: copy it verbatim — do not remove, paraphrase, or weaken it. Only the title names the application. Project facts (stack, versions, constraints, commands) do not belong in this file; they live in requirements, the build file, the Plan, and Implementation Plans. -->

## Project Context

<!-- FIXED — preserve verbatim -->
This file holds process rules only. Project facts live in their own sources; read them there and do not restate them here:

* Product requirements, technology stack, and scope exclusions: `docs/requirements.md` (when present) and the work item's `requirements.md`.
* Build, runtime, and dependency versions: the build file (for example `pom.xml`, `build.gradle`, or `pyproject.toml`).
* Verification commands: the approved Plan and the milestone's Implementation Plan.

Do not introduce excluded capabilities unless explicitly approved by requirements.

<!-- FIXED — preserve verbatim -->
## Architecture

* Follow the application's approved architecture.
* Prefer the smallest design satisfying approved requirements.
* Do not introduce unnecessary abstractions, infrastructure, or distributed-system patterns.

<!-- FIXED — preserve verbatim -->
## PDD Workflow

Each milestone's type follows the kind of change, as defined by the `prompt-driven-development` skill's Milestone Types:

```
Requirements
→ Plan
→ Human Review
→ CONTRACT milestone when applicable: API / External Contract → Human Review
→ FOR EACH SEQUENCE OF IMPLEMENTATION MILESTONES, typed by the kind of change:
    behavior change:
        optional FOUNDATION milestone: Implementation Plan → Human Review → execution → Verification
        RED milestone: Implementation Plan → Human Review → execution → Verification
        → GREEN milestone: Implementation Plan → Human Review → execution → Verification
        → optional REFACTOR milestone: Implementation Plan → Human Review → execution → Verification
    behavior-preserving restructuring of existing production code:
        REFACTOR milestone from a verified GREEN baseline: Implementation Plan → Human Review → execution → Verification
    no production behavior change (test-only, build, configuration, infrastructure):
        OTHER milestone: Implementation Plan → Human Review → execution → Verification
→ Final Review
```

A failing test is not automatically RED: if the test itself is wrong and production behavior is correct, the work is OTHER; if a correct existing test exposes missing behavior, that test is the RED evidence and RED changes no file. When the requirements do not settle which side is wrong, ask and stop.

Each Implementation Plan authorizes exactly one repository-changing milestone — never RED and GREEN together, and never more than one milestone. FOUNDATION when required, RED, GREEN, REFACTOR, and OTHER are each separate milestones and separate authorization boundaries.

When an API / External Contract is required, it is a CONTRACT milestone recorded in the Plan: the first milestone after Plan approval, before any FOUNDATION, RED, GREEN, REFACTOR, or OTHER milestone. It changes no executable artifact and has no Implementation Plan; the contract artifact itself is the human-reviewed deliverable. A changed contract starts from the verified current contract and defines only the approved changes.

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

<!-- FIXED — preserve verbatim -->
* Work items: each piece of work (new project or enhancement) has its own folder `docs/.ai/<work-item>/`; PDD commands take the work item as an argument
* Requirements: `docs/.ai/<work-item>/requirements.md` (optional product-level `docs/requirements.md` is read-only context)
* Plan: `docs/.ai/<work-item>/Plan.md`
* API / External Contract: `docs/.ai/<work-item>/<contract file, e.g. API-Contract.md>` (when applicable)
* Implementation Plans: `docs/.ai/<work-item>/NNN_Implementation_Plan_<Milestone>.md`

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

<!-- FIXED — preserve verbatim -->
Run the verification commands recorded in the approved Implementation Plan for the milestone.

Do not claim verification succeeded unless the commands completed successfully.
