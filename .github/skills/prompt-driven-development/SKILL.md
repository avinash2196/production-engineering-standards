---
name: prompt-driven-development
description: Use when planning or delivering work through explicit human-reviewed Requirements, Plan, optional API/external contract, Implementation Plan, RED, GREEN, optional REFACTOR, and final-review boundaries.
---

# Prompt-Driven Development

Use this skill when the adopting repository explicitly follows the PDD lifecycle.

## Lifecycle

**Requirements → Plan → Human Review → API/External Contract when applicable → Human Review → Implementation Plan → Human Review → RED → GREEN → optional REFACTOR → Final Review**

The API/external contract stage is required when externally observable behavior must be defined before implementation, such as an HTTP API or another stable consumer-facing interface.

## Artifact Authority

Each artifact has a distinct responsibility:

- Requirements define intended behavior, constraints, and explicit exclusions.
- Plan defines approved scope, milestone sequence, and completion criteria.
- API/external contract defines approved externally observable behavior when applicable.
- Implementation Plan defines how one authorized milestone and phase will be executed.
- Tests/checks provide executable evidence of expected behavior.
- Production code implements the approved behavior.

Do not silently reconcile material contradictions between authoritative artifacts.

If approved artifacts materially conflict:

1. identify the conflict,
2. stop the current workflow,
3. surface it for human review,
4. do not modify one artifact merely to make it match another.

## Plan Integrity

After human approval, the Plan is an authorization artifact.

- Do not rewrite the Plan to match implementation.
- Do not change milestone definitions during milestone execution.
- Do not expand scope because implementation reveals a technically useful improvement.
- Update only execution/status information after the milestone success criteria are verified.
- Scope or milestone changes require explicit replanning and human review.
- Material unresolved decisions must be resolved before Plan approval.

## Phase Controls

- Each repository-changing milestone gets its own Implementation Plan defining how that milestone only is executed.
- RED, GREEN, and REFACTOR are separate authorization boundaries.
- RED writes tests/checks only.
- GREEN implements the smallest production change needed for approved RED evidence.
- REFACTOR is optional and behavior-preserving.
- A completed phase never implies approval of the next phase.
- A single end-to-end request does not remove these boundaries.

## Task Prompt Boundary

Persistent instructions, agents, and skills do not replace the active task prompt.

The active task should still identify the current authorization boundary, including as applicable:

- goal,
- authoritative inputs,
- current milestone and phase,
- requested output,
- files or areas allowed to change,
- milestone-specific constraints,
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
