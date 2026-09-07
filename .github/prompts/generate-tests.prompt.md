---
description: "Execute an approved RED Implementation Plan, establish valid RED evidence, and record verified RED progress."
argument-hint: "approved RED Implementation Plan"
agent: "test-engineer"
tools:
  - read
  - search
  - edit
  - execute
---
Apply `testing`, `prompt-driven-development`, and relevant domain skills.

Read:

- the authoritative requirements, Plan, and applicable API/external contract;
- the current repository state;
- the approved RED Implementation Plan.

Implement only the test/check changes authorized by the approved RED Implementation Plan.

Do not write production implementation.
Do not weaken, disable, or skip tests merely to manufacture RED.
Do not pull GREEN or future milestone work into RED.

Run the verification commands required by the approved Implementation Plan and establish valid RED evidence.

Confirm that the observed failure demonstrates the intended missing approved behavior rather than an unrelated compilation, configuration, or environment problem.

After valid RED is actually established, update only the corresponding execution/status information in `docs/.ai/Plan.md` with completion and concise actual evidence.

If RED is invalid or verification fails unexpectedly, do not mark the milestone or phase complete.

Report the commands actually executed and the observed evidence.

Do not begin GREEN.
