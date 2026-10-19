# PDD Gap Fixes — October 2026 (batch C)

Status: open, awaiting evidence. Nothing in this brief is fixed yet. It also holds the user's review of the batch-B fixes released in 0.14.0 (see "Review of released batch-B fixes").

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
| G2 (confirmed — see C12) | The contract template covers HTTP APIs only. WebSocket and event contracts would be unstructured. | `api-design/templates/API-Contract.md` has API Capabilities sections only. It has nothing for handshake auth, frame or message format, close codes, backpressure, or event topic, schema, delivery semantics and idempotency key. | Do the WebSocket and `SessionCompleted` contracts get written, and with which of those properties? Is the CONTRACT milestone given every interface, or only the REST ones? | Add a section per interface kind to the template; or add a separate event/stream contract template. |
| G3 | Milestones are split by layer, not by service. Cross-service integration and end-to-end proof have no milestone. | `create-plan.prompt.md` Adaptive Milestone Decomposition gives only the layer example (Persistence, Service, API). | Is the Plan split per service, per layer, or as one huge pair? Is there a milestone that proves the end-to-end flow (session, stream, event, report)? Is the Plan reviewable in size? | A decomposition rule for multi-service work items; a required integration/end-to-end RED/GREEN pair; one work item per service with a parent item. |
| G4 | Verification assumes one build. There is no rule for several services, mixed stacks, or tests that need a broker or containers. | Plan Content Rule 13 records "the" verification commands. Rule 11 says RED cannot add test infrastructure. The CLAUDE.md template lists one command set. | Does the Plan record commands per service and an end-to-end harness? Is a FOUNDATION placed for each service that needs one? Is the broker test setup owned before the RED milestone that needs it? | Rule 13 allows per-component commands with an owner; FOUNDATION guidance for shared test infrastructure. |
| G5 | Product-level requirements are single-repository. When an application is split into one repository per service, PDD can read the product requirements only from a copy in each repository, and a work item in one repository cannot see product statements made out of date by another. | `prompt-driven-development` SKILL "Work-Item Folders" and every command read only `docs/requirements.md` in the same repository; Final Review lists out-of-date product statements, but only the user updates the document, per repository. Checked against `.github/` and `.claude/` text on 2026-10-16. | Partly seen (scribe platform, 2026-10-16): the run needed a manual sync script that copies the product document into each sibling repository with its source commit. Still to observe: does `capture-requirements` or `create-plan` notice a stale copy, and do Final Reviews in different repositories report the same product statement inconsistently? | A documented product-requirements source outside the repository (path or pinned copy with its source version); a staleness check against that source. |
| G6 | No artifact coordinates a capability that spans work items in several repositories (contract first, then providers, then consumers). Ordering and "consumer waits for the published contract" exist only in the human's head. | Every command operates on exactly one work item in one repository; "another work item's artifacts never authorize work in the current one". Nothing names cross-repository dependencies. Checked 2026-10-16. | Partly seen (scribe platform, 2026-10-16): the run created a non-PDD `docs/roadmap.md` in an architecture repository to track the chain. Still to observe: does a consumer's `create-plan` notice that the contract version it needs is not yet approved or published, or does it plan against an assumed contract? | A "Depends On" section in requirements or the Plan naming external work items and contract versions, checked before RED; or a parent work item. Related to G3's "one work item per service with a parent item". |

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
| C8 | Plan revision 3 (same work item, 2026-10-05) | Requirement R17 asks the Final Review to state something (prompt and model effects are confounded). Plan Content Rule 8 allows only three forms for a requirement with no owning milestone: exclusion, not required, and preserved. None fits a requirement the Final Review fulfils. The Plan improvised "none — Final Review obligation" / "Final Review". Acceptance criteria already allow "Final Review inspection", but requirements do not. | Plugin | Add a fourth row form to Rule 8 and the Plan template: a Final Review obligation (Owning "none — Final Review obligation", Verifying "Final Review"). |
| C10 | M4 execution (same work item, 2026-10-07) | The planning dry run sent the step 4 request with a scratch `C:/...` path instead of the plan's `$HOME`-based path. Git Bash's `/c/...` form then broke `curl -F image=@...` at execution, and all four cases failed locally (no cost). The `implementation-planning` dry-run rule already requires running the plan's exact code and commands. | Model | No plugin change. |
| C11 | All gates (`medgemma-xray-demo`, work item `two-pass-experiment`, 0.14.0, 2026-10-08) | Second occurrence of C1. Mid-capture the user said "all steps are approved complete it and let me know once ready for deployment", a blanket approval of artifacts not yet written. The model recorded each Status as "Pre-approved … recorded for review" and executed through GREEN, stopping before the cost-bearing deployment. Also second occurrence of C3: an OTHER validation milestone waiting on an owner-run deployment had no status other than Pending. | Plugin (evidence for C1 and C3) | Same fix as C1; C3 now has two cases (prompt-robustness RM6, two-pass-experiment TM6), so it can leave Watch. |
| C12 | CONTRACT milestone (`scribe-contracts`, work item `protocol-v1`, 0.14.0, 2026-10-18) | Confirms G2. The work item needed a WebSocket client protocol, a gRPC bidirectional stream and a unary gRPC call besides two REST operations. The template's capability fields (Endpoint, HTTP method, success and failure status codes) fit only the two REST operations. The model added its own sections for the WebSocket protocol (handshake and auth timing, message envelope, ack semantics, state machine, ping/pong, close-code table, limits) and for each gRPC interface (methods, stream order, metadata, status codes). Contract Completeness questions 1–9 are HTTP-worded, so their WebSocket and gRPC answers were improvised in Contract-Wide Rules. Also observed: the requirements deferred field-level decisions to the contract, but `create-api-contract` forbids choosing them, so the model asked one round of proposals (9 questions, all accepted) and flagged 7 further details as "Derived for review", which the user confirmed at contract review. That flow worked and needs no fix. Latest `.github/skills/api-design/templates/API-Contract.md` still has only the HTTP capability fields (checked 2026-10-18). | Plugin | Design from this evidence: add per-interface-kind sections to the template (message or stream interface: connection and auth, framing, message catalogue, ordering and ack semantics, state rules, keepalive, close or status codes, limits; RPC interface: methods, stream order, metadata, status codes), and word Completeness questions 1, 7 and 8 so they apply to non-HTTP interfaces. |
| C9 | Before M4 planning (same work item) | The user had switched the deployed model outside PDD (`/health` reported a different model than the repository's setting). It was found only because the assistant compared `/health` with the repository by hand. M4's baseline evidence ("health response showing the model loaded") did not require comparing the deployed configuration with the repository's. | Plugin (Watch — seen once) | For an OTHER milestone that validates a deployment, the baseline evidence could require confirming the deployment matches the repository state being validated. Decide after a second case. |

Run notes for `prompt-quality` (two services, but only the backend changed): one verification command set was enough, so this run neither confirms nor refutes G1–G4.

Run notes for the scribe platform (2026-10-16, Claude Code, 0.14.0; seven services, one repository per service, Java and Python): before any PDD command ran, the architecture was settled in conversation and written into the product-level `docs/requirements.md` (services, data ownership, auth boundaries, queue rules, decision log), because no PDD artifact holds it. This is early evidence for G1's question "where do architecture decisions end up": in the product requirements, outside any reviewed work-item artifact. G5 and G6 were raised by the same run. Work items start in `scribe-contracts` (`protocol-v1`); watch them for G1–G6.

## Review of released batch-B fixes (user review, 2026-10-05)

The user reviewed batch B's gaps after H1–H4 were released in 0.14.0. The verdicts below are the user's, compared with the released text. The follow-ups are candidates for the next release. Nothing is changed yet.

| Batch B item | User verdict | Released 0.14.0 text | Follow-up for the next release |
| --- | --- | --- | --- |
| B1 / H1: contract amendment after milestones ran | Real gap, but the interpretation is wrong. PDD must not reopen or re-run an executed milestone, or renumber history. | Plan Integrity: an unmeetable contract decision uses the Blocked stop, and `create-api-contract` amendment mode is correct. `create-plan` then adds "a new Pending milestone **of the same type** (`<milestone> amendment`)" for each executed milestone the amendment lists. | Keep the Blocked trigger and the Amendments section. Replace the "same type / `<milestone> amendment`" wording: the revision adds a new milestone with its own name, typed by the kind of change it makes (Milestone Types), and never labelled as a continuation of an executed milestone. |
| B2 / H2: operator configuration ownership | Partial gap. Implementation Plans already own concrete configuration decisions (Carried-Forward Decisions), so "no owning artifact" was overstated. The real gap is when operator configuration becomes a stable external contract and stops being an implementation detail. | Rule 2 and `create-api-contract`: "When the requirements require externally settable configuration, define the names and shapes operators set." | The released text matches the narrowed gap, so no text change. Correction to the record: B2's "had no owning artifact" was wrong. In the run, IP 004 decided the names and IP 006 carried them forward. |
| B3 / H3: new tests passing at RED | Not a gap. A RED test must fail for the missing behavior, and a passing test for behavior already delivered is regression or predecessor coverage, not RED evidence. | `implementation-planning` RED allows such tests when an earlier milestone delivers the behavior, and the Implementation Plan template gains `Tests expected to pass at RED`. | Reclassify B3 as **Model**. The root cause was a traceability error: the Plan made the GREEN milestone M6 the owner of the hashed-password requirement although M4 delivered it, which Plan Content Rule 8 already covers. Decide whether to withdraw H3's allowance and the template field. **Interaction:** C2 builds on H3's allowance (extending it to preserved behavior), so if H3 is withdrawn, re-assess C2 on its own terms: tests for preserved behavior that the Plan explicitly assigns to a RED milestone. |
| B4 / H4: security and identity comparison | Real gap, narrowly scoped: identity comparison and canonicalization are under-specified. | `security` skill line on canonical identity comparison, plus a `create-implementation-plan` rule to apply `security` and list every identity, role or ownership comparison in Risks. | Keep the `security` line. Consider removing the planning trigger: security already routes at review time (`code-reviewer`, `production-readiness-reviewer`), and that is how the defect was found. |
| B5: missing application instruction file | Not a core PDD gap. This is bootstrap or orchestration, and `setup-claude-instructions` already says "Run first". Coupling requirements capture to setup is unnecessary. | Not changed (it was a Watch item). | Closed with no plugin change. Moved to "Keep out of the plugin". |

### Late model findings from the batch-B evidence (no plugin change)

| ID | Finding | Existing rule |
| --- | --- | --- |
| C6 | In approval-service `initial-build`, the model appended amendment text to an **executed** milestone's Execution Status row (M5) and titled the amendment Implementation Plan as part of that milestone. | Plan Integrity: "Do not rewrite the Plan to match implementation"; update only execution/status after verification; scope or milestone changes need replanning. |
| C7 | In the same run, the Plan assigned the hashed-password requirement to the M6 GREEN milestone although M4 delivered it, so its M5 RED test passed at RED (the evidence behind B3). | Plan Content Rule 8: single ownership; the owning milestone delivers the requirement. |

## Rules for this batch

The rules are the same as in batches A and B:

- Fixes must be project-neutral.
- Only plugin gaps get a fix. A finding where the model broke a rule the plugin already states clearly is listed under "No plugin change".
- Prefer structure over prose.
- Use the smallest wording that works.
- Check every gap against the latest `.github/` text before logging it.

## Keep out of the plugin

- **B5 (closed by user review, 2026-10-05):** do not make PDD commands check for or require the application instruction file. That is bootstrap; `setup-claude-instructions` / `setup-copilot-instructions` already say "Run first".

These are evidence only, never skill text: the service names, the speech or LLM provider, the broker product, WebSocket libraries, and any audio format.
