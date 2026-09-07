---
description: "Execute an approved GREEN Implementation Plan, verify GREEN, and record verified progress."
argument-hint: "approved GREEN Implementation Plan and valid RED evidence"
agent: "implementation-engineer"
tools:
  - read
  - search
  - edit
  - execute
---
Apply `prompt-driven-development` and relevant stack/domain skills.

Read:

- the authoritative requirements, Plan, and applicable API/external contract;
- the current repository state;
- the approved GREEN Implementation Plan;
- valid predecessor RED evidence.

Implement only the production changes explicitly authorized by the approved GREEN Implementation Plan.

Prefer the smallest production change that satisfies the approved RED evidence.

Do not introduce unrelated refactoring, infrastructure, dependencies, abstractions, or future milestone work.

Run the verification commands required by the approved Implementation Plan.

Confirm that the previously valid RED behavior is now GREEN and that existing relevant tests remain GREEN.

After GREEN is actually verified, update only the corresponding execution/status information in `docs/.ai/Plan.md` with completion and concise actual evidence.

If verification fails, do not mark the milestone or phase complete.

If implementation requires changing approved scope or materially conflicts with an authoritative artifact, stop for replanning and human review.

Report the commands actually executed and the observed evidence.

Do not begin the next milestone.
