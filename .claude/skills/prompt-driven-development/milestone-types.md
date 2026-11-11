# Prompt-Driven Development — Milestone Types and Milestone Controls

Part of the `prompt-driven-development` skill (see its Parts table). Apply it together with the core `SKILL.md`.

### Failing Tests: RED or OTHER

When a work item starts from a test that fails, its classification depends on which side is wrong, and that is a requirements question decided in the Plan with evidence — never by an executing agent:

- **The test is wrong** (wrong fixture, wrong assertion, flaky) and production behavior already matches the approved requirements → OTHER. No RED, because no behavior changes.
- **The test is right and production is wrong** — the test correctly expresses approved behavior that production lacks → a RED milestone whose evidence is that existing failing test, then GREEN. The RED milestone changes no test file; it validates and records the existing failure as RED evidence (see "Existing failing tests as RED evidence" under Milestone Controls).
- **Production is wrong and no test exposes it** → RED writes or changes the test, then GREEN.

If the requirements and repository evidence do not establish which side is wrong, ask the user and stop; do not pick one.

### Standalone REFACTOR

REFACTOR also covers a work item whose whole purpose is behavior-preserving restructuring of existing production code (for example splitting a large class), with no RED or GREEN in the work item. Its verified GREEN baseline is the existing system: the full verification suite passing on the unmodified repository, recorded before any change. The Plan names the existing tests that cover the code being restructured. If those tests do not cover the behavior the restructuring could break, precede the REFACTOR with an OTHER milestone that adds characterization tests for the current behavior — never restructure code its tests do not protect.

### OTHER

OTHER keeps every PDD gate — its own Implementation Plan, human review, verification, and Final Review — and the no-code-change-without-approval rule applies to it in full. It exists so that work with no behavior to drive is not forced into an artificial RED.

- **Only without behavior change.** Use OTHER only when no requirement the milestone owns adds or changes production behavior. If a test could be written that fails first because behavior is missing, the work is RED then GREEN, not OTHER. The Plan states, per OTHER milestone, why none of its owned requirements changes behavior.
- **Before and after evidence.** The Plan names the baseline evidence that shows the problem or the starting state (for example a failure rate, a log check, a timing, or the configuration in use) and the evidence that shows completion. The Implementation Plan records the baseline before any change.
- **Existing tests are the safety net.** The Plan names the existing tests that prove behavior is preserved; they must pass after the milestone. Test changes in an OTHER milestone must not weaken or remove an assertion without a same-coverage replacement.
- **Stop on a behavior change.** If an OTHER milestone turns out to need a production behavior change, stop and replan it as RED and GREEN.
- **Validation protocol.** When the requirements call for a check against a running system or with inputs the user supplies, an OTHER milestone may be a validation protocol: the exact commands or steps, each input with who supplies it and where it is placed (never committed unless the requirements say so), the expected observation and the met or not-met rule for each case, and no repository change other than the evidence it records.

### Only RED Ends Failing

Only a RED milestone may end with a failing check, and only with valid RED evidence. FOUNDATION, GREEN, REFACTOR, and OTHER milestones end with every verification command passing; success criteria that let them end failing ("fail", "may fail") are an error. If a milestone cannot pass on its own, the decomposition is wrong — re-split it, or ask and stop.

### Fix Work Items

A defect found after a work item's Plan is approved or its Final Review is done, or a Final Review finding the user accepted, is fixed as its own work item with the fewest milestones: `Decomposition: one pair, one plan` when the fix changes behavior (RED still proves the defect first), or `Decomposition: one milestone` when it is OTHER. Its requirements are short: the defect, the expected behavior, and how to reproduce it. Its Implementation Plan is the Review Summary, the exact diff, and the verification command. It still needs the user's approval at every gate; nothing is approved automatically because it is small.

## Milestone Controls

### Adaptive Milestone Decomposition

Use as few milestones as keep each Implementation Plan reviewable as exact code. One cohesive behavior change uses one RED milestone and one GREEN milestone, plus CONTRACT and FOUNDATION when Milestone Types call for them. This applies to new and existing projects alike; a new project usually has more milestones because it has more of the reasons below, not because it is new.

Every review gate stays whatever the count: requirements, Plan, contract when required, an Implementation Plan for each milestone, execution, and Final Review. Fewer milestones never merges RED and GREEN and never leaves a requirement without an owning milestone and a RED test that verifies it (Plan Content Rule 8).

Split into more milestones only for a stated reason, and record the decision in the Plan as `Decomposition: one pair`, `Decomposition: one pair, one plan` (below), `Decomposition: one milestone` (work that is a single OTHER or standalone REFACTOR milestone), or `Split: <reason>` for each split, so the user approves it at Plan review. Valid reasons:

- **separate engineering decision:** a part carries a material design decision the user should review and approve on its own, such as a schema or query design, a business rule, or an API mapping. A layer counts when it carries such a decision;
- **size:** one Implementation Plan would be too large to review well as exact code;
- **independent capabilities:** separate behaviors that can each be verified on their own;
- **different risk:** a part, such as a data migration or a security change, needs its own gate;
- **ordering:** one part must be verified before the next can be planned;
- **different verification setup:** a part needs its own test infrastructure.

**One pair, one plan (small changes).** When the pair changes no API/external contract and touches at most about 3 production or build files (test files do not count), the Plan may record `Decomposition: one pair, one plan`. The RED and GREEN milestones stay separate in `Plan.md`, each with its own Execution Status, but one Implementation Plan holds both, with a RED part and a GREEN part. The user approves it once. Execution runs in two verified steps: `generate-tests` applies the RED part and records valid RED; then `implement-approved-plan` applies the GREEN part. RED evidence is still required before any production change.

Never split mechanically: not one pair per class or file, and not one pair per layer by habit. A layer with no material decision of its own, such as a pass-through controller or a one-line mapping, stays in the milestone that needs it.

Boundaries may be persistence, business behavior, API behavior, integration, or another independently testable capability; `docs/getting-started.md` has fuller examples. When a stated reason to split applies to complex requirements that span multiple independently testable architectural layers, use layer-wise implementation milestones — a RED milestone and GREEN milestone (and optional REFACTOR milestone) for each layer — rather than one feature-wide pair, for example Persistence RED → Persistence GREEN → Service RED → Service GREEN → API RED → API GREEN. There is no containing "capability milestone" that owns these as internal phases: each has its own Implementation Plan and Human Review, and before each layer's RED milestone, decide whether a FOUNDATION milestone is needed (Conditional SETUP / FOUNDATION). Layer-wise decomposition is not a mandatory architectural template: when capability, workflow, domain aggregate, integration boundary, migration step, or concurrency concern is the better boundary, use it.

The governing rule: use the fewest independently reviewable implementation milestones that keep each Implementation Plan reviewable, and give every in-scope requirement or cross-cutting concern (for example validation, error mapping, authorization, observability, or persistence behavior) one owning milestone in the Plan. One milestone may own several.

- FOUNDATION (when required), RED, GREEN, REFACTOR, and OTHER are each separate milestones and separate authorization boundaries, each with its own Implementation Plan. Neither a completed milestone nor a single end-to-end request authorizes the next.
- RED Implementation Plans propose test/check changes only. RED execution writes tests/checks only and establishes valid RED evidence. In statically typed languages, a compilation failure caused directly by an intentionally absent production type, method, or signature the approved behavior requires (for example a test referencing `UserService` before `UserService` exists) is valid RED evidence. Do not create production-source scaffolding merely to make RED tests compile. Unrelated compilation, configuration, dependency, or environment failures are not valid RED evidence.
- **Existing failing tests as RED evidence.** When `Plan.md` names an existing failing test as a RED milestone's evidence, RED execution changes no file: it runs that test, confirms it fails for the missing approved behavior and not for an unrelated reason, confirms each of its assertions expresses the approved requirement, and records that as RED evidence. If the test turns out to be wrong, stop and return to planning — the work is OTHER, not RED. That named test is this milestone's evidence, not a pre-existing failure outside its scope.
- GREEN Implementation Plans start from valid RED evidence and propose the smallest production change that satisfies it; GREEN execution implements only that change.
- REFACTOR is optional and behavior-preserving, and needs a verified GREEN baseline plus its own approved Implementation Plan: a preceding GREEN milestone's evidence, or for a standalone REFACTOR the full suite passing on the unmodified repository.
- OTHER makes only approved changes with no production behavior change, records baseline evidence first, and is complete only when its after evidence and preserved tests pass (Milestone Types).

When a milestone changes several files or every occurrence of a pattern, verify completeness before reporting it finished — search for remaining occurrences, rerun the relevant tests or build, or check each affected file. Applied edits alone are not evidence.

### Conditional SETUP / FOUNDATION

SETUP/FOUNDATION exists only when executable prerequisites must be established before meaningful RED work can begin. It is conditional, never a default or mandatory milestone, and most work will not need one.

Before starting a RED milestone, determine whether the current repository state is sufficient to begin RED. If it is, proceed with the RED milestone, then the GREEN milestone, then an optional REFACTOR milestone. If executable prerequisites are genuinely missing, precede RED with a FOUNDATION milestone.

Apply this same current-state-driven decision to both new and existing repositories, inspected each time rather than assumed from the project's age. Do not assume a new project automatically requires FOUNDATION: its build and test infrastructure may already exist. Do not assume an existing project automatically has every prerequisite: it can still lack something a new RED milestone needs. At Plan time, apply the same test to the repository state projected after each RED milestone's predecessors complete (Plan Content Rule 11).

Valid FOUNDATION work: build or dependency setup; module or project structure the layer needs; test framework or infrastructure; required configuration; bootstrap needed before the layer is testable; a prerequisite contract or interface from an earlier architectural decision; a migration or framework prerequisite; or another executable prerequisite without which RED cannot meaningfully begin.

**Missing production symbols do not, by themselves, require SETUP.** A production class, service, repository, controller, method, or interface under test that does not exist yet is the expected RED condition, and creating it with real behavior is GREEN's job. Only missing infrastructure that prevents RED from testing the behavior at all is a SETUP trigger.

SETUP/FOUNDATION needs the same authorization as any other code change: every change it makes to source, test infrastructure, configuration, dependencies, build files, schema or migrations, scripts, or runtime artifacts requires its own approved SETUP/FOUNDATION Implementation Plan and human review before execution, then verification and a fresh inspection of the repository before the RED Implementation Plan. An instruction to "make whatever setup changes are necessary" is not authorization. FOUNDATION writes no tests and implements no approved behavior: do not hide prerequisite work in GREEN, and do not use FOUNDATION as a general-purpose coding milestone. It establishes only the minimum prerequisite the RED milestones it serves need.
