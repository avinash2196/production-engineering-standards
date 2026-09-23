---
name: prompt-driven-development
description: Use when planning or delivering work through explicit human-reviewed Requirements, Plan, optional API/external contract, milestone-specific Implementation Plans, RED, GREEN, optional REFACTOR, and final-review boundaries.
---

# Prompt-Driven Development

Use this skill when the adopting repository explicitly follows the PDD lifecycle.

## Lifecycle

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

The API/external contract is required when externally observable behavior must be defined before implementation, such as an HTTP API or another stable consumer-facing interface. When required, it is delivered by a CONTRACT milestone recorded in `Plan.md`.

A CONTRACT milestone, when present, is always the first milestone after Plan approval. It precedes every FOUNDATION, RED, GREEN, and REFACTOR milestone, because no repository-changing milestone may start before the externally observable behavior it depends on is approved. Its deliverable is the API/external contract artifact itself; it changes no executable artifact, so it has no Implementation Plan — the contract artifact is the human-reviewed deliverable.

CONTRACT, FOUNDATION, RED, GREEN, and REFACTOR are each their own milestone, not phases nested inside a containing milestone. A single Implementation Plan authorizes exactly one milestone — it never authorizes more than one milestone, and it never authorizes work for a different milestone. Each repository-changing milestone gets its own human-reviewed Implementation Plan. Completing one milestone never authorizes the next milestone. FOUNDATION is conditional — see "Conditional SETUP / FOUNDATION" below — most sequences proceed directly to a RED milestone.

A RED milestone is followed by a GREEN milestone, then an optional REFACTOR milestone, once per independently reviewable capability/layer. See "Adaptive Milestone Decomposition" below for how many such milestone sequences a given piece of work should use.

## Artifact Authority

Each artifact has a distinct responsibility:

- Requirements define intended behavior, constraints, and explicit exclusions.
- Plan defines approved scope, milestone sequence, requirement ownership, completion criteria, and execution status. After approval it is the single source of truth for the complete development: every contract, Implementation Plan, test, and production change must trace to a milestone recorded in it, and nothing outside it is authorized.
- API/external contract defines approved externally observable behavior when applicable.
- Implementation Plan defines the concrete proposed changes for one authorized milestone based on the current repository state.
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
4. establish the actual current-state baseline for the authorized milestone, including prerequisites/dependencies, contracts or interfaces the milestone depends on, relevant test entry points, and any unresolved blockers.

This inspection is preparation for planning, not a separate implementation milestone — it does not introduce a formal step before the RED milestone. If it discovers that repository code must change before the milestone's own work can proceed, that change still requires its own approved Implementation Plan; inspection alone never authorizes a change.

Do not plan from an assumed repository structure or from the original Plan alone when earlier milestones have changed the codebase.

An Implementation Plan is a human-review artifact, not merely a task list.

For the authorized milestone, it must contain:

- authoritative artifact references;
- predecessor evidence;
- current repository state relevant to the milestone;
- exact files to create or modify;
- ordered proposed changes;
- concrete proposed tests or production changes;
- relevant classes, methods, interfaces, signatures, structures, or configuration changes;
- code snippets, pseudocode, or patch-level detail where practical and useful for human review;
- explicit Acceptance / Completion Criteria for the specific milestone — what must be true for it to be considered complete, distinct from the verification that demonstrates it;
- verification commands and expected milestone evidence;
- risks and explicit exclusions.

The proposed code belongs inside the Implementation Plan so a human can review the intended change before repository implementation is modified.

The planner may write proposed code in the Implementation Plan, but must not apply those proposed changes to production source, tests, build configuration, deployment configuration, or runtime configuration.

## Plan Content Rules

The Plan defines WHAT is delivered and in which milestone order. It does not define HOW (Implementation Plans) or externally observable behavior (the API/external contract). When creating or revising a Plan:

1. **Milestone order.** Record every milestone in one strictly linear sequence. Each milestone has exactly one predecessor — Plan approval for the first milestone, otherwise one earlier milestone. Do not record parallel, optional, or "logically but not strictly required" predecessors. When a CONTRACT milestone exists it is the first milestone; any FOUNDATION milestone follows it.
2. **Contract-owned decisions stay in the contract.** Do not fix endpoint paths, operations/methods, status codes, parameter or field names, request/response schemas, validation rules, error behavior, result shapes for empty or missing data, or any decision the requirements defer to the contract — not even as examples, defaults, or "X or per contract" hints. Reference the contract artifact instead. The CONTRACT milestone's decision list contains the decisions the requirements defer to it plus the externally observable behavior needed to define the required operations — nothing else (no documentation formats, tooling, or extra capabilities). A decision the requirements explicitly defer to a CONTRACT milestone is owned by that milestone; it does not block Plan approval and must not be resolved, narrowed, or presumed in the Plan.
3. **No internal design.** Do not name classes, files, methods, interfaces, packages, framework annotations, libraries or dependencies beyond the approved technology stack, test classes, mocking or test-isolation strategies, or internal layering within a milestone. Describe each milestone by the behavior and requirements it covers. Naming a decomposition boundary (for example a layer or capability chosen under Adaptive Milestone Decomposition) is allowed; prescribing its internal structure is not.
4. **RED milestones deliver tests/checks only.** State the behaviors the tests must verify. Never list production types, scaffolding, or configuration as RED deliverables.
5. **GREEN milestones deliver behavior.** State the behavior that makes the predecessor RED evidence pass. Do not list production classes or components.
6. **FOUNDATION is prerequisite-only.** Limit it to the build, dependency, bootstrap, configuration, or test-infrastructure prerequisites the following RED milestone needs to execute, consistent with approved requirements (never an alternative the requirements exclude). The domain model, schema derived from it, and target behavior belong to GREEN.
7. **Complete milestone entries.** Every milestone records every field the Plan template requires, including explicit exclusions and success criteria.
8. **Single ownership.** Every approved requirement and cross-cutting concern has exactly one owning delivery milestone, recorded in the Plan's requirement traceability. The owning milestone delivers it (GREEN for behavior, CONTRACT for contract decisions, FOUNDATION for prerequisites); the verifying milestone is the RED milestone whose tests verify it (or human review for a CONTRACT decision). No requirement has two owners.
9. **No invented scope.** Do not add requirements, non-functional targets, coverage thresholds, exclusions, or constraints that are not in approved requirements or repository evidence. Out of Scope lists only exclusions the requirements state. Current State describes only what inspection of the repository shows. Risks and mitigations must not weaken, reinterpret, or contradict a requirement or reassign a decision to a different milestone.
10. **Honest status.** A newly created or revised Plan records every milestone as Pending and marks nothing approved, verified, or complete.

## Plan Integrity

After human approval, the Plan is an authorization artifact and a living execution-status record.

- Do not rewrite the Plan to match implementation.
- Do not change milestone definitions during milestone execution.
- Do not expand scope because implementation reveals a technically useful improvement.
- Update only execution/status information after the milestone's success criteria are actually verified.
- Record actual verification evidence where appropriate.
- Scope, milestone, architecture, or success-criteria changes require explicit replanning and human review.
- Material unresolved decisions must be resolved before Plan approval.

If execution reveals that the approved Plan itself must change, stop for replanning and human review.

## Milestone Controls

### Adaptive Milestone Decomposition

For larger changes, decompose implementation into independently reviewable sequences of RED milestone → GREEN milestone → optional REFACTOR milestone based on complexity, risk, responsibility boundaries, and independent verifiability.

A small cohesive change may use one RED milestone / GREEN milestone pair.

Do not default to one giant RED/GREEN pair for the whole feature. Do not mechanically create one pair per class or file.

Boundaries may include persistence, business behavior, API behavior, integration, or another independently testable capability. See `docs/getting-started.md` for fuller illustrative examples — this skill states the rule, not an exhaustive catalog of boundaries.

For complex requirements that span multiple independently testable architectural layers, create separate layer-wise implementation milestones — a separate RED milestone and GREEN milestone (and optional REFACTOR milestone) for each layer — rather than one feature-wide RED/GREEN pair. In a typical layered application, this may result in separate milestone sequences for persistence/data access, domain/service behavior, API/controller behavior, and cross-layer integration — for example: Persistence RED → Persistence GREEN → Service RED → Service GREEN → API RED → API GREEN. There is no containing "capability milestone" that owns these as internal phases — each is its own milestone with its own Implementation Plan and Human Review before execution. Before the RED milestone for each layer, determine whether a preceding FOUNDATION milestone is required — see "Conditional SETUP / FOUNDATION" below.

Layer-wise decomposition is not a mandatory architectural template. If the system is better decomposed by capability, workflow, domain aggregate, integration boundary, migration step, concurrency concern, or another independently reviewable responsibility, use that boundary instead.

The governing rule is: decompose complex work into the smallest meaningful independently reviewable implementation milestones. When the complexity crosses architectural layers, prefer separate layer-wise milestones over one feature-wide cycle — but do not force layer boundaries onto an architecture that does not support them.

When work is decomposed across milestones, every requirement or cross-cutting concern within approved scope — for example validation, error mapping, authorization, observability, or persistence behavior — must have an explicit owning milestone recorded in the Plan. Not every concern needs its own milestone; a single milestone may own several, but no approved concern may be left without an assigned owner across the decomposition.

- Each repository-changing milestone gets its own Implementation Plan.
- FOUNDATION (when required), RED, GREEN, and REFACTOR are each separate milestones and separate authorization boundaries.
- RED Implementation Plans propose test/check changes only.
- RED execution writes tests/checks only and establishes valid RED evidence. In statically typed languages, RED may include a compilation failure when that failure is directly caused by an intentionally absent production type, method, or signature required by the approved behavior (for example, a test referencing `UserService` failing to compile because `UserService` does not exist yet). Do not create production-source scaffolding merely to make RED tests compile. Unrelated compilation, configuration, dependency, or environment failures are not valid RED evidence.
- GREEN Implementation Plans start from valid RED evidence and propose the smallest production change needed to satisfy it.
- GREEN execution implements only the approved production change.
- REFACTOR is optional, behavior-preserving, and requires a verified GREEN baseline plus its own approved Implementation Plan.
- A completed milestone never implies approval of the next milestone.
- A single end-to-end request does not remove these boundaries.

When an approved milestone's change is intended to affect multiple files or multiple occurrences of a pattern, verify completeness before reporting that milestone's work as finished — for example, search for remaining occurrences of the prior pattern, rerun the relevant tests or build, or check each affected file; the verification method should match the nature of the change. Do not report a multi-location change complete solely because the edit operations were applied.

### Conditional SETUP / FOUNDATION

SETUP/FOUNDATION exists only when executable prerequisites must be established before meaningful RED work can begin. It is conditional, never a default or mandatory milestone, and most work will not need one.

Before starting a RED milestone, determine whether the current repository state is sufficient to begin RED:

- If yes, proceed directly with the RED milestone, then the GREEN milestone, then an optional REFACTOR milestone.
- If no, because executable prerequisites are genuinely missing, precede it with a FOUNDATION milestone: FOUNDATION milestone → RED milestone → GREEN milestone → optional REFACTOR milestone.

Apply this same current-state-driven decision to both new and existing repositories — do not decide FOUNDATION from whether the project is labeled greenfield or brownfield. Do not assume a new project automatically requires FOUNDATION: if a new project's build/test infrastructure has already been set up, the RED milestone can often proceed directly. Do not assume an existing project automatically has every prerequisite: an established codebase can still be missing something a new RED milestone specifically needs. Determine FOUNDATION solely from whether the current repository state actually provides what the RED milestone needs — inspected each time, not assumed from the project's age.

Examples of valid SETUP/FOUNDATION work: required build/dependency setup; module or project structure required by the layer; test framework/infrastructure needed before tests can run; required configuration; infrastructure/bootstrap required before the layer is testable; a prerequisite contract/interface established by an earlier architectural decision; a migration/framework prerequisite; or another executable prerequisite without which RED cannot meaningfully begin.

**Missing production symbols do not, by themselves, require SETUP.** Do not create a FOUNDATION milestone merely because the production class, service, repository, controller, method, interface, or other implementation under test does not yet exist — that absence is itself the expected RED condition (a compilation failure caused by an intentionally absent approved production type, method, or signature is valid RED evidence, per RED execution above), and creating that type with real behavior is GREEN's job, not SETUP's. Distinguish:

- missing behavior/type that RED is intended to drive — not a SETUP trigger, from
- missing infrastructure/prerequisite that prevents RED from meaningfully testing the behavior at all — a genuine SETUP trigger.

SETUP/FOUNDATION still requires the same authorization as any other code change. Every SETUP change to production source, test infrastructure, configuration, dependencies, build files, schema/migrations, scripts, or runtime/infrastructure artifacts requires its own approved SETUP/FOUNDATION Implementation Plan and human review before execution, exactly like RED, GREEN, and REFACTOR:

```
SETUP/FOUNDATION Implementation Plan
→ Human Review
→ SETUP/FOUNDATION execution
→ verification
→ inspect current repository state
→ RED Implementation Plan
→ Human Review
→ RED
```

Do not accept an instruction to "make whatever setup changes are necessary" as authorization — SETUP/FOUNDATION work requires its own approved Implementation Plan like any other code change.

SETUP/FOUNDATION is not RED (it does not write tests) and is not GREEN (it does not implement approved behavior). Do not use GREEN to hide prerequisite work that should have been approved before RED. Do not treat FOUNDATION as a general-purpose coding milestone — its only purpose is to establish the minimum approved prerequisite necessary to make the following RED milestone executable, nothing more.

## Plan Progress

After an approved milestone is successfully executed and verified:

- update only the execution/status section of `Plan.md`;
- record the completed milestone;
- record actual verification evidence or concise notes where appropriate;
- do not rewrite requirements, milestone scope, architecture, exclusions, success criteria, or future milestones.

If verification fails or does not demonstrate the intended milestone evidence, do not mark the milestone complete.

Completing a milestone does not authorize the next milestone. Each subsequent repository-changing milestone requires its own approved Implementation Plan and Human Review.

## Final Review Authority

Final Review (code review, production-readiness review, or any review command) produces findings and recommendations only. A finding is not an authorized change.

- Do not apply a Final Review finding directly to production code, tests, or configuration.
- A finding that requires a change to source, tests, configuration, dependencies, schemas, migrations, scripts, or other executable artifacts must go through the normal authorization chain: update the relevant authoritative artifact if scope is affected, then a new or amended Implementation Plan, then RED before GREEN if the finding adds or alters behavior or validation. There is no trivial-change exception for executable artifacts.

## Task Prompt Boundary

Persistent instructions, agents, and skills do not replace the active task prompt.

The active task should still identify the current authorization boundary, including as applicable:

- goal;
- authoritative inputs;
- current milestone and its type (FOUNDATION, RED, GREEN, or REFACTOR);
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
