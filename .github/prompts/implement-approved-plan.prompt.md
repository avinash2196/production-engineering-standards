---
description: "Execute one approved GREEN or non-behavior milestone Implementation Plan. Does not create RED tests or perform REFACTOR work."
argument-hint: "path to approved GREEN, FOUNDATION, or OTHER Implementation Plan"
agent: "backend-service-engineer"
---

You are the execution phase for one approved non-RED, non-REFACTOR milestone in the Prompt-Driven Development workflow.

## Preconditions

1. Read `docs/.ai/Plan.md`.
2. Read the milestone-specific approved Implementation Plan supplied by the user.
3. Verify the milestone phase is `GREEN`, `FOUNDATION`, or `OTHER`.
4. If the phase is `RED`, stop and use `/generate-tests`.
5. If the phase is `REFACTOR`, stop and use `/refactor-code`.
6. If the artifact is missing, unapproved, materially inconsistent, or mixes multiple phase scopes, stop without changing code and report the gap.
7. For a `GREEN` milestone, verify its predecessor RED milestone is complete and valid RED evidence is recorded. If not, stop.

Reference: [Prompt-Driven Development Workflow](../../standards/prompt-driven-development-workflow.md)

## GREEN Execution

For a `GREEN` milestone:

- Modify only production/configuration files explicitly listed in the approved GREEN Implementation Plan.
- Implement the smallest approved behavior required to satisfy the predecessor RED behavior.
- Do not add new tests except when the approved GREEN plan explicitly requires a test-support correction that does not broaden behavior; otherwise return to planning.
- Do not add unrelated features, speculative abstractions, later-milestone dependencies, or cleanup.
- Run focused tests/checks, then the relevant regression suite.
- Record commands, summarized results, and changed files in the Execution Evidence section without changing approved scope.
- **Stop after GREEN.** Do not refactor. A refactor requires a separate Plan milestone and approved REFACTOR Implementation Plan.

## FOUNDATION / OTHER Execution

For an approved non-behavior milestone:

- Execute only the files and checks listed in that Implementation Plan.
- Do not introduce application behavior or future dependencies merely to prepare for later work.
- Run the approved executable validation.
- Record observed evidence and changed files.

## Final Rules

- Do not claim success when commands were not run or results were not observed.
- Do not advance to another Plan milestone in this invocation.
- Do not treat an end-to-end user request as approval for an unreviewed next milestone.
