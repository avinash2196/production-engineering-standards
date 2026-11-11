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

The API/external contract is required when the work item creates or changes externally observable behavior that must be defined before implementation, such as an HTTP API or another stable consumer-facing interface. When required, it is delivered by a CONTRACT milestone recorded in `Plan.md`. When the work item leaves an existing contract unchanged, that contract is a constraint the Plan references — not a CONTRACT milestone; do not record a milestone to restate, archive, or re-publish an unchanged contract. When the work item changes an existing contract, the CONTRACT milestone starts from that contract as its baseline (`plan-rules.md` Changed Contracts).

A CONTRACT milestone, when present, is always the first milestone after Plan approval. It precedes every FOUNDATION, RED, GREEN, REFACTOR, and OTHER milestone, because no repository-changing milestone may start before the externally observable behavior it depends on is approved. Its deliverable is the API/external contract artifact itself; it changes no executable artifact, so it has no Implementation Plan — the contract artifact is the human-reviewed deliverable.

CONTRACT, FOUNDATION, RED, GREEN, REFACTOR, and OTHER are each their own milestone, not phases nested inside a containing milestone. A single Implementation Plan authorizes exactly one milestone and no work for any other. The one exception is a paired plan (`Decomposition: one pair, one plan`, Adaptive Milestone Decomposition): one Implementation Plan for exactly one RED milestone and the GREEN milestone it pairs with. Completing one milestone never authorizes the next. FOUNDATION is conditional (Conditional SETUP / FOUNDATION); most sequences proceed directly to a RED milestone.

## Parts

This core holds the rules every PDD command needs. The other sections are in files in this skill's folder, read on demand. A reference such as "`prompt-driven-development` Test Scope and Output" names a section in whichever file holds it.

| File | Sections | Read up front by |
| --- | --- | --- |
| `SKILL.md` (this core) | Lifecycle, Milestone Types (table), Work-Item Folders, Artifact Authority, Approval Status, Fresh Context, Task Prompt Boundary, Scope Control | every PDD command |
| `milestone-types.md` | Failing Tests: RED or OTHER, Standalone REFACTOR, OTHER, Only RED Ends Failing, Fix Work Items, Milestone Controls (Adaptive Milestone Decomposition, Conditional SETUP / FOUNDATION) | `create-plan`, `create-implementation-plan`, `generate-tests`, Final Reviews |
| `plan-rules.md` | Plan Content Rules, Changed Contracts | `create-plan`, `create-api-contract`, Final Reviews |
| `execution.md` | Implementation Plan, Test Scope and Output, Plan Integrity, Plan Progress | `create-implementation-plan`, `generate-tests`, `implement-approved-plan`, `refactor-code`, `prepare-pr`, Final Reviews |
| `final-review.md` | Final Review Authority | `review-code`, `review-production-readiness` |

A command reads another part whenever a rule it applies points there (for example a Plan Content Rule number).

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
- Another work item's artifacts never authorize work in the current one. Completed work items are history, not authority — and not templates: build each artifact from the templates in `templates/`, the user's input, and the current repository, not by copying another work item's structure, wording, or citations. The one exception is a changed external contract, which starts from the verified current contract as its baseline (`plan-rules.md` Changed Contracts).
- An optional product-level `docs/requirements.md` describes the product as a whole. PDD commands may read it as context but never edit it. The work item's `requirements.md` is authoritative for the work item and states which product-level behavior it changes; any other material conflict between the two stops the workflow for human review. Only the user updates `docs/requirements.md`; Final Review lists the product-level statements a work item has made out of date.

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

## Task Prompt Boundary

Persistent instructions, agents, and skills do not replace the active task prompt. The active task still identifies its authorization boundary, as applicable: goal, authoritative inputs, current milestone and its type, requested output, files or areas allowed to change, milestone-specific constraints, and success criteria.

Role belongs to the selected agent. Reusable engineering knowledge belongs to skills. Stable governance belongs to instructions.

## Scope Control

Do not invent requirements or non-functional requirements, pull future milestone work into the current task, introduce unrelated dependencies, infrastructure, observability, resilience, or architecture changes, or treat engineering best practices as authorization to expand scope.

When a material unresolved decision blocks the current artifact or change, apply the requirements-analysis clarification gate: ask, stop, and wait.

Use the templates in `templates/` when the adopting project does not already define compatible artifacts. Template guidance is written in HTML comments (`<!-- … -->`); remove every template comment from the finished artifact. This does not apply to the application instruction templates (`application-claude-instructions.md`, `application-copilot-instructions.md`), whose setup commands copy them byte for byte, comments included.
