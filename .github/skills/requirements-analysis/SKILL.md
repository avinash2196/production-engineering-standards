---
name: requirements-analysis
description: Review software requirements before planning. Use when creating or reviewing a Plan, scaffolding a service, or when requirements may be incomplete, ambiguous, contradictory, or unsupported by repository evidence.
---

# Requirements Analysis

Use this skill as the gate between **Requirements** and **Plan** in the repository's Prompt-Driven Development workflow.

This skill does not create requirements. It does not make product, legal, security, compliance, architecture, or operational decisions on the user's behalf.

## Required Behavior

1. Read the supplied requirement or user request without broadening it.
2. Read enough current repository context to understand what is already established. Relevant evidence may include approved planning artifacts, contracts, code, tests, configuration, schemas, migrations, and adopted standards.
3. For each planning-relevant decision, classify the evidence as:
   - `EXPLICIT` — directly stated by the user or requirement;
   - `REPOSITORY-CONFIRMED` — established by current repository evidence or an approved decision;
   - `UNRESOLVED` — missing, ambiguous, or contradictory and material now;
   - `NOT REQUIRED YET` — may be needed later but does not affect the current planning boundary.
4. Never promote a guess, common engineering practice, framework default, industry convention, prior example, or probable future need into `EXPLICIT` or `REPOSITORY-CONFIRMED`.
5. When an `UNRESOLVED` item materially affects correct planning, ask the smallest set of numbered clarification questions and stop before Plan creation.
6. Do not ask questions for decisions that belong only to a later milestone. Record them as `NOT REQUIRED YET` until they become material.
7. If requirements and repository evidence conflict, treat the conflict as `UNRESOLVED` unless an approved artifact clearly establishes precedence.

## Material Decisions

Treat a gap as material when it can change the current Plan's:

- business behavior, domain rules, or validation;
- API/event contract or compatibility behavior;
- data classification, retention, privacy, or security behavior;
- persistence, transaction, consistency, ordering, idempotency, or integration behavior;
- acceptance criteria or required positive/negative tests;
- explicitly in-scope reliability, availability, latency, or recovery behavior;
- explicitly applicable compliance controls;
- milestone scope, sequencing, or success criteria.

For sensitive or healthcare-related data, do not infer HIPAA applicability merely from domain vocabulary. If data classification or regulatory scope materially changes the Plan and is not explicit, ask.

## Defaults

Repository defaults may guide implementation mechanics only after the requirement and approved architecture permit the choice.

Defaults must never invent:

- business behavior;
- validation rules;
- endpoints or event semantics;
- data retention or classification;
- authorization policy;
- compliance obligations;
- reliability/SLO requirements;
- external dependencies;
- deployment architecture.

## Result Contract

Return one of two outcomes:

### `CLARIFICATION REQUIRED`

Output numbered questions only. Do not create a Plan, propose a default, or continue into implementation.

### `READY FOR PLANNING`

State the explicit and repository-confirmed evidence that is sufficient for the current planning boundary. Clearly identify decisions that are `NOT REQUIRED YET` without resolving them early.

## Review Checklist

- [ ] Requirement text was read before repository assumptions were considered.
- [ ] Current repository evidence was checked where relevant.
- [ ] No inferred behavior was presented as a requirement.
- [ ] Contradictions were surfaced rather than silently resolved.
- [ ] Only material, current-boundary questions were asked.
- [ ] Later-milestone decisions were not pulled forward unnecessarily.
- [ ] Planning proceeds only when no material `UNRESOLVED` item remains.
