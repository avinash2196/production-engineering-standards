---
description: "Perform an approved behavior-preserving REFACTOR milestone from a verified GREEN baseline and record verified progress."
argument-hint: "approved REFACTOR Implementation Plan"
agent: "refactoring-engineer"
tools:
  - read
  - search
  - edit
  - execute
---
Apply `prompt-driven-development` and relevant engineering/domain skills.

Read:

- the authoritative artifacts;
- the current repository state;
- the approved REFACTOR Implementation Plan;
- verified GREEN baseline evidence.

Perform only the behavior-preserving changes authorized by the approved REFACTOR Implementation Plan.

Do not add features, expand contracts, or pull future milestone work into the refactor.

Run the approved verification commands and confirm the system remains GREEN.

After successful verification, update only the corresponding execution/status information in `docs/.ai/Plan.md` with completion and concise actual evidence.

If behavior changes or verification fails, do not mark the REFACTOR phase complete. Stop for replanning when required.

Report the commands actually executed and the observed evidence.
