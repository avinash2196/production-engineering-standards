---
description: "Analyze requirements and repository evidence before planning. Do not implement."
argument-hint: "requirement, issue, or change request"
agent: "planner"
tools:
  - read
  - search
---
Apply the `requirements-analysis` skill. Separate explicit requirements, repository facts, material unknowns, and optional decisions. Ask only material clarification questions, including the applicable Operational Characteristics questions. Do not create implementation code.

Check provenance: flag any item without a source, any derived consequence presented as a user requirement or repository fact, any repository citation that does not match the current repository, and any qualitative term that decides testable behavior without a bound (`requirements-analysis` Material Clarification Gate).

When the named work item already has `docs/.ai/<work-item>/requirements.md`, review that artifact:

- a decision the artifact already records with a user label is settled — do not ask it again or list it to record;
- check internal consistency: Provenance Check statements against the labels actually used, overlapping or duplicate requirements, sections that contradict each other, requirements without an acceptance criterion, and Clarification Log numbering;
- ask only material requirement decisions; a question the build file, framework defaults, or repository can answer, or one that decides how rather than what, belongs to the Implementation Plan and is not asked.

End with a "Resolved decisions to record" list containing only decisions not yet in the artifact (`requirements-analysis` Recording Resolved Decisions), continuing the artifact's `Qn` numbering, then this block:

- `Verdict: Ready for human approval` or `Verdict: Blocked`
- blocking items, if any
- `Next step:` the exact PDD command — `capture-requirements` while anything must be recorded or resolved, otherwise human approval of the requirements, then `create-plan`.

Do not edit files.
