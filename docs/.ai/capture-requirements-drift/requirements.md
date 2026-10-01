# Requirements — capture-requirements-drift

## Context

A PDD test run of the plugin's `capture-requirements` workflow on GitHub Copilot CLI (against `order-management-service`, change request "Restore Order Management Service Test Suite") produced `docs/.ai/test-suite-stabilization/requirements.md`. The user's verdict on that artifact: **Requirements gate: NOT READY FOR APPROVAL.**

What the run did correctly (to be preserved): it created the correct work-item artifact, kept `docs/requirements.md` read-only, preserved the core defect-fix requirements, and stopped before Plan/code changes.

What it did wrong: `capture-requirements` is supposed to capture only user-provided requirements or confirmed repository evidence, but it converted engineering recommendations and likely assumptions into requirements, weakened one user requirement, and mixed later-phase content into the requirements artifact.

## Requirements

### CR-1 — Capture only user-provided requirements or confirmed repository evidence

`capture-requirements` must not add to the requirements artifact anything that was neither provided by the user nor confirmed by repository evidence. The observed inventions that must not recur are:

1. build/test commands (e.g. `mvn test`, `mvn -Dtest=<Test>#<method> test`);
2. language/runtime versions (e.g. Java/JVM 17);
3. CI reproducibility as a requirement;
4. a specific worktree or branch;
5. mandatory observability/logging requirements;
6. mandatory flakiness handling;
7. rollback considerations;
8. extra documentation requirements;
9. solution-shape constraints the user did not state (e.g. "single minimal corrective action");
10. assumptions about external services.

### CR-2 — Establish facts by inspection, not by assertion

Items that may later turn out to be true repository facts must be established by inspecting the repository, not manufactured during requirements capture.

### CR-3 — Inspect before asking

Clarification questions must not be asked about matters the repository has not yet been inspected for. (Observed: blocking questions about Maven profiles and external services were asked before the repository was inspected.)

### CR-4 — Preserve the meaning of user requirements

Captured requirements must not replace a user requirement with a non-equivalent statement. Observed: the user's "preserve approved behavior" was captured as "No behavioral changes to other passing tests are required to fix the failing test." These are not equivalent — a legitimate root-cause fix may touch behavior exercised by other tests while keeping those tests green.

### CR-5 — Keep later-phase content out of the requirements artifact

The requirements artifact must not contain content that belongs primarily to planning, the Implementation Plan, or verification evidence — exact commands, branch/worktree, stack traces, evidence snapshots, rollback strategy — unless the user explicitly requires it.

### CR-6 — Both platforms

The fix applies to the plugin for both GitHub Copilot and Claude Code. (User decision: "fix both in plugin"; the drift was observed on Copilot, and the user expects the same behavior from Claude.)

## Acceptance Criteria

- AC-1: Re-running `capture-requirements` on the same change request on **Copilot** produces a requirements artifact that contains none of the CR-1 items unless they come from the user or repository inspection, satisfies CR-3 through CR-5, and keeps the correct behaviors listed in Context.
- AC-2: The same re-run on **Claude Code** meets AC-1.

## Repository-Confirmed Facts

- The Copilot prompt `.github/prompts/capture-requirements.prompt.md` and the Claude command `.claude/commands/capture-requirements.md` have identical instruction bodies. `.github/skills/` and `.claude/skills/` have identical content, and the validator enforces the mirror. The drift therefore comes from shared instruction text, not from a difference between platforms.
- The command instructs: "apply the `requirements-analysis` Operational Characteristics check and record every answer". `requirements-analysis` § Operational Characteristics tells the agent to *ask* about six characteristics (scale, deployment, availability/latency, consistency/concurrency, dependency failure, observability). The Copilot artifact instead answered a self-made 14-item checklist itself. That checklist is the source of CR-1 items 5–8 (observability, flakiness, rollback, documentation).
- The "no invented scope" rule (`prompt-driven-development` Plan rule 9) applies to the Plan; `requirements-analysis` states "Do not promote framework defaults, industry conventions, repository conventions, or personal preference into requirements" but has no rule for CR-3, CR-4, or CR-5.
- Claude Code check (2026-09-30, one headless run of `/production-engineering-standards:capture-requirements` on a scratch copy of the `copilot-order-test-fix` worktree with the same change request): the drift was **not** reproduced. The run inspected the repository first, created no artifact, and stopped with three repository-grounded blocking questions. One run does not show that Claude is immune; the shared instruction gaps above still apply.
- Observation from that run (not yet a requirement): the change request says "93 of 94 tests pass", but both `order-management-service` and the `copilot-order-test-fix` worktree contain 15 `@Test` methods. The Copilot artifact accepted the premise without checking it; Claude flagged the conflict.

## Operational Characteristics

Repository evidence: this work item changes plugin instruction text (skills, prompts, commands, agents) and no running system, so none of the six characteristics can be changed by it. Recorded as exclusions, pending the user's confirmation at requirements review.

- Scale: not required for this work item.
- Deployment: not required for this work item.
- Availability and latency: not required for this work item.
- Consistency and concurrency: not required for this work item.
- Dependency failure: not required for this work item.
- Observability: not required for this work item.
