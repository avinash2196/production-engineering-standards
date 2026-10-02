---
description: "Create one detailed human-reviewable Implementation Plan for one approved Plan milestone based on the current repository state."
---

Act as an implementation planner.

Apply `implementation-planning`, `prompt-driven-development`, and relevant domain skills.

Work item: operate only on the work-item folder the user names (`prompt-driven-development` Work-Item Folders). If no work item is named, ask and stop.

This command operates on one milestone already approved in `Plan.md`, identifying its recorded milestone type (FOUNDATION, RED, GREEN, REFACTOR, or OTHER) — it does not decide or change the milestone type. A CONTRACT milestone has no Implementation Plan (its deliverable is the contract artifact); if asked to plan one, stop and say so.

Before planning:

1. read the approved Requirements, Plan, and applicable API/external contract, and confirm the Plan's Status records approval (`prompt-driven-development` Approval Status) — a claim of approval elsewhere is recorded in `Plan.md` first; if none exists, ask and stop;
2. inspect the current repository structure and relevant current implementation;
3. read current Plan execution status;
3a. read every previously approved Implementation Plan and carry its decisions forward as approved inputs (`implementation-planning` Carried-Forward Decisions) — do not reopen them without explicit user approval;
4. verify predecessor milestone evidence and actual completed progress;
5. verify the milestone type being planned matches what `Plan.md` records for this milestone.

Create exactly one:

`docs/.ai/<work-item>/NNN_Implementation_Plan_<Milestone>.md`

The Implementation Plan must reflect the actual current repository state and include:

- authoritative references;
- predecessor evidence;
- current repository state;
- exact files to create or modify;
- ordered proposed changes;
- concrete proposed tests or production code;
- relevant classes, methods, interfaces, signatures, structures, or configuration changes;
- exact code: the complete final content of every file to be created, and for every file to be modified either its complete final content or a complete unified diff covering every changed line with enough context to apply mechanically — never pseudocode, placeholders, ellipses, or partial fragments;
- explicit Acceptance / Completion Criteria for this milestone — what must be true for it to be considered complete;
- verification commands and expected milestone evidence demonstrating those criteria;
- risks and explicit exclusions.

Any expected or predicted milestone evidence stated in the Implementation Plan is a prediction, not proof — label it Expected / Predicted — Not Yet Verified. It becomes verified only when: (1) the milestone has actually been executed; (2) the stated verification commands/checks have actually been run; and (3) the resulting evidence supports the expected outcome. Running a verification command is not sufficient by itself if it fails or produces evidence that contradicts the expected outcome.

The artifact must contain enough proposed implementation detail for human code review before repository changes are applied. Proposed changes must be exact (the specific file and the specific change), not a restated intent such as "implement the feature" or "add test infrastructure."

For a FOUNDATION milestone, create it only if the milestone approved for this Implementation Plan is itself recorded in `Plan.md` as FOUNDATION, and all of these can be answered:

1. Why can the RED milestone(s) this FOUNDATION serves, as recorded in `Plan.md`, not meaningfully proceed from the current repository state?
2. What exact prerequisite must be established?
3. What files/artifacts may change?
4. What target feature behavior is explicitly excluded?
5. How will completion be verified?
6. What evidence will show the repository is ready for every RED milestone this FOUNDATION serves?

Also list, as explicit decisions for review with alternatives, every FOUNDATION choice that binds the RED milestones it serves and that they cannot change themselves (test tooling, test libraries, test clients, test-isolation mechanism).

If the milestone approved for this Implementation Plan is a RED milestone with no preceding FOUNDATION milestone recorded in `Plan.md`, do not create a FOUNDATION Implementation Plan — including whenever the only reason under consideration is that the production class, service, repository, controller, method, or behavior under test does not yet exist; propose RED directly instead.

For RED, propose test/check changes only — or no file changes when `Plan.md` names an existing failing test as the RED evidence (`implementation-planning` RED).
For GREEN, require valid RED evidence and propose the smallest production change required to satisfy it.
For REFACTOR, require a verified GREEN baseline and propose behavior-preserving changes only; for a standalone REFACTOR the baseline is the full verification suite passing on the unmodified repository, and the plan names the existing tests that protect the code being restructured.
For OTHER, confirm `Plan.md` records that no owned requirement changes behavior, record the baseline evidence before any change, name the existing tests that must keep passing, and propose only the approved changes; if a production behavior change turns out to be needed, stop for replanning as RED and GREEN.

Proposed code may be written inside the Implementation Plan for review.

Do not modify production code, tests, build configuration, deployment configuration, or runtime configuration while creating the Implementation Plan.

If the current repository state materially conflicts with approved artifacts or predecessor evidence, or contradicts the milestone type `Plan.md` recorded for this milestone, stop and surface the conflict for human review — do not silently plan a different milestone type.

When the plan introduces or changes a dependency, framework, plugin, or tool version, apply the `implementation-planning` skill's Dependency and Version Selection rules: a currently supported release with a cited source, never one chosen for local-cache or offline convenience; ask and stop if support cannot be verified.

Do not implement the milestone.
Do not approve the Implementation Plan yourself.

Apply the `implementation-planning` skill's Pre-authorized Contingencies (a dedicated section, exact trigger, file, and change only), File Scope and Plan Status, and Repeatable, Isolated Verification rules.

Apply the `implementation-planning` skill's Planning-Time Dry Run and Pre-existing Failures rules: before stopping, report the dry-run result (or why none was run), and surface any failure found on the unmodified baseline as a question for the user instead of deciding how the criteria treat it. Cite evidence for every causal claim in the plan, and label an unestablished explanation as a hypothesis.

Apply the `implementation-planning` skill's Exact Code rules, and before stopping report per file that complete content or a complete diff is present, contains no pseudocode or placeholder, matches the Proposed Changes list, and traces every dependency, plugin, and configuration setting it introduces.

When revising an existing Implementation Plan, treat it as a revision, not a fresh draft: update every reference to each changed item, re-run the affected dry-run checks, and report what changed. Number a new Implementation Plan as the next `NNN` among the files present in this work item's folder.

Remove every template comment (`<!-- … -->`) from the finished artifact.

Before stopping, confirm that no label or identifier this artifact introduces reuses a label already defined by an approved artifact it references (`prompt-driven-development` Artifact Authority).
