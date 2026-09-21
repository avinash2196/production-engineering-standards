---
name: prompt-driven-development
description: Use when planning or delivering work through explicit human-reviewed Requirements, Plan, optional API/external contract, phase-specific Implementation Plans, RED, GREEN, optional REFACTOR, and final-review boundaries.
---

# Prompt-Driven Development

Use this skill when the adopting repository explicitly follows the PDD lifecycle.

## Lifecycle

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

The API/external contract stage is required when externally observable behavior must be defined before implementation, such as an HTTP API or another stable consumer-facing interface.

A single Implementation Plan authorizes exactly one phase (RED, GREEN, or REFACTOR) of exactly one milestone — it never authorizes more than one phase, and it never authorizes work for a different milestone. Each repository-changing phase gets its own human-reviewed Implementation Plan. Completing one phase never authorizes the next phase.

This RED → GREEN → optional REFACTOR sequence repeats once per implementation milestone. See "Adaptive Milestone Decomposition" under Phase Controls for how many milestones a given piece of work should use.

## Artifact Authority

Each artifact has a distinct responsibility:

- Requirements define intended behavior, constraints, and explicit exclusions.
- Plan defines approved scope, milestone sequence, completion criteria, and execution status.
- API/external contract defines approved externally observable behavior when applicable.
- Implementation Plan defines the concrete proposed changes for one authorized milestone and phase based on the current repository state.
- Tests/checks provide executable evidence of expected behavior.
- Production code implements the approved behavior.
- Final Review evaluates completed work against approved artifacts and produces findings and recommendations, not authorized changes.

Do not silently reconcile material contradictions between authoritative artifacts.

If approved artifacts materially conflict:

1. identify the conflict,
2. stop the current workflow,
3. surface it for human review,
4. do not modify one artifact merely to make it match another.

## Implementation Plan

Before creating an Implementation Plan:

1. read the approved Requirements, Plan, and applicable API/external contract;
2. inspect the current repository structure and relevant implementation;
3. read current Plan execution status and completed predecessor evidence;
4. establish the actual current-state baseline for the authorized milestone and phase.

Do not plan from an assumed repository structure or from the original Plan alone when earlier milestones have changed the codebase.

An Implementation Plan is a human-review artifact, not merely a task list.

For the authorized milestone and phase, it must contain:

- authoritative artifact references;
- predecessor evidence;
- current repository state relevant to the milestone;
- exact files to create or modify;
- ordered proposed changes;
- concrete proposed tests or production changes;
- relevant classes, methods, interfaces, signatures, structures, or configuration changes;
- code snippets, pseudocode, or patch-level detail where practical and useful for human review;
- verification commands and expected phase evidence;
- risks and explicit exclusions.

The proposed code belongs inside the Implementation Plan so a human can review the intended change before repository implementation is modified.

The planner may write proposed code in the Implementation Plan, but must not apply those proposed changes to production source, tests, build configuration, deployment configuration, or runtime configuration.

## Plan Integrity

After human approval, the Plan is an authorization artifact and a living execution-status record.

- Do not rewrite the Plan to match implementation.
- Do not change milestone definitions during milestone execution.
- Do not expand scope because implementation reveals a technically useful improvement.
- Update only execution/status information after the milestone or phase success criteria are actually verified.
- Record actual verification evidence where appropriate.
- Scope, milestone, architecture, or success-criteria changes require explicit replanning and human review.
- Material unresolved decisions must be resolved before Plan approval.

If execution reveals that the approved Plan itself must change, stop for replanning and human review.

## Phase Controls

### Adaptive Milestone Decomposition

For larger changes, decompose implementation into independently reviewable RED → GREEN → optional REFACTOR cycles based on complexity, risk, responsibility boundaries, and independent verifiability.

A small cohesive change may use one RED/GREEN pair.

Do not default either to one giant RED/GREEN pair for the whole feature or mechanically create one pair per class/layer.

Boundaries may include persistence, business behavior, API behavior, integration, or another independently testable capability. See `docs/getting-started.md` for fuller illustrative examples — this skill states the rule, not an exhaustive catalog of boundaries.

- Each repository-changing milestone and phase gets its own Implementation Plan.
- RED, GREEN, and REFACTOR are separate authorization boundaries.
- RED Implementation Plans propose test/check changes only.
- RED execution writes tests/checks only and establishes valid RED evidence. In statically typed languages, RED may include a compilation failure when that failure is directly caused by an intentionally absent production type, method, or signature required by the approved behavior (for example, a test referencing `UserService` failing to compile because `UserService` does not exist yet). Do not create production-source scaffolding merely to make RED tests compile. Unrelated compilation, configuration, dependency, or environment failures are not valid RED evidence.
- GREEN Implementation Plans start from valid RED evidence and propose the smallest production change needed to satisfy it.
- GREEN execution implements only the approved production change.
- REFACTOR is optional, behavior-preserving, and requires a verified GREEN baseline plus its own approved Implementation Plan.
- A completed phase never implies approval of the next phase.
- A single end-to-end request does not remove these boundaries.

## Plan Progress

After an approved phase is successfully executed and verified:

- update only the execution/status section of `Plan.md`;
- record the completed milestone/phase;
- record actual verification evidence or concise notes where appropriate;
- do not rewrite requirements, milestone scope, architecture, exclusions, success criteria, or future milestones.

If verification fails or does not demonstrate the intended phase evidence, do not mark the phase complete.

## Final Review Authority

Final Review (code review, production-readiness review, or any review command) produces findings and recommendations only. A finding is not an authorized change.

- Do not apply a Final Review finding directly to production code, tests, or configuration.
- A finding that requires a change must go through the normal authorization chain: update the relevant authoritative artifact if scope is affected, then a new or amended Implementation Plan, then RED before GREEN if the finding adds or alters behavior or validation.
- The only exception is a trivial, zero-behavior-change correction (e.g. a typo, a formatting fix) — anything that changes what the system does or validates is not trivial.

## Task Prompt Boundary

Persistent instructions, agents, and skills do not replace the active task prompt.

The active task should still identify the current authorization boundary, including as applicable:

- goal;
- authoritative inputs;
- current milestone and phase;
- requested output;
- files or areas allowed to change;
- milestone-specific constraints;
- success criteria.

Role belongs to the selected agent. Reusable engineering knowledge belongs to skills. Stable governance belongs to instructions.

## Scope Control

Do not:

- invent requirements or non-functional requirements;
- pull future milestone work into the current task;
- introduce unrelated dependencies, infrastructure, observability, resilience, or architecture changes;
- treat engineering best practices as authorization to expand scope.

When a material unresolved decision blocks the current artifact or change, apply the requirements-analysis clarification gate: ask, stop, and wait.

Use the templates in `templates/` when the adopting project does not already define compatible artifacts.
