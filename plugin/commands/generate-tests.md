---
description: "Execute an approved RED Implementation Plan, establish valid RED evidence, and record verified RED progress."
---

Act as a test engineer and implement only the test/check changes authorized by the approved RED Implementation Plan.

Apply `testing`, `prompt-driven-development`, and relevant domain skills.

Read:

- the authoritative requirements, Plan, and applicable API/external contract;
- the current repository state;
- the approved RED Implementation Plan.

Do not write production implementation.
Do not weaken, disable, or skip tests merely to manufacture RED.
Do not pull GREEN or future milestone work into RED.

In statically typed languages, a compilation failure is valid RED evidence when it is directly caused by an intentionally absent production type, method, or signature required by the approved behavior (e.g. a test referencing `UserService` failing to compile because `UserService` does not exist yet). Do not create production-source scaffolding merely to make tests compile.

Run the verification commands required by the approved Implementation Plan and establish valid RED evidence.

Confirm that the observed failure demonstrates the intended missing approved behavior rather than an unrelated compilation, configuration, or environment problem.

After valid RED is actually established, update only the corresponding execution/status information in `docs/.ai/Plan.md` with completion and concise actual evidence.

If RED is invalid or verification fails unexpectedly, do not mark the milestone or phase complete.

Before reporting completion, re-read every test/check assertion you wrote or changed and confirm each one still asserts the actual approved behavior (not the current unimplemented state) — a test that asserts acceptance of input the approved artifacts require to be rejected, or that stops asserting the required exception/value, is not valid RED evidence even if it fails for an unrelated reason.

Report the commands actually executed and the observed evidence.

Do not begin GREEN.
