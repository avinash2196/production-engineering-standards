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

Before marking REFACTOR complete, verify every approved REFACTOR Acceptance / Completion Criterion using the approved verification commands and evidence — do not invent, weaken, reinterpret, or modify the criteria during execution. Confirm the existing GREEN baseline remains passing and observable behavior is preserved.

After successful verification, update only the corresponding execution/status information in `docs/.ai/Plan.md`, recording the REFACTOR milestone as completed with concise actual evidence.

If behavior changes or verification fails, do not mark the REFACTOR milestone complete. Stop for replanning when required.

Report the commands actually executed and the observed evidence.

If the approved Implementation Plan lists Pre-authorized Contingencies, apply one only when its exact trigger actually occurs, and report for each contingency whether its trigger occurred and whether it was applied. Any other deviation — including a change to the approach — stops execution for re-approval. When the Implementation Plan requires a repeat run of the verification commands without cleaning, perform it and report both runs; a pass that is not repeatable is not verified.

Apply the code exactly as the approved Implementation Plan writes it. Any difference between the resulting files and the plan's exact code — including formatting-independent structural changes — is a deviation: stop and report it for re-approval rather than applying it.

Never remove, loosen, or weaken a test assertion or an Acceptance / Completion Criterion to make verification pass, even under a pre-authorized contingency; a failing check stops execution for re-approval.
