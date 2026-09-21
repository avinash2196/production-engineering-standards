---
description: "Create one detailed human-reviewable Implementation Plan for one approved Plan milestone and phase based on the current repository state."
---

Act as an implementation planner and create exactly one detailed Implementation Plan.

Apply `implementation-planning`, `prompt-driven-development`, and relevant domain skills.

This command operates on the milestone and phase already approved in `Plan.md` — it does not decide which phase a milestone needs. Whether FOUNDATION is required is a planning decision recorded in `Plan.md`'s `setup required` field for that milestone.

Before planning:

1. read the approved Requirements, Plan, and applicable API/external contract;
2. inspect the current repository structure and relevant current implementation;
3. read current Plan execution status;
4. verify predecessor evidence and actual completed progress;
5. verify the requested phase matches what `Plan.md` records for this milestone.

Create exactly one: `docs/.ai/NNN_Implementation_Plan_<Milestone>.md`

The Implementation Plan must reflect the actual current repository state and include:

- authoritative references;
- predecessor evidence;
- current repository state;
- exact files to create or modify;
- ordered proposed changes;
- concrete proposed tests or production code;
- relevant classes, methods, interfaces, signatures, structures, or configuration changes;
- code snippets, pseudocode, or patch-level detail where practical and useful for human review;
- explicit Acceptance / Completion Criteria for this phase — what must be true for it to be considered complete;
- verification commands and expected phase evidence demonstrating those criteria;
- risks and explicit exclusions.

The artifact must contain enough proposed implementation detail for human code review before repository changes are applied. Proposed changes must be exact (the specific file and the specific change), not a restated intent such as "implement the feature" or "add test infrastructure."

For FOUNDATION, create it only if `Plan.md` already records this milestone's setup required as Yes, and all of these can be answered:

1. Why can RED not meaningfully proceed from the current repository state?
2. What exact prerequisite must be established?
3. What files/artifacts may change?
4. What target feature behavior is explicitly excluded?
5. How will completion be verified?
6. What evidence will show the repository is ready for RED?

If `Plan.md` records this milestone's setup required as No, do not create a FOUNDATION Implementation Plan — including whenever the only reason under consideration is that the production class, service, repository, controller, method, or behavior under test does not yet exist; propose RED directly instead.

For RED, propose test/check changes only.
For GREEN, require valid RED evidence and propose the smallest production change required to satisfy it.
For REFACTOR, require a verified GREEN baseline and propose behavior-preserving changes only.

Proposed code may be written inside the Implementation Plan for review.

Do not modify production code, tests, build configuration, deployment configuration, or runtime configuration while creating the Implementation Plan.

If the current repository state materially conflicts with approved artifacts or predecessor evidence, or contradicts the phase `Plan.md` selected for this milestone, stop and surface the conflict for human review — do not silently plan a different phase.

Do not implement the milestone.
Do not approve the Implementation Plan yourself.
