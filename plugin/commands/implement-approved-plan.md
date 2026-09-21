---
description: "Execute an approved GREEN Implementation Plan, verify GREEN, and record verified progress."
---

Act as an implementation engineer and implement only the production changes explicitly authorized by the approved GREEN Implementation Plan.

Apply `prompt-driven-development` and relevant stack/domain skills.

Read:

- the authoritative requirements, Plan, and applicable API/external contract;
- the current repository state;
- the approved GREEN Implementation Plan;
- valid predecessor RED evidence.

Prefer the smallest production change that satisfies the approved RED evidence.

Do not introduce unrelated refactoring, infrastructure, dependencies, abstractions, or future milestone work.

Run the verification commands required by the approved Implementation Plan.

Confirm that the previously valid RED behavior is now GREEN and that existing relevant tests remain GREEN.

After GREEN is actually verified, update only the corresponding execution/status information in `docs/.ai/Plan.md` with completion and concise actual evidence.

If verification fails, do not mark the milestone or phase complete.

If implementation requires changing approved scope or materially conflicts with an authoritative artifact, stop for replanning and human review.

Before reporting completion, diff the actual repository changes against the approved Implementation Plan. Every production-code, test, configuration, dependency, schema, migration, or runtime change must map to an explicitly authorized change in the Implementation Plan — do not silently include additional validation, fields, checks, or behavior noticed while implementing, even if it looks like an obvious related fix; surface it as a finding for a separate Implementation Plan instead. Workflow bookkeeping explicitly authorized by the PDD process, such as updating `docs/.ai/Plan.md`'s execution status/evidence after successful verification, is exempt from this comparison.

Report the commands actually executed and the observed evidence.

Do not begin the next milestone.
