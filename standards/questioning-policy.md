# Questioning Policy for Agents

## Purpose

This policy defines when AI-assisted engineering workflows must ask for clarification and when they should continue using established repository evidence. The goal is to prevent invented requirements without turning planning into unnecessary interrogation.

## Core Rule

Ask when missing, ambiguous, or contradictory information **materially affects the current decision or planning boundary** and cannot be resolved from approved repository evidence.

Do not guess through a material ambiguity. Do not ask about decisions that are irrelevant to the current scope or belong only to a later milestone.

Use the [Requirements Analysis Skill](../.github/skills/requirements-analysis/SKILL.md) before creating or materially updating a Plan.

## Agents MUST Ask When Materially Unresolved

Examples include:

1. **Business behavior or validation**
   - required vs optional fields;
   - state-transition rules;
   - duplicate-request behavior;
   - success/error semantics.

2. **Contract behavior**
   - endpoint/event semantics;
   - compatibility requirements;
   - ordering or delivery expectations.

3. **Data handling and privacy**
   - sensitive-data classification;
   - retention/deletion requirements;
   - whether logs, traces, or exports may contain protected data.

4. **Security or compliance behavior**
   - authorization policy;
   - trust boundaries;
   - explicitly applicable regulatory controls.

5. **Persistence and distributed-system correctness**
   - transaction boundaries;
   - consistency expectations;
   - idempotency or ordering requirements when duplicates/concurrency can affect correctness.

6. **External integrations**
   - an integration contract, ownership boundary, credential model, or failure expectation required for the current milestone.

7. **Current acceptance criteria**
   - a missing decision that changes required positive/negative tests or milestone success criteria.

## Agents SHOULD NOT Ask When

1. The answer is already explicit in the request, an approved Plan/Implementation Plan, contract, configuration, or current repository behavior that is authoritative for the task.
2. The choice is a trivial implementation detail covered by an adopted coding/style standard and does not change observable behavior.
3. The decision belongs only to a later milestone and does not constrain the current Plan.
4. The user explicitly selected an existing repository default and that default does not invent new business, security, compliance, or operational requirements.

## Questioning Behavior

- Ask the **smallest set of questions required to unblock the current decision**. There is no arbitrary numeric cap.
- Group related questions and make each question specific enough to produce an actionable answer.
- For a planning gate, when material ambiguity remains, ask numbered clarification questions and stop. Do not append a speculative Plan or implementation.
- Do not present a preferred default as though the user had selected it.
- You may explain technically valid options when the user asks for options or when trade-offs are necessary to answer a clarification, but clearly label them as options rather than requirements.
- Preserve unresolved later-milestone decisions instead of resolving them prematurely.

## Repository Defaults

Repository defaults may guide implementation mechanics only when the requirement and approved architecture already permit the choice.

A default must never invent:

- business behavior or validation;
- API/event semantics;
- data classification or retention;
- authorization policy;
- compliance obligations;
- SLO/reliability requirements;
- external dependencies;
- deployment architecture.

Local-adapter defaults may be used only when a relevant capability has already been selected and local development/CI explicitly needs that adapter. They are never implicit production fallback behavior.

## Compliance and Legal Boundaries

Agents must not fabricate legal conclusions or infer a compliance regime from industry vocabulary alone. They may explain engineering implications of explicitly adopted controls and should reference the relevant repository compliance standard when applicable.

For healthcare-related systems, terms such as `healthcare`, `patient`, or `medical` do not by themselves establish HIPAA scope. If regulatory scope or data classification materially changes the current Plan and is unresolved, ask.

## LLM Instructions

- Do not invent missing requirements.
- Use repository evidence before asking the user to repeat information.
- Ask only questions that materially affect the current scope.
- Stop planning when a material ambiguity remains.
- Do not pull later-milestone decisions forward.
- Never turn a recommendation or default into an unstated requirement.

## Review Checklist

- [ ] Every clarification question is material to the current scope.
- [ ] Existing repository evidence was checked first.
- [ ] No arbitrary question-count limit suppressed a necessary clarification.
- [ ] Defaults were not used to invent behavior or compliance obligations.
- [ ] Later-milestone decisions were left for the appropriate milestone.
- [ ] Healthcare/compliance context was not inferred beyond explicit evidence.
