---
name: requirements-analysis
description: Use before requirements review, contract definition, or planning to separate explicit requirements, repository-confirmed facts, material unresolved decisions, and optional/non-blocking decisions. Especially important when requirements are incomplete, ambiguous, or conflicting.
---

# Requirements Analysis

Classify information as:

1. explicit requirement,
2. repository-confirmed fact,
3. material unresolved decision,
4. optional/non-blocking decision.

Do not promote framework defaults, industry conventions, repository conventions, or personal preference into requirements.

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

- Ask only what applies to this system, in one round together with any other clarification questions. For an enhancement, ask only about characteristics the work item could change or depends on.
- Deployment topology and consistency/concurrency are material: while unanswered, they block planning.
- For the others, "not required for this work item" is a valid answer. Record it as an explicit exclusion, never as a silent default.
- Record every answer in the work item's requirements (Recording Resolved Decisions). Operational requirements are then owned by milestones like any other requirement; `architecture-design`, `distributed-systems`, `observability`, and `resilience-and-degradation` apply when a recorded requirement calls for them.
- Ask about needs, not solutions. Do not propose technologies, patterns, or infrastructure while asking.

## Presenting Clarification Questions

Present questions in two groups so the user can see what actually blocks planning:

1. **Blocking — must be answered before planning:** material unresolved decisions, including deployment topology and consistency/concurrency. Keep this group to the minimum the current work item needs.
2. **Answer or mark not required:** applicable operational characteristics that are not blocking. For each, state that "not required for this work item" is a valid answer and will be recorded as an explicit exclusion.

Number questions continuously across both groups so answers can reference them.

## Recording Resolved Decisions

An answer to a clarification question is a decision, not conversation. A review that only analyzes requirements writes no files: it ends by listing each resolved decision with the requirement text it changes, and states that the requirements artifact must record them (through requirements capture) before planning relies on them. Downstream artifacts trace to the requirements artifact, never to conversation history.

## Non-Blocking Decisions

If a decision does not affect correctness or approved scope of the current task:

- record the boundary explicitly when useful;
- prefer the smallest conservative interpretation — except operational characteristics, which are asked (Operational Characteristics), never defaulted;
- do not allow the choice to expand the milestone;
- leave it for a later phase when appropriate.
