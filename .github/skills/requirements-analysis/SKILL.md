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

## Non-Blocking Decisions

If a decision does not affect correctness or approved scope of the current task:

- record the boundary explicitly when useful;
- prefer the smallest conservative interpretation;
- do not allow the choice to expand the milestone;
- leave it for a later phase when appropriate.
