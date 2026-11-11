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
→ FOR EACH SEQUENCE OF IMPLEMENTATION MILESTONES, typed by the kind of change (Milestone Types):
    behavior change:
        optional FOUNDATION milestone: Implementation Plan → Human Review → execution → Verification
        RED milestone: Implementation Plan → Human Review → execution → Verification
        → GREEN milestone: Implementation Plan → Human Review → execution → Verification
        → optional REFACTOR milestone: Implementation Plan → Human Review → execution → Verification
    behavior-preserving restructuring of existing production code:
        REFACTOR milestone from a verified GREEN baseline: Implementation Plan → Human Review → execution → Verification
    no production behavior change (test-only, build, configuration, infrastructure):
        OTHER milestone: Implementation Plan → Human Review → execution → Verification
    after each GREEN, and after each single FOUNDATION, OTHER, or REFACTOR milestone:
        prepare-pr: review → Human go → commit and draft pull request
→ Final Review
```

The API/external contract is required when the work item creates or changes externally observable behavior that must be defined before implementation, such as an HTTP API or another stable consumer-facing interface. When required, it is delivered by a CONTRACT milestone recorded in `Plan.md`. When the work item leaves an existing contract unchanged, that contract is a constraint the Plan references — not a CONTRACT milestone; do not record a milestone to restate, archive, or re-publish an unchanged contract. When the work item changes an existing contract, the CONTRACT milestone starts from that contract as its baseline (see "Changed Contracts" below).

A CONTRACT milestone, when present, is always the first milestone after Plan approval. It precedes every FOUNDATION, RED, GREEN, REFACTOR, and OTHER milestone, because no repository-changing milestone may start before the externally observable behavior it depends on is approved. Its deliverable is the API/external contract artifact itself; it changes no executable artifact, so it has no Implementation Plan — the contract artifact is the human-reviewed deliverable.

CONTRACT, FOUNDATION, RED, GREEN, REFACTOR, and OTHER are each their own milestone, not phases nested inside a containing milestone. A single Implementation Plan authorizes exactly one milestone and no work for any other. The one exception is a paired plan (`Decomposition: one pair, one plan`, Adaptive Milestone Decomposition): one Implementation Plan for exactly one RED milestone and the GREEN milestone it pairs with. Completing one milestone never authorizes the next. FOUNDATION is conditional (Conditional SETUP / FOUNDATION); most sequences proceed directly to a RED milestone.

## Milestone Types

Test-driven development is the heart of PDD: every requirement that adds or changes behavior is delivered by a RED milestone followed by a GREEN milestone. Choose each milestone's type by the kind of change it makes — not by whether the project is new or an enhancement:

| Kind of change | Milestone type |
| --- | --- |
| Creates or changes an external contract | CONTRACT (first, no Implementation Plan) |
| Adds or changes behavior | RED, then GREEN |
| Executable prerequisite a RED milestone needs | FOUNDATION, before that RED |
| Behavior-preserving structural cleanup of production code, from a verified GREEN baseline — either a preceding GREEN milestone or the existing system | REFACTOR (optional after GREEN; standalone for a restructuring request) |
| Approved change with no production behavior change that is not production-code restructuring — for example test-only fixes, characterization tests, or replacing build, configuration, or infrastructure under unchanged behavior | OTHER |

A new project normally needs CONTRACT (when it exposes a contract), FOUNDATION (when its build or test infrastructure does not exist — not when the project already has working build and test infrastructure), and RED/GREEN for every behavior. An enhancement uses only the types its requirements call for, and one work item may mix them — for example OTHER for an infrastructure swap plus RED/GREEN for a new failure behavior it introduces.

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

## Work-Item Folders

Every piece of work — the initial build of a new project and every later enhancement or fix — is a work item with its own folder, so new and existing projects use the same structure:

```
docs/.ai/<work-item>/
  requirements.md
  Plan.md
  <API/external contract>          (when a CONTRACT milestone exists)
  NNN_Implementation_Plan_<Milestone>.md   (a paired plan: NNN_Implementation_Plan_<RED>_<GREEN>.md)
  Final-Review.md
```

- `<work-item>` is a short kebab-case name chosen by the user (for example `initial-build` or `order-cancellation`), with no numeric prefix.
- Every PDD command operates on exactly one work item, named explicitly by the user. If no work item is named, or the named folder does not exist when the command needs an existing artifact, ask and stop — do not infer it from branch names, recent files, or other folders.
- In this skill and in every agent and command, Requirements, `Plan.md`, the API/external contract, Implementation Plans, and `Final-Review.md` mean the files in the current work item's folder.
- Implementation Plan numbering (`NNN`) is per work item and starts at `001`.
- Another work item's artifacts never authorize work in the current one. Completed work items are history, not authority — and not templates: build each artifact from the templates in `templates/`, the user's input, and the current repository, not by copying another work item's structure, wording, or citations. The one exception is a changed external contract, which starts from the verified current contract as its baseline (see "Changed Contracts" below).
- An optional product-level `docs/requirements.md` describes the product as a whole. PDD commands may read it as context but never edit it. The work item's `requirements.md` is authoritative for the work item and states which product-level behavior it changes; any other material conflict between the two stops the workflow for human review. Only the user updates `docs/requirements.md`; Final Review lists the product-level statements a work item has made out of date.

### Changed Contracts

When a work item changes an existing external contract (for example adding an operation, field, or status code to an existing API), its CONTRACT milestone does not rebuild the contract from scratch:

1. **Find the baseline.** Identify the current effective contract — the latest approved contract artifact, or the repository's published contract (for example an OpenAPI document) when that is authoritative.
2. **Verify it.** Check the baseline against the current repository and published contract. If they diverge, stop and surface the divergence for human review; do not silently choose one.
3. **Apply only the delta.** The work item's contract is the complete resulting contract: baseline content carried over unchanged, plus the changes the current requirements and Plan approve. Record the baseline's source and list every change in a Changes in This Work Item section.
4. **Review the delta.** Carried-over content is the existing behavior, not a new decision — it is not reopened, and it authorizes no new work. Every change must trace to the current requirements or Plan; only the changes are CONTRACT decisions under review.

## Artifact Authority

Each artifact has a distinct responsibility:

- Requirements define intended behavior, constraints, and explicit exclusions.
- Plan defines approved scope, milestone sequence, requirement ownership, completion criteria, and execution status. After approval it is the single source of truth for the complete development: every contract, Implementation Plan, test, and production change must trace to a milestone recorded in it, and nothing outside it is authorized.
- API/external contract defines approved externally observable behavior when applicable.
- Implementation Plan defines the concrete proposed changes for one authorized milestone based on the current repository state.
- Tests/checks provide executable evidence of expected behavior.
- Production code implements the approved behavior.
- Final Review evaluates completed work against approved artifacts and produces findings and recommendations, not authorized changes.

Self-checks show their evidence. A self-check that an artifact-creating command reports (provenance, traceability, rule compliance, exact code) passes only by naming what it checked — each derived item with the question that confirmed it, each requirement with the scope bullet that delivers it, each prohibited item searched for. A summary, a count, or a check restated from an earlier pass is not a pass. After any edit, re-derive the check.

Labels and identifiers an artifact introduces (requirement, constraint, decision, clarification, criterion, or contingency IDs) must not reuse a label already defined by an approved artifact it references; use a distinct prefix so every reference is unambiguous.

Do not silently reconcile material contradictions between authoritative artifacts. If approved artifacts materially conflict, identify the conflict, stop, and surface it for human review; never modify one artifact merely to make it match another.

## Implementation Plan

Before creating an Implementation Plan, read the approved Requirements, Plan, and applicable API/external contract, the Plan's execution status and predecessor evidence, and the current repository. Establish the milestone's actual baseline: prerequisites, the contracts or interfaces it depends on, relevant test entry points, and unresolved blockers. Do not plan from an assumed repository structure, or from the original Plan alone when earlier milestones have changed the codebase. This inspection is preparation, not a milestone; if it shows that code must change before the milestone's own work, that change needs its own approved Implementation Plan.

An Implementation Plan is a human-review artifact, not a task list. For the authorized milestone it contains:

- authoritative artifact references and predecessor evidence;
- the current repository state relevant to the milestone;
- the exact files to create, modify, or delete, and the ordered proposed changes, with the classes, methods, interfaces, signatures, structures, or configuration they touch;
- exact code: the complete final content of every file to be created, and for every file to be modified either its complete final content or a complete unified diff covering every changed line with enough context to apply mechanically — never pseudocode, placeholders, ellipses, or partial fragments;
- explicit Acceptance / Completion Criteria for the specific milestone, distinct from the verification that demonstrates them;
- verification commands and expected milestone evidence;
- risks and explicit exclusions.

The planner writes the proposed code in the Implementation Plan for review, and never applies it to production source, tests, or build, deployment, or runtime configuration.

### Approval Status

Only the user approves an Implementation Plan; the AI never approves its own artifact. An Implementation Plan records its status in exactly one place — its Human Review section — and does not repeat it elsewhere in the artifact.

Approval is read only from the artifact. Before any execution command changes a file, it confirms that the plan's Human Review status records approval; it never takes approval from the conversation, and this holds whether or not the command runs in a fresh context (Fresh Context). When the user approves in conversation, the main conversation writes the approval into the artifact's status (`Approved by <user> on <date>`) at the user's word, before the next command runs. No particular phrase is required: "go ahead" or "proceed" in reply to a request to approve that specific artifact is approval. An approval covers one specific artifact that already exists. "Approve everything", "approve on my behalf", or approval of an artifact not yet written is not approval: record nothing, tell the user it was not recorded, and stop at each gate as usual. No command, subagent, or external loop records an approval on its own. An Implementation Plan whose execution stopped at a blocker is not approved until the user re-approves it. Never infer approval from a commit message, from the artifact's existence, or from the plan appearing complete. If no approval is recorded, ask and stop.

After verified execution, update that same Human Review status to executed, point to the evidence recorded in `Plan.md`, and leave no stale status text. A paired plan after RED only records `RED executed — see Plan.md; GREEN approved, not yet executed`; the GREEN step needs no new approval, and the plan becomes `Executed` after GREEN.

The same rule applies to every artifact a command builds on: the requirements before a Plan, the Plan before a contract or Implementation Plan, the contract before the milestones that depend on it. Each records its approval in its own Status section, written there by the main conversation at the user's word; a contract's approval also marks its CONTRACT milestone complete in `Plan.md` Execution Status, pointing to the contract. Before working, a command reads its predecessor's recorded status and cites the artifact, never the conversation. A revised artifact returns to awaiting review. If no approval is recorded, ask and stop.

### Fresh Context

The artifacts carry all state between steps, so every command that works from artifacts runs in a fresh context with its role agent and no conversation history: `create-plan`, `create-api-contract`, and `create-implementation-plan` (planner); `generate-tests` (test-engineer); `implement-approved-plan` (implementation-engineer); `refactor-code` (refactoring-engineer); `review-code`, `review-production-readiness`, and `review-architecture` (the matching reviewer); `prepare-pr` (code-reviewer). Claude Code runs them with `context: fork`. Copilot runs them inline in the main conversation, because Copilot CLI subagents cannot yet write files with these agents' tool lists; there the command still reads state only from the artifacts and the repository and does not rely on earlier conversation. Commands that need back-and-forth with the user — `capture-requirements`, `review-requirements`, the setup commands, and `migrate-oracle-to-postgres` — run in the main conversation.

A fresh-context command reads state only from the artifacts and the repository, and only the inputs it needs:

| Command | Reads |
| --- | --- |
| `create-plan` | requirements, product-level requirements, repository |
| `create-api-contract` | requirements, Plan, repository |
| `create-implementation-plan` | requirements, Plan, contract, earlier Implementation Plans (Carried-Forward Decisions), repository |
| `generate-tests` (RED) | requirements, Plan, contract, its Implementation Plan, repository |
| `implement-approved-plan`, `refactor-code` | Plan (status and predecessor evidence), its Implementation Plan, repository |
| `review-code`, `review-production-readiness`, `review-architecture` | every artifact of the work item, repository |
| `prepare-pr` | Plan, contract, the Implementation Plans executed since the last commit, repository; in branch mode, the repository only |

RED reads the requirements and contract because it checks that each assertion matches them. FOUNDATION, GREEN, OTHER, and REFACTOR execution applies exact code that the approved Implementation Plan already holds, so it does not read them; a difference stops execution.

**Check the repository state first.** Every command, planning included, compares the working tree and its commits with what `Plan.md` records. Uncommitted changes are expected only for the files of milestones that Execution Status records as executed since its last `Committed as <hash>` entry, and for `docs/.ai/<work-item>/`. Any other uncommitted, untracked, or committed-but-unrecorded change is unplanned: stop and report it (`Stopped — awaiting user: <the changes>`) instead of building on it. `prepare-pr` commits each finished milestone together with `docs/.ai/<work-item>/`, so a new clone, worktree, or session sees the artifacts.

**Answers to a command's questions are recorded in the artifact, never left in the conversation.** When the user answers questions a fresh-context command stopped on, the next run takes those answers quoted after the work item (for example `create-implementation-plan <work-item> answers: OQ-1 "…"`) and records each one in the artifact it writes, under its question ID, as `[User: <ID>, <date>]`. The main conversation does not edit the artifact itself.

Its report ends with exactly one of: what it wrote or executed, with its evidence; `Stopped — awaiting user: <questions, or the approval needed>`; or `Blocked — <reason>`. It holds nothing else: no recap of the steps taken and no restatement of the artifact. The main conversation relays the report; the user answers there, and any approval is recorded in the artifact (Approval Status) before the next command runs.

Every PDD command's report then closes with one `Next:` line naming the step that follows: the approval needed and the next command with its work item (for example `Next: approve Plan.md, then create-implementation-plan order-cancellation`), the answers needed, or `Next: none — work item closed`. In Copilot, run each fresh-context command above in a new chat. Copilot runs them inline, so a new chat is what keeps the earlier conversation out. Record any pending approval in the artifact before switching chats. In Claude Code these commands already run in a fresh context, but the main conversation still grows with every report and approval, so start a new chat after the requirements are approved and after each executed GREEN, OTHER, or REFACTOR milestone; the artifacts hold all the state. A `Next:` line that crosses one of these points ends with `(new chat)`.

## Test Scope and Output

Run tests scoped to the change, and the full suite once per milestone that changes production or build code.

| Step | Tests run |
| --- | --- |
| RED dry run and RED execution | Compile everything; only the new tests, each failing for the intended reason; plus tests that use a shared test file the milestone changes |
| GREEN, FOUNDATION, OTHER, REFACTOR dry run | Compile; the new and affected tests, once |
| GREEN execution | The full suite once; a second run only for tests that touch persistent state or override configuration (`implementation-planning` Repeatable, Isolated Verification) |
| FOUNDATION, OTHER execution | Build and the checks the plan names; the full suite once when production or build files change |
| REFACTOR execution | The full suite once after the change; the baseline is the recorded GREEN run unless the repository changed since |
| `prepare-pr` | The full suite once, unless the working tree is clean apart from `docs/.ai/` and `Plan.md` records a full run at the current commit; always once in branch mode |
| Final Review | Rerun only when no full run is recorded for the current repository state |

The Implementation Plan lists the affected tests and how they were found (tests in the changed packages, tests that reference changed classes, tests the contract names); the user approves the list with the plan. A known flaky test follows `implementation-planning` Pre-existing Failures.

Test output:

- Write each verification command's output to a log file, and record only its summary (for example `Tests run`, `BUILD SUCCESS`) and the failing tests. Never copy the full log into the conversation or an artifact.
- Run a long command in the background with a completion notice where the tool supports it. Do not poll.
- The gate still waits: a milestone is complete only after the result is read and recorded in `Plan.md`.

## Plan Content Rules

The Plan defines WHAT is delivered and in which milestone order. It does not define HOW (Implementation Plans) or externally observable behavior (the API/external contract). When creating or revising a Plan:

1. **Milestone order.** Record every milestone in one strictly linear sequence. Each milestone has exactly one predecessor — Plan approval for the first milestone, otherwise one earlier milestone. Do not record parallel, optional, or "logically but not strictly required" predecessors. When a CONTRACT milestone exists it is the first milestone; any FOUNDATION milestone follows it.
2. **Contract-owned decisions stay in the contract.** Do not fix endpoint paths, operations/methods, status codes, parameter or field names, request/response schemas, validation rules, error behavior, result shapes for empty or missing data, or any decision the requirements defer to the contract — not even as examples, defaults, or "X or per contract" hints. Reference the contract artifact instead. The CONTRACT milestone's decision list contains the decisions the requirements defer to it plus the externally observable behavior needed to define the required operations — nothing else (no documentation formats, tooling, or extra capabilities). A decision the requirements explicitly defer to a CONTRACT milestone is owned by that milestone; it does not block Plan approval and must not be resolved, narrowed, or presumed in the Plan. When the requirements require externally settable configuration (environment variables, configuration keys, profiles), the names and shapes operators set are contract decisions; with no CONTRACT milestone, the first Implementation Plan that needs them decides them for review, and later Implementation Plans carry them forward (`implementation-planning` Carried-Forward Decisions).
3. **No internal design.** Do not name classes, files, methods, interfaces, packages, framework annotations, libraries or dependencies beyond the approved technology stack, test classes, mocking or test-isolation strategies, or internal layering within a milestone. Describe each milestone by the behavior and requirements it covers. Naming a decomposition boundary (for example a layer or capability chosen under Adaptive Milestone Decomposition) is allowed; prescribing its internal structure is not. This rule governs milestone descriptions; Current State, Risks, and an OTHER or standalone REFACTOR milestone's preserved-test list or a RED milestone's existing failing test may name existing files, tests, and configuration as repository facts.
4. **RED milestones deliver tests/checks only.** State the behaviors the tests must verify. Never list production types, scaffolding, or configuration as RED deliverables. When the RED evidence is an existing failing test (Failing Tests: RED or OTHER), name that test and the requirement it expresses; the milestone changes no file.
5. **GREEN milestones deliver behavior.** State the behavior that makes the predecessor RED evidence pass. Do not list production classes or components.
6. **FOUNDATION is prerequisite-only.** Limit it to the build, dependency, bootstrap, configuration, or test-infrastructure prerequisites that the RED milestones it serves need to execute — which may be more than the immediately following RED milestone (see rule 11) — consistent with approved requirements (never an alternative the requirements exclude). The domain model, schema derived from it, and target behavior belong to GREEN.
7. **Complete milestone entries.** Every milestone records every field the Plan template requires, including explicit exclusions and success criteria.
8. **Single ownership.** Every approved requirement and cross-cutting concern has exactly one owning delivery milestone, recorded in the Plan's requirement traceability. The owning milestone delivers it (GREEN for behavior, CONTRACT for contract decisions, FOUNDATION for prerequisites, REFACTOR for a standalone restructuring requirement, OTHER for an approved change with no behavior change); the verifying milestone is the RED milestone whose tests verify it (or human review for a CONTRACT decision, or the OTHER or standalone REFACTOR milestone itself through its baseline evidence and preserved tests). No requirement has two owners. Four kinds of row have no owning milestone, and each uses its own form. A requirement that states an absence (for example "no X is required") is an exclusion — must not be introduced — verified at Final Review; a characteristic recorded as not required for this work item has nothing to verify and is never called an exclusion; preserved existing behavior is verified by the milestone whose preserved tests cover it; a requirement the Final Review itself fulfils (for example a statement the Final Review must make) is a Final Review obligation, answered in the Final Review. Never assign one of these to a delivery milestone or claim a RED milestone verifies it. Every requirement that the traceability names a RED milestone as verifying appears in that RED milestone's scope, and that RED milestone's scope verifies nothing the traceability does not assign to it.
9. **No invented scope.** Do not add requirements, non-functional targets, coverage thresholds, exclusions, or constraints that are not in approved requirements or repository evidence. Out of Scope lists only exclusions the requirements state. Current State describes only what inspection of the repository shows. When the work item changes existing code, Current State lists the existing behavior the work item affects and the existing tests that cover it; for a new project with no code yet, it says so. Risks and mitigations must not weaken, reinterpret, or contradict a requirement or reassign a decision to a different milestone. A mitigation may reference only in-scope work; one that needs new scope is a clarification question, not a plan item. Risks cite repository evidence. The Plan does not prescribe commits, branches, pull requests, owners, or other delivery process unless the requirements state it.
10. **Honest status.** A newly created Plan records every milestone as Pending and marks nothing approved, verified, or complete. A revision keeps every executed milestone, its status, and its evidence unchanged; only changed or new milestones are Pending.
11. **Prerequisite coverage for every RED milestone.** RED milestones cannot add dependencies, build configuration, or test infrastructure, and GREEN comes after RED, so every prerequisite a RED milestone needs must already exist when it starts. Walk the whole sequence: for each RED milestone, determine what its tests need to compile and run (dependencies, test infrastructure, configuration) given the repository state projected after all of its predecessor milestones complete — not only the current state. If any prerequisite is not provided by a predecessor, either widen an earlier FOUNDATION milestone to provide it or insert a FOUNDATION milestone immediately before that RED milestone. Record which RED milestones each FOUNDATION milestone serves.
12. **Criteria coverage.** Every acceptance criterion in the requirements and every Plan-level success criterion appears in Final Acceptance Criteria with the milestone whose completion evidence demonstrates it, or Final Review inspection. That milestone must be able to produce the evidence — for example, a RED milestone cannot demonstrate that the application runs. Every artifact a verification step uses is in some milestone's scope.
13. **Verification commands.** Record the commands that verify milestones in the Plan's Verification Commands section, each with its source (requirements, or repository evidence such as the build file or project documentation). Do not take them from the application instruction file, which holds no project facts. For a project with no build yet, state that the FOUNDATION milestone establishes them; its Implementation Plan records the exact commands.

## Plan Integrity

Before approval, the Plan is a working proposal and may be revised freely in response to human review. Human approval makes it the execution baseline: an authorization artifact and a living execution-status record that the AI never changes silently. Material unresolved decisions are resolved before approval. After approval, never rewrite the Plan to match implementation, change milestone definitions during execution, or expand scope for a technically useful improvement; only execution status changes (Plan Progress). Scope, milestone, architecture, or success-criteria changes need explicit replanning and human review.

If execution reveals that the approved Plan itself must change, stop for replanning and human review. Replanning is allowed at any point, including after implementation has started; the control is human approval, not immutability. When a blocker materially invalidates approved scope, milestone order, architecture, assumptions, or acceptance criteria:

1. The execution command stops. It records the milestone in `Plan.md` Execution Status as `Blocked — <reason>`, with its evidence below the table, and records in the Implementation Plan's Human Review status: `Execution stopped at a blocker — see Plan.md. Re-approval required before execution.` It describes the minimum Plan revision in its report and changes nothing else in `Plan.md`.
2. Any change to scope, milestones, architecture, or acceptance criteria is made only through `create-plan` revision mode, which addresses every `Blocked` row, replaces it with the revised milestone's Pending row, and keeps executed milestones and their evidence unchanged.
3. The revised Plan returns to awaiting human review.
4. Execution resumes only after the user approves the revised Plan, and the affected milestone runs only from a new Implementation Plan or the user's recorded re-approval of the existing one.

When execution shows that an approved contract decision cannot be met, use the same stop (step 1), naming the contract decision and the evidence. Then:

1. `create-api-contract` revision mode changes only that decision and records it in the contract's Amendments section: the change, the reason with its evidence, the impact, and the executed milestones whose tests or code encode the old decision. The amended contract returns to awaiting review.
2. `create-plan` revision mode adds new Pending milestones that bring the executed work the amendment lists into line with the amended contract. Each has its own name and is typed by the kind of change it makes (Milestone Types) — for example, a test that encodes the old decision is updated in an OTHER or RED milestone, and a production change is a RED and GREEN pair. None is labelled or numbered as part of an executed milestone. They are placed before the revised Blocked milestone, each with its own Implementation Plan numbered as the next `NNN`. The executed milestones' rows and evidence stay unchanged.
3. Execution resumes only after the user approves both the amended contract and the revised Plan.

Never replan and continue executing without that approval.

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

## Plan Progress

After an approved milestone is executed and verified, update only the Execution Status section of `Plan.md`: record the completed milestone and its evidence, and never rewrite requirements, scope, architecture, exclusions, success criteria, or future milestones. After `prepare-pr` commits the milestone, add `Committed as <hash>` to its row; changes only under `docs/.ai/` since that commit count as the same tested state. If verification fails or does not show the intended evidence, the milestone is not complete.

Execution Status values are `Pending`, `Waiting — <named input> from <who>`, `Blocked — <reason>`, and completed with evidence. `Waiting` records that an approved milestone cannot start or continue until the user supplies a named input or performs a named action (for example images, a deployment, or credentials the user enters). The Plan stays valid and the milestone resumes on the same approved Implementation Plan once the input exists; only `Blocked` needs replanning.

Evidence is each command as actually run with its trimmed real output (its summary and failing tests, never the full log; Test Scope and Output), stored in `Plan.md` below the Execution Status table (or in a file it links) — never a statement that output was recorded elsewhere. Each Execution Status row stays on one line and points to its evidence. Any difference between a planned and an executed command (arguments, port, profile, order) is listed as a deviation with its reason. Every process the executor started (servers, containers, background jobs) is stopped before reporting, and the report says so.

## Final Review Authority

Final Review of a work item is performed only by `review-code` or `review-production-readiness`, when the user names the work item. Other reviews — for example `review-architecture` or `review-requirements` — are intermediate and do not close the work item. Any review produces findings and recommendations only; a finding is not an authorized change. Never apply one directly to code, tests, or configuration: a finding that needs an executable change goes through the normal chain — the authoritative artifact when scope changes, then a new or amended Implementation Plan (a fix work item, Fix Work Items), RED before GREEN when behavior or validation changes. There is no trivial-change exception for executable artifacts.

When a review is the Final Review of a Plan, write it to `docs/.ai/<work-item>/Final-Review.md` — the verdict, each Final Acceptance Criterion with its evidence, an answer to every Final Review obligation row in the Plan's traceability, the findings, and the recommendation — and add a Final Review row to `Plan.md` Execution Status pointing to it, with the status "Written — awaiting user decision" (never "Completed"). Change no other file. Accepting the findings is the user's decision, recorded by the user in that file. Final-Review.md also lists each product-level statement now out of date in `docs/requirements.md`, and each statement in user-facing documentation such as README files that the work item made false, for the user to update; the review does not edit them.

- Use `templates/Final-Review.md` for the structure, and mark each finding as pre-existing or introduced by the work item.
- Before raising a finding, read `Plan.md` Execution Status evidence and the approved Implementation Plans; drop any finding that recorded evidence or an approved decision contradicts.
- Never recommend reverting an approved decision as a fix; raise it as a question for the user.
- Give a severity only with a concrete failure scenario, and cite the correct path.
- An error in an earlier approved artifact (for example a wrong explanation in an Implementation Plan) is recorded as a finding in Final-Review.md; do not edit the approved artifact.

## Task Prompt Boundary

Persistent instructions, agents, and skills do not replace the active task prompt. The active task still identifies its authorization boundary, as applicable: goal, authoritative inputs, current milestone and its type, requested output, files or areas allowed to change, milestone-specific constraints, and success criteria.

Role belongs to the selected agent. Reusable engineering knowledge belongs to skills. Stable governance belongs to instructions.

## Scope Control

Do not invent requirements or non-functional requirements, pull future milestone work into the current task, introduce unrelated dependencies, infrastructure, observability, resilience, or architecture changes, or treat engineering best practices as authorization to expand scope.

When a material unresolved decision blocks the current artifact or change, apply the requirements-analysis clarification gate: ask, stop, and wait.

Use the templates in `templates/` when the adopting project does not already define compatible artifacts. Template guidance is written in HTML comments (`<!-- … -->`); remove every template comment from the finished artifact. This does not apply to the application instruction templates (`application-claude-instructions.md`, `application-copilot-instructions.md`), whose setup commands copy them byte for byte, comments included.
