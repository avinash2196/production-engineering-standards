---
description: "Create one detailed human-reviewable Implementation Plan for one approved Plan milestone and phase based on the current repository state."
argument-hint: "approved milestone and phase"
agent: "planner"
tools:
  - read
  - search
  - edit
---
Apply `implementation-planning`, `prompt-driven-development`, and relevant domain skills.

Before planning:

1. read the approved Requirements, Plan, and applicable API/external contract;
2. inspect the current repository structure and relevant current implementation;
3. read current Plan execution status;
4. verify predecessor evidence and actual completed progress.

Create exactly one:

`docs/.ai/NNN_Implementation_Plan_<Milestone>.md`

The Implementation Plan must reflect the actual current repository state and include:

- authoritative references;
- predecessor evidence;
- current repository state;
- exact files to create or modify;
- ordered proposed changes;
- concrete proposed tests or production code;
- relevant classes, methods, interfaces, signatures, structures, or configuration changes;
- code snippets, pseudocode, or patch-level detail where practical and useful for human review;
- verification commands and expected phase evidence;
- risks and explicit exclusions.

The artifact must contain enough proposed implementation detail for human code review before repository changes are applied.

For RED, propose test/check changes only.
For GREEN, require valid RED evidence and propose the smallest production change required to satisfy it.
For REFACTOR, require a verified GREEN baseline and propose behavior-preserving changes only.

Proposed code may be written inside the Implementation Plan for review.

Do not modify production code, tests, build configuration, deployment configuration, or runtime configuration while creating the Implementation Plan.

If the current repository state materially conflicts with approved artifacts or predecessor evidence, stop and surface the conflict for human review.

Do not implement the milestone.
Do not approve the Implementation Plan yourself.
