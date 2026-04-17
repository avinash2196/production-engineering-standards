# Create Doc Workflow

Step-by-step process for creating any new `.md` file in this repo.

## When to Use This

Use this workflow any time you are creating:
- A README for a new service, stack, or tool
- An Architecture Decision Record (ADR)
- A runbook or operational guide
- A new standard or coding guideline
- A template document
- Any agent-facing guide with LLM instructions

Do **not** use this for minor edits to existing docs — edit in place.

## Step 1: Determine If the Doc Already Exists

Search before creating:

```bash
# Search by likely title keywords
grep -r "<keyword>" docs/ standards/ stacks/ playbooks/ templates/ --include="*.md" -l

# Check for similar files in the same directory
ls standards/   # or the relevant folder
```

If a related doc exists, prefer updating it over creating a duplicate. If it's genuinely new, continue to Step 2.

## Step 2: Ask the Five Questions

Before writing, gather answers to these questions in a single message to the user.  
Skip any question that is obvious from context.

| # | Question | Options / Guidance |
|---|----------|--------------------|
| 1 | **Type** — What kind of document is this? | `README` · `ADR` · `runbook` · `standard` · `guide` · `template` · `changelog` · `other` |
| 2 | **Audience** — Who will primarily read it? | `developer` · `ops/SRE` · `tech lead` · `external contributor` · `agent/LLM` · `mixed` |
| 3 | **Scope** — What does it cover, and what is explicitly out of scope? | Free text, 1–2 sentences |
| 4 | **Inputs** — What context already exists? | Code, related docs, ADR number, design notes, Jira ticket |
| 5 | **Cross-links** — Which existing docs should reference this, and which should this reference? | Free text or "none" |

**Never ask more than 5 questions.** If context makes some obvious, drop them.

## Step 3: Select the Template

Match the doc type to a template in `templates/docs/`:

| Doc type | Template |
|----------|----------|
| Service README | `templates/docs/service-readme-template.md` |
| Project copilot instructions | `templates/docs/project-copilot-instructions-bootstrap.md` |
| Local standards | `templates/docs/local-standards-template.md` |
| Repo instructions | `templates/docs/repo-instructions-template.md` |
| ADR | No template yet — use standard ADR format (see below) |
| Runbook | No template yet — use standard runbook format (see below) |
| New standard | Copy structure from any file in `standards/` |

If no template matches, create the file from scratch using the section guidelines in Step 4.

### ADR Format (when no template exists)

```markdown
# ADR-NNN: <Title>

**Date:** YYYY-MM-DD  
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-NNN  
**Deciders:** <names or roles>

## Context

<What situation or problem led to this decision?>

## Decision

<What was decided?>

## Consequences

### Positive
- ...

### Negative / Trade-offs
- ...

## Alternatives Considered

| Option | Why rejected |
|--------|-------------|
| ... | ... |
```

### Runbook Format (when no template exists)

```markdown
# Runbook: <Service or Process Name>

**Owner:** <team or role>  
**Last verified:** YYYY-MM-DD  
**Alert source:** <PagerDuty policy / Grafana alert name>

## Symptoms

<What does the problem look like? What alert fires?>

## Immediate Actions (< 5 min)

1. ...
2. ...

## Diagnosis Steps

1. ...

## Fix

<Commands or steps to resolve>

## Escalation

<When to escalate and to whom>

## Post-Incident

- [ ] File incident report
- [ ] Update runbook if steps were wrong
```

## Step 4: Required Sections for Agent-Facing Docs

Any doc intended to guide agent or LLM behaviour (standards, architecture guides, capability specs) **must** include these two sections at the end:

```markdown
## LLM Instructions

- <directive 1 — imperative, specific>
- <directive 2>

## Review Checklist

- [ ] <what to verify before the work is done>
- [ ] <second check>
```

## Step 5: Naming and Placement

Follow `standards/naming.md`. Key rules:

| Doc type | Location | Naming |
|----------|----------|--------|
| Service README | `/examples/<name>/README.md` or `/stacks/<name>/README.md` | `README.md` |
| ADR | `docs/decisions/ADR-NNN-<kebab-title>.md` | Zero-padded 3-digit number |
| Runbook | `docs/runbooks/<kebab-name>.md` | `kebab-case.md` |
| Standard | `standards/<kebab-name>.md` | `kebab-case.md` |
| Workflow | `playbooks/<kebab-name>.md` | `kebab-case.md` |
| Agent-facing guide | `agents/<kebab-name>.md` | `kebab-name.md` |

## Step 6: Write the Plan (if doc is large)

If the document will have more than 5 sections or requires reading multiple existing files, follow [agent-execution.md](../standards/agent-execution.md) and write a plan file first at `.copilot/plans/`.

## Step 7: Cross-Link

After creating the file:

1. **Add links from the new doc** to every related document identified in Step 2.
2. **Add a link to the new doc** from every document that should reference it.
3. Update the relevant `README.md` index if one exists.
4. If the doc is a new standard, add a row to the Standards table in `.github/copilot-instructions.md`.

## Step 8: Verify

- [ ] File is in the correct location per `standards/naming.md`
- [ ] Template structure followed
- [ ] Agent-facing docs have `## LLM Instructions` and `## Review Checklist`
- [ ] All cross-links added in both directions
- [ ] No duplicate doc exists covering the same topic
- [ ] `.github/copilot-instructions.md` updated if this is a new standard

## LLM Instructions

- Before creating any new `.md` file, ask the five questions (Step 2) in a single message. Never skip this step.
- Search for an existing doc on the same topic before creating a new one. Use `grep` or file search in the same folder.
- Always select a template from `templates/docs/` or use the standard ADR/runbook format defined in this workflow.
- Add `## LLM Instructions` and `## Review Checklist` to any doc intended to guide agent behaviour.
- After creating a file, always run the cross-link step (Step 7).
- If the new document is a standard, add it to the Standards table in `.github/copilot-instructions.md`.

## Review Checklist

- [ ] Five questions asked and answered before writing started
- [ ] Duplicate search done
- [ ] Correct template used
- [ ] File placed in correct directory per naming standard
- [ ] LLM Instructions + Review Checklist present (if agent-facing)
- [ ] Cross-links added in both directions
- [ ] copilot-instructions.md updated if this is a new standard

## References

- [standards/agent-execution.md](../standards/agent-execution.md)
- [standards/naming.md](../standards/naming.md)
- [templates/docs/](../templates/docs/)
