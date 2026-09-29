---
description: "Execute an approved RED Implementation Plan, establish valid RED evidence, and record verified RED progress."
argument-hint: "work item; approved RED Implementation Plan"
agent: "test-engineer"
tools:
  - read
  - search
  - edit
  - execute
---
Apply `testing`, `prompt-driven-development`, and relevant domain skills.

Work item: operate only on the work-item folder the user names (`prompt-driven-development` Work-Item Folders). If no work item is named, ask and stop.

Before changing any file, confirm the Implementation Plan is approved and record that approval in its Human Review status (`prompt-driven-development` Approval Status). If no approval exists, ask and stop. After verified execution, update that same status.

Read:

- the authoritative requirements, Plan, and applicable API/external contract;
- the current repository state;
- the approved RED Implementation Plan.

Implement only the test/check changes authorized by the approved RED Implementation Plan.

Do not write production implementation.
Do not weaken, disable, or skip tests merely to manufacture RED.
Do not pull GREEN or future milestone work into RED.

In statically typed languages, a compilation failure is valid RED evidence when it is directly caused by an intentionally absent production type, method, or signature required by the approved behavior (e.g. a test referencing `UserService` failing to compile because `UserService` does not exist yet). Do not create production-source scaffolding merely to make tests compile.

Run the verification commands required by the approved Implementation Plan and establish valid RED evidence.

Before marking RED complete, verify every approved RED Acceptance / Completion Criterion using the approved verification commands and evidence — do not invent, weaken, reinterpret, or modify the criteria during execution. If an approved criterion cannot be satisfied without work outside the approved Implementation Plan, stop and report it to planning rather than changing the criterion.

Confirm that the observed failure demonstrates the intended missing approved behavior rather than an unrelated compilation, configuration, or environment problem.

After valid RED is actually established, update only the corresponding execution/status information in `docs/.ai/<work-item>/Plan.md`, recording the RED milestone as completed with concise actual evidence.

If RED is invalid or verification fails unexpectedly, do not mark the RED milestone complete.

Completing the RED milestone does not complete or authorize GREEN. GREEN is a separate milestone that still requires its own approved Implementation Plan and Human Review.

Before reporting completion, re-read every test/check assertion you wrote or changed and confirm each one still asserts the actual approved behavior (not the current unimplemented state) — a test that asserts acceptance of input the approved artifacts require to be rejected, or that stops asserting the required exception/value, is not valid RED evidence even if it fails for an unrelated reason. Also confirm that no test asserting only that something does not happen passes vacuously in RED — each such test must first exercise the positive case in the same test.

Report the commands actually executed and the observed evidence.

Do not begin GREEN.

If the approved Implementation Plan lists Pre-authorized Contingencies, apply one only when its exact trigger actually occurs, and report for each contingency whether its trigger occurred and whether it was applied. Any other deviation — including a change to the approach — stops execution for re-approval. When the Implementation Plan requires a repeat run of the verification commands without cleaning, perform it and report both runs; a pass that is not repeatable is not verified. A verification failure that the approved Implementation Plan does not name as a known pre-existing failure stops execution; never rerun verification until it happens to pass.

Apply the code exactly as the approved Implementation Plan writes it. Any difference between the resulting files and the plan's exact code — including formatting-independent structural changes — is a deviation: stop and report it for re-approval rather than applying it.

Never remove, loosen, or weaken a test assertion or an Acceptance / Completion Criterion to make verification pass, even under a pre-authorized contingency; a failing check stops execution for re-approval.
