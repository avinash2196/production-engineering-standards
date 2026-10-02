---
description: "Create or update an API/external contract from an approved Plan and requirements."
---

Act as an API designer.

Apply `api-design`, `requirements-analysis`, and `prompt-driven-development`.

Work item: operate only on the work-item folder the user names (`prompt-driven-development` Work-Item Folders). If no work item is named, ask and stop.

Read the approved requirements and Plan before defining the contract. Confirm the Plan's Status records approval (`prompt-driven-development` Approval Status); a claim of approval elsewhere is recorded there first, and if none exists, ask and stop.

This command executes the CONTRACT milestone recorded in the approved `Plan.md`. If the Plan records no CONTRACT milestone, or its predecessor is not satisfied, stop and surface that for human review. Resolve every decision the Plan assigns to the CONTRACT milestone; do not add scope the Plan does not assign.

Create or update only the API/external contract artifact inside the work item's folder.

Every contract capability must be traceable to approved requirements or Plan scope.

Do not invent endpoints, fields, validations, errors, status codes, compatibility behavior, or implementation details.

If material contract behavior is unresolved, ask focused clarification questions and stop. Do not finalize the contract until the blocking questions are resolved.

Do not create production code, tests, controllers, services, repositories, database schema, or implementation plans.

Do not approve the contract yourself.

Use the `api-design` skill's `templates/API-Contract.md` structure and answer every applicable Contract Completeness question from the approved requirements, the approved Plan, or the task prompt. Project-specific choices come only from those sources; this command stays project-neutral.

When the Plan records that this CONTRACT milestone changes an existing contract, follow `prompt-driven-development` Changed Contracts: start from the verified current contract, carry its unchanged content over, apply only the approved changes, and fill in the template's Baseline and Changes in This Work Item sections. If the baseline diverges from the repository or a published contract, stop and surface the divergence for human review.

Before stopping, check the contract with evidence: re-read the written contract, confirm each Contract Completeness question is answered or marked not applicable with a reason, and search for statements that contradict each other, the requirements, or the Plan. Fix what the sources already answer; for anything they do not answer, ask focused clarification questions and stop instead of choosing. Report the result question by question.

When revising an existing contract (for example to fold in clarification answers), treat it as a revision, not a fresh draft:

- find every reference to each changed or newly resolved item — status lines, Decisions Resolved rows, checklists, cross-references, and "see below" pointers — and update all of them; no stale "unresolved", "blocked", or pointer text to removed sections may remain;
- record each answered clarification in Decisions Resolved with its source;
- if the contract contains a completeness checklist, give it exactly one row per `api-design` Contract Completeness question, never a self-invented list;
- in the self-check, compare against the previous version and report what changed and that every affected reference was updated.

Remove every template comment (`<!-- … -->`) from the finished artifact.

Before stopping, confirm that no label or identifier this artifact introduces reuses a label already defined by an approved artifact it references (`prompt-driven-development` Artifact Authority).
