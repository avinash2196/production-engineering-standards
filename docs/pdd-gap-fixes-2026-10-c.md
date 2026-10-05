# PDD Gap Fixes — October 2026 (batch C)

Status: open, awaiting evidence. Nothing in this brief is fixed yet.

`docs/pdd-gap-fixes-2026-10-b.md` is closed (released in 0.14.0). This brief starts the next batch.

## Why this brief is different

Batches A and B logged gaps that a real run had shown. The gaps G1–G4 below are **predictions**. They come from reading the plugin text (0.14.0) against a planned multi-service application. No run has shown them yet.

The batch rules accept only gaps backed by evidence. So each prediction stays in the Predicted Gaps table until the next run confirms or refutes it:

- **Confirmed:** the run hit the gap. Move it to the Findings Log with the run's evidence, then design a fix from what the run showed. Do not design the fix from the prediction.
- **Refuted:** the existing skills handled it. Record how, and close it with no plugin change.
- **Model:** the plugin already states the rule and the model broke it. List it under "No plugin change".

Do not fix G1–G4 before the run. The point of the run is to learn whether the current plugin copes, and which fix shape fits.

## Planned evidence run

| Item | Value |
| --- | --- |
| Application | `speaker-insights` (a new application folder) |
| Executor | Claude Code, planning with Opus |
| Plugin | 0.14.0 |
| Business goal | Record audio from the frontend, analyse it for speakers, and produce a concise report. |
| Stated constraint | The system is split into separate services: orchestration/session, auth, streaming (WebSocket), AI gateway, and a background report worker that consumes a completion event. This must be stated as an approved constraint. Otherwise the `architecture-design` skill rightly weighs a modular monolith, and recommending one would be correct, not a gap. |
| Deliberately thin input | Say "speaker identification". Do not say "diarization". Do not state real-time vs after-recording, token issuer, broker, data ownership, or how the report is delivered. |
| Sequence | Setup instructions, `capture-requirements`, `review-requirements`, `create-plan`. Stop at Plan review. |
| After the fixes | Re-run `create-plan` from the same approved requirements on the fixed release and compare the two Plans. |

## Predicted Gaps (need evidence from the run)

| ID | Prediction | Plugin evidence (0.14.0) | What to observe in the run | Candidate fix shapes (choose only after evidence) |
| --- | --- | --- | --- | --- |
| G1 | No command or artifact establishes the architecture before `Plan.md`. Service boundaries, data ownership, sync/async boundaries, the broker and auth boundaries have no reviewed home. | `architecture-design` is a short consideration list. `review-architecture` reviews an existing design but nothing creates one. Plan Content Rule 3 forbids internal design and library names in the Plan. | Where do architecture decisions end up: nowhere, in the requirements, smuggled into the Plan (breaking Rule 3), or as clarification questions? Does anything get human review before milestones are decomposed? | A `create-architecture` command and `Architecture.md` reviewed before the Plan; a required Architecture section in the requirements; an ARCHITECTURE milestone type like CONTRACT. |
| G2 | The contract template covers HTTP APIs only. WebSocket and event contracts would be unstructured. | `api-design/templates/API-Contract.md` has API Capabilities sections only. It has nothing for handshake auth, frame or message format, close codes, backpressure, or event topic, schema, delivery semantics and idempotency key. | Do the WebSocket and `SessionCompleted` contracts get written, and with which of those properties? Is the CONTRACT milestone given every interface, or only the REST ones? | Add a section per interface kind to the template; or add a separate event/stream contract template. |
| G3 | Milestones are split by layer, not by service. Cross-service integration and end-to-end proof have no milestone. | `create-plan.prompt.md` Adaptive Milestone Decomposition gives only the layer example (Persistence, Service, API). | Is the Plan split per service, per layer, or as one huge pair? Is there a milestone that proves the end-to-end flow (session, stream, event, report)? Is the Plan reviewable in size? | A decomposition rule for multi-service work items; a required integration/end-to-end RED/GREEN pair; one work item per service with a parent item. |
| G4 | Verification assumes one build. There is no rule for several services, mixed stacks, or tests that need a broker or containers. | Plan Content Rule 13 records "the" verification commands. Rule 11 says RED cannot add test infrastructure. The CLAUDE.md template lists one command set. | Does the Plan record commands per service and an end-to-end harness? Is a FOUNDATION placed for each service that needs one? Is the broker test setup owned before the RED milestone that needs it? | Rule 13 allows per-component commands with an owner; FOUNDATION guidance for shared test infrastructure. |

## Answer key for the run

Write down in advance which questions and boundaries the run should raise. Grade each step against this list. A question the plugin asks counts as a pass. A silent choice counts as a finding.

**Requirements (`capture-requirements` and `review-requirements` should ask):**

1. Speaker identification or diarization? Identification needs enrolled voice profiles and is biometric data. The expected answer is "diarization first, identification later".
2. Real-time analysis with a live transcript, or analysis after the recording ends?
3. Is raw audio retained? What does retention cost for recovery and privacy?
4. How is the report delivered: by polling the orchestration status, or by push?
5. What happens to a session that is abandoned (the WebSocket drops without a completion)?
6. Which AI provider handles speech and diarization, which handles the summary, and how is report quality evaluated? (`llm-engineering`)
7. Which stack for each service?

**Architecture (wherever the run puts it):**

8. The orchestration service returns a session ID, a stream URL and a short-lived token. It never holds the WebSocket.
9. Who issues the streaming token, and how does the streaming service validate it without calling back?
10. Does orchestration validate every request through the auth service, or do services validate signed tokens locally?
11. Data ownership: who owns session status, the transcript and speaker segments, and the report? Orchestration must not read the worker's store directly.
12. How is session status updated when the stream completes, and when the report is ready (an event back, or a query)?
13. Does `SessionCompleted` carry a reference or the payload? Where does the worker get the transcript?
14. Delivery semantics: duplicate events, an idempotent worker keyed by session, retries, and a dead-letter path. (`distributed-systems`)
15. The background worker handles business events only. Logs, metrics and traces belong to observability.
16. The AI gateway holds the provider credentials. A fake provider is used for deterministic tests.

**Plan:**

17. Milestones are reviewable per service, and one milestone proves the flow end to end.
18. Every RED milestone that needs a broker or a container has a predecessor that provides it.

## Findings Log

Each row gets an ID (C1, C2, …), the phase, the finding, its kind (Plugin or Model), and the fix.

| ID | Phase | Finding | Kind | Fix |
| --- | --- | --- | --- | --- |
| C1 | All approval gates (`medgemma-xray-demo`, work item `prompt-quality`, 0.14.0, 2026-10-05) | The user said "approve changes on my behalf". The plugin has no form for this: Approval Status says only the user approves, and `capture-requirements` says never to answer an operational characteristic yourself. The run improvised `Approved by Claude on behalf of <user> (delegated approval)` in every Status, and recorded Q9–Q11 as "Delegated" in the Clarification Log. | Plugin | Decide one rule: either delegation is not accepted (ask and stop), or there is a recorded delegated form that lists every delegated decision for the user to review at Final Review. |
| C2 | RED planning (same run) | Plan traceability allows a "none — preserved" row whose verifying milestone is the one whose tests cover it, and the Plan gave the RED milestone tests for preserved behavior (R15). But `implementation-planning` RED allows a test that passes at RED only when an earlier milestone of the work item delivers its behavior. Four preserved-behavior tests passed at RED with no rule covering them. | Plugin | In RED, allow tests for preserved behavior that the Plan assigns to this RED milestone; list them in Expected Evidence as preserved, not RED evidence. |
| C3 | Plan, OTHER milestone (same run) | The requirements need a manual four-case check on the deployed GPU model with owner-supplied images. OTHER was the only fit, but its Implementation Plan needs exact code and baseline evidence. There is also no status for a milestone waiting on external inputs (`Blocked` is for blockers that invalidate the Plan). | Plugin (Watch — seen once) | Let OTHER cover a human-run validation protocol in place of exact code, or add a "waiting on input" status. Decide after a second case. |
| C4 | `capture-requirements` (same run) | AC4 was written stricter than the brief ("no spine or cervical content in other report types" versus brief AC-5 "must not introduce cervical-spine-specific behavior"). That would have removed existing Nasopharynx guidance. It was caught while planning RED and revised (Q11). The "Preserve the user's meaning" rule already covers this. | Model | No plugin change. |
| C5 | Planning-time dry run (same run) | The first dry-run attempt failed on a Windows path conversion and created a gitignored `.venv/` in the repository root; it was removed. The "never modify the repository during a dry run" rule already covers this. | Model | No plugin change. |

Run notes for `prompt-quality` (two services, but only the backend changed): one verification command set was enough, so this run neither confirms nor refutes G1–G4.

## Watch (carried from batch B)

- **B5:** a new application folder with no application instruction file. `capture-requirements` could mention that `setup-claude-instructions` / `setup-copilot-instructions` has not been run. Seen once. The planned run runs setup first, so it will not test this.

## Rules for this batch

The rules are the same as in batches A and B:

- Fixes must be project-neutral.
- Only plugin gaps get a fix. A finding where the model broke a rule the plugin already states clearly is listed under "No plugin change".
- Prefer structure over prose.
- Use the smallest wording that works.
- Check every gap against the latest `.github/` text before logging it.

## Keep out of the plugin

These are evidence only, never skill text: the service names, the speech or LLM provider, the broker product, WebSocket libraries, and any audio format.
