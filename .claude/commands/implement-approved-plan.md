---
description: "Execute an approved FOUNDATION or GREEN Implementation Plan, verify it, and record verified progress."
---

Act as an implementation engineer and execute only the approved Implementation Plan (FOUNDATION or GREEN).

Apply `prompt-driven-development` and relevant stack/domain skills.

Read:

- the authoritative requirements, Plan, and applicable API/external contract;
- the current repository state;
- the approved Implementation Plan (FOUNDATION or GREEN).

First read which milestone type the approved Implementation Plan declares (FOUNDATION or GREEN), and follow only that branch. Do not decide the milestone type yourself — it was already decided in `Plan.md` and fixed by the approved Implementation Plan. Do not treat a GREEN Implementation Plan as needing FOUNDATION first, and do not decide mid-execution that setup is needed; if that turns out to be true, stop (see below) rather than acting on it.

**If the approved Implementation Plan is FOUNDATION:**

- execute only the approved prerequisite changes explicitly listed in the Implementation Plan;
- do not implement target feature/business behavior — that is RED's and GREEN's job, not FOUNDATION's;
- do not create speculative production scaffolding for behavior no RED has driven yet;
- before marking FOUNDATION complete, verify every approved FOUNDATION Acceptance / Completion Criterion using the approved verification commands and confirm the evidence demonstrates the prerequisite is established (RED can now meaningfully begin) — do not invent, weaken, reinterpret, or modify the criteria during execution;
- update only the corresponding execution/status information in `docs/.ai/Plan.md`, recording the FOUNDATION milestone as completed with concise actual evidence;
- stop. Do not begin RED. A FOUNDATION execution never flows automatically into RED — RED still requires its own RED Implementation Plan and human approval.

**If the approved Implementation Plan is GREEN**, also read valid predecessor RED evidence, then:

- implement only the production changes explicitly authorized by the approved GREEN Implementation Plan;
- prefer the smallest production change that satisfies the approved RED evidence;
- do not introduce unrelated refactoring, infrastructure, dependencies, abstractions, or future milestone work;
- before marking GREEN complete, verify every approved GREEN Acceptance / Completion Criterion using the approved verification commands and evidence — do not invent, weaken, reinterpret, or modify the criteria during execution;
- confirm that the previously valid RED behavior is now GREEN, that existing relevant tests remain GREEN, and that no unapproved changes were introduced;
- after GREEN is actually verified, update only the corresponding execution/status information in `docs/.ai/Plan.md`, recording the GREEN milestone as completed with concise actual evidence.

For either milestone type: if verification fails, do not mark that milestone complete.

If implementation requires changing approved scope or materially conflicts with an authoritative artifact, stop for replanning and human review. This includes: discovering during execution that an additional, unapproved prerequisite (dependency, configuration, or other change) is needed — do not add it automatically; stop and report it to planning. It also includes discovering that an approved Acceptance/Completion Criterion cannot be satisfied without work outside the approved Implementation Plan — do not change the criterion or broaden the implementation to cover it; stop and report the unmet criterion and the required unapproved work to planning.

Do not decide whether FOUNDATION is required, add prerequisites on your own judgment, redesign the approved changes, change which files are in scope, or include an "obviously related" fix that was not explicitly authorized. If additional work seems needed, stop and report it rather than performing it.

Before reporting completion, diff the actual repository changes against the approved Implementation Plan. Every production-code, test, configuration, dependency, schema, migration, or runtime change must map to an explicitly authorized change in the Implementation Plan — do not silently include additional validation, fields, checks, or behavior noticed while implementing, even if it looks like an obvious related fix; surface it as a finding for a separate Implementation Plan instead. Workflow bookkeeping explicitly authorized by the PDD process, such as updating `docs/.ai/Plan.md`'s execution status/evidence after successful verification, is exempt from this comparison.

Report the commands actually executed and the observed evidence.

Do not begin the next milestone.
