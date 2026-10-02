---
name: requirements-analysis
description: Use before requirements review, contract definition, or planning to separate explicit requirements, repository-confirmed facts, material unresolved decisions, and optional/non-blocking decisions. Especially important when requirements are incomplete, ambiguous, or conflicting.
---

# Requirements Analysis

Classify information as:

1. explicit requirement,
2. repository-confirmed fact,
3. material unresolved decision,
4. optional/non-blocking decision,
5. derived consequence — a statement inferred from user input, repository evidence, or another approved artifact rather than stated by the user or observed in the repository.

Do not promote framework defaults, industry conventions, repository conventions, or personal preference into requirements. Do not present a derived consequence as an explicit requirement or a repository-confirmed fact.

## Requirements Capture

When writing or updating a requirements artifact:

- **Inspect before asserting or asking.** Read the repository before stating any fact about it (build commands, language or runtime versions, profiles, external services, test counts) and before asking a clarification question. Never ask what inspection can answer. Record a repository fact only when inspection established it, and say where.
- **Preserve the user's meaning.** Record each user requirement with the same meaning — do not narrow, broaden, or reword it into a non-equivalent statement. When a paraphrase could change the meaning, quote the user's wording.
- **Requirements only.** The artifact holds requirements, constraints, explicit exclusions, acceptance criteria, resolved decisions, and repository-confirmed facts. Unless the user explicitly requires them, it does not hold build or test commands, branch or worktree names, stack traces, evidence snapshots, rollback strategy, solution shape (such as "a single minimal change"), or next steps — those belong to the Plan, the Implementation Plan, or verification evidence.
- **No recommended requirements.** Engineering recommendations from skills or checklists (observability, logging, flakiness handling, rollback, documentation, CI, compatibility) are not requirements. Include one only when the user stated it or repository evidence establishes it as a requirement.
- **Name every source.** Every requirement, constraint, exclusion, resolved decision, and repository fact names where it came from: the user (brief or numbered answer), repository inspection (path and line), an approved artifact of another work item this one explicitly depends on, or derivation. Use `prompt-driven-development` `templates/requirements.md` when the adopting project does not define a compatible requirements artifact.
- **Confirm derived consequences.** Label a derived consequence with what it is derived from and ask the user to confirm it before finalizing. Record it only after confirmation; until then it is an unresolved decision.
- **Options you wrote are not the user's words.** When the user picks a clarification option you wrote, record as the user's decision only what the user confirmed. Any further constraint implied by the option's wording is a derived consequence.
- **Existing behavior is a fact, not a requirement.** Existing tests and current behavior are repository-confirmed facts. When the work item affects behavior that existing tests assert, ask whether each affected behavior is kept, changed, or removed, and record a requirement only from the answer.
- **Confirm product-level supersession.** When the work item contradicts or replaces a statement in the product-level `docs/requirements.md`, that change is a derived consequence: ask the user to confirm it before recording the statement as changed, and never record a contradicted statement as still in force.
- **Every requirement has a criterion.** Every in-scope requirement maps to at least one acceptance criterion, and every criterion traces to a requirement. Report any unmapped item; add a criterion only from user-stated intent, otherwise ask.
- **Revise the whole artifact.** When updating an existing artifact, apply the requested changes, then re-read every section and table and resolve each statement the change contradicts. Moving an item means removing it from its old section. Re-derive the Provenance Check; never restate the previous one.
- **Other work items are context, not templates.** Do not copy another work item's structure, wording, citations, or closing statements. Re-verify any fact taken from another work item against the current repository before recording it.
- **Check provenance before finalizing.** Confirm that every item has a source, every derived consequence was confirmed, every repository citation was verified against the current repository during this capture, and that no statement about the artifact as a whole (for example "nothing was inferred") is made unless it was checked.

## Material Clarification Gate

A decision is material when it can change the correctness or approved scope of the current artifact or task, including:

- business behavior,
- API or external contract behavior,
- validation or error behavior,
- data ownership or representation,
- persistence semantics,
- security or authorization,
- compatibility,
- architecture boundaries,
- external integrations,
- deployment topology and consistency/concurrency guarantees,
- testing expectations,
- acceptance criteria,
- milestone boundaries.

When a material unresolved decision exists:

1. Ask the minimum focused clarification questions required.
2. Do not choose an answer on the user's behalf.
3. Do not convert the unresolved decision into an assumption or default.
4. Do not finalize, create, or update the downstream artifact that depends on the answer.
5. Stop the current workflow and wait for the user's response.

A material unresolved decision must not be hidden in an Open Questions section while the workflow continues as if the artifact were complete.

A qualitative term that decides testable behavior without a bound (for example "slow", "large", "soon", "high volume") is a material unresolved decision: bound it, or record it as explicitly deferred to a named later decision.

## Operational Characteristics

Requirements often describe behavior but say nothing about how the system must run. Do not assume either extreme — neither a single-user, single-instance system nor scale, distribution, or observability nobody asked for. Ask once, before planning.

When the requirements do not state them and neither the repository nor the product-level `docs/requirements.md` answers them, ask about the characteristics that apply to this system:

- **Scale:** expected users, request rate, data volume, and growth over the period this work item must support.
- **Deployment:** one running instance or several. Several instances change whether in-memory state, local locks, local caches, and scheduled jobs are correct.
- **Availability and latency:** uptime expectation, latency expectation for key operations, and tolerance for downtime during deployment.
- **Consistency and concurrency:** which operations must never conflict, duplicate, or be lost, and where eventual consistency is acceptable.
- **Dependency failure:** expected behavior when a downstream system is slow or unavailable, and whether the service must run locally or in CI without it (which decides whether local adapters are needed).
- **Observability:** what must be visible in production — logs, metrics, traces, alerts — and any existing monitoring stack to use.

Rules:

- Record an answer only when the user gave it or repository evidence establishes it. Never answer a characteristic on the user's behalf, and never add characteristics beyond the list above.
- Ask only what applies to this system, in one round together with any other clarification questions. For an enhancement, ask only about characteristics the work item could change or depends on.
- Deployment topology and consistency/concurrency are material: while unanswered, they block planning.
- For the others, "not required for this work item" is a valid answer. Record it explicitly as not required, never as a silent default. "Not required" means no milestone must deliver it; it is not an exclusion. Record a capability as excluded — must not be introduced — only when the user or an approved artifact excludes it.
- Record every answer in the work item's requirements (Recording Resolved Decisions). Operational requirements are then owned by milestones like any other requirement; `architecture-design`, `distributed-systems`, `observability`, and `resilience-and-degradation` apply when a recorded requirement calls for them.
- Ask about needs, not solutions. Do not propose technologies, patterns, or infrastructure while asking.

## Presenting Clarification Questions

Present questions in two groups so the user can see what actually blocks planning:

1. **Blocking — must be answered before planning:** material unresolved decisions, including deployment topology and consistency/concurrency. Keep this group to the minimum the current work item needs.
2. **Answer or mark not required:** applicable operational characteristics that are not blocking. For each, state that "not required for this work item" is a valid answer and will be recorded explicitly as not required.

Number questions continuously across both groups so answers can reference them. Numbering continues across every clarification round and every review of the same work item — never restart at 1 — and each question is recorded with its answer in the requirements artifact's Clarification Log, so every `[User: Qn]` label is traceable.

## Recording Resolved Decisions

An answer to a clarification question is a decision, not conversation. A review that only analyzes requirements writes no files: it ends by listing each resolved decision with the requirement text it changes, and states that the requirements artifact must record them (through requirements capture) before planning relies on them. Downstream artifacts trace to the requirements artifact, never to conversation history.

## Non-Blocking Decisions

If a decision does not affect correctness or approved scope of the current task:

- record the boundary explicitly when useful;
- prefer the smallest conservative interpretation — except operational characteristics, which are asked (Operational Characteristics), never defaulted;
- do not allow the choice to expand the milestone;
- leave it for a later phase when appropriate, labeled `[Left to <phase> — non-blocking]`, never `Derived`.

## Items No Milestone Delivers Now

Keep these kinds distinct; each has its own section or answer and is never relabeled as another:

| Kind | Meaning |
| --- | --- |
| Deferred | In scope for this work item; decided by a named later milestone |
| Non-blocking | Left to a later phase; does not change correctness or scope |
| Exclusion | Must not be introduced; stated by the user or an approved artifact |
| Not required | An operational characteristic the user marked not required; nothing to deliver; not an exclusion |
| Preserved behavior | Existing behavior the work item must leave unchanged |

Something outside the work item altogether is an exclusion only when the user or an approved artifact excludes it; otherwise it is simply not recorded.
