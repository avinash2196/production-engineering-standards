# Agent Execution Standard

Rules for how agents plan, checkpoint, and safely complete multi-step tasks.

## Purpose

Long-running agent tasks (scaffold, refactor, doc generation, fallback wiring) can touch dozens of files. Without a plan the work is opaque, hard to review mid-flight, and unrecoverable if the session is interrupted. This standard requires every heavy agent task to write a plan file first, implement against it, and checkpoint each step.

## When a Plan Is Required

A plan file **must** be written before any implementation starts when the task meets **any** of these conditions:

| Condition | Example |
|-----------|---------|
| Touches ≥ 4 files | Scaffold a new service |
| Creates or deletes directories | New stack, new feature module |
| Changes a shared standard | Updating fallback-strategy.md |
| Adds or removes wiring | New slash command, new capability interface |
| User says "do the whole thing" or "implement end-to-end" | Any open-ended request |

For tasks below these thresholds (e.g., fix a typo, add one field), write and implement directly — no plan needed.

## Plan File

### Location

```
.copilot/plans/YYYY-MM-DD-<task-slug>.md
```

Examples:
- `.copilot/plans/2026-04-16-scaffold-order-service.md`
- `.copilot/plans/2026-04-16-add-kafka-fallback.md`
- `.copilot/plans/2026-04-16-update-redis-docs.md`

Plans are **working files** — they do not need to be reviewed or merged like production code.

### Required Sections

```markdown
# Plan: <task title>

**Date:** YYYY-MM-DD
**Requested by:** <user request summary, one sentence>
**Scope:** <what is and is not included>

## Context Gathered

- Key files read: <list>
- Decisions made: <list any non-obvious choices and why>
- Open questions: <anything still uncertain — ask user before continuing>

## Steps

- [ ] Step 1: <specific, actionable description> — files affected: `path/to/file`
- [ ] Step 2: ...
- [ ] Step 3: ...
...

## Rollback Notes

How to undo if something goes wrong: <e.g., "all changes are additive — delete `.copilot/plans/` and revert edited files">
```

### Checkpoint Rules

1. **Mark `[x]` immediately after completing each step** — not in batch at the end.
2. **If a step fails**, stop, update the plan with the failure note, and report to the user before continuing.
3. **Never mark a step complete before it is done.** Partial completion is noted as `[-] Step N (partial): <what was done>`.
4. **After the final step**, add a `## Summary` section listing every file created/modified and any follow-up actions.

## Doc Creation Protocol

Applies whenever creating any `.md` file (README, runbook, ADR, standard, guide, template).

### Questions to Ask First (in one message, ≤ 5 questions)

Before writing a single line of the document, ask the user:

1. **Type** — What kind of document is this?
   - Options: `README` · `ADR` · `runbook` · `standard` · `guide` · `template` · `changelog` · `other`
2. **Audience** — Who will read it?
   - Options: `developer` · `ops/SRE` · `tech lead` · `external contributor` · `agent/LLM` · `mixed`
3. **Scope** — What does it cover and what does it explicitly exclude?
   - Free text, one or two sentences.
4. **Inputs available** — What context already exists?
   - Examples: existing code, related docs, ADR number, Jira ticket, design notes.
5. **Cross-links needed** — Are there other docs this should reference or that should reference it?
   - Free text or "none".

Skip questions that are obvious from context. Never ask more than 5.

### After Gathering Answers

1. Look up the matching template in `templates/docs/`.
2. Check for an existing doc in the same area to avoid duplication. If one exists, prefer updating it.
3. Follow naming conventions from `standards/naming.md`.
4. After creating the file, run the cross-link check: search for all docs that should reference the new file and add links.

### Mandatory Front Matter for Agent-Facing Docs

Any `.md` file intended to guide agent behavior (standards, guides, LLM instructions sections) must include:

```markdown
## LLM Instructions

- <directive 1>
- <directive 2>

## Review Checklist

- [ ] <check 1>
- [ ] <check 2>
```

## Agent Behaviour Rules

When operating under this standard, agents must:

- **Plan before touching files.** Write the plan file, present it to the user ("Here is my plan — proceeding unless you say stop"), wait 10 seconds (or until a message is received), then start.
- **Read before writing.** Always read a file before editing it. Never overwrite content you haven't seen.
- **Scope-lock.** Do not expand scope beyond the plan without updating the plan and noting the addition.
- **One concern per step.** Each plan step changes one file or one logical unit. Don't bundle unrelated edits.
- **Surface blockers immediately.** If a step cannot be completed (file missing, ambiguous requirement), stop and ask. Do not guess.

## LLM Instructions

- When a task qualifies for a plan (see table above), write the plan file at `.copilot/plans/` before any edits.
- Present the plan to the user with: "Plan written to `.copilot/plans/<filename>`. Proceeding with implementation — reply to stop or redirect."
- Check off each step in the plan as you complete it.
- When creating any `.md` file, ask the five Doc Creation Protocol questions first, then use matching template from `templates/docs/`.
- Never create a doc that duplicates an existing one — search first.

## Review Checklist

- [ ] Plan file exists at `.copilot/plans/` for all qualifying tasks
- [ ] All plan steps are checked off or have a failure note
- [ ] Summary section added after final step
- [ ] Doc creation questions were asked before writing
- [ ] Correct template used from `templates/docs/`
- [ ] Cross-links added in both directions (new doc → related, related → new doc)
- [ ] New agent-facing docs contain `## LLM Instructions` and `## Review Checklist` sections

## References

- [standards/naming.md](naming.md)
- [standards/coding-standards.md](coding-standards.md)
- [templates/docs/](../templates/docs/)
- [playbooks/create-doc.md](../playbooks/create-doc.md)
