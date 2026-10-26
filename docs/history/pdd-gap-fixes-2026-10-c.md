# PDD Gap Fixes — October 2026 (batch C)

Status: D1–D7 applied in 0.15.0 (branch `release/0.15.0`), awaiting a trial run before release. G1 and G3–G6 remain predictions; C9 remains on Watch. It also holds the user's review of the batch-B fixes released in 0.14.0 (see "Review of released batch-B fixes").

`docs/history/pdd-gap-fixes-2026-10-b.md` is closed (released in 0.14.0). This brief starts the next batch.

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
| C13 | All phases, Claude Code (user observation across the medgemma, scribe-contracts and approval-service runs, 0.14.0, 2026-10-19) | The artifacts are designed for a cold start: each command reads requirements, Plan, contract, Implementation Plan, and the repository. Yet every Claude Code command runs inside the user's main conversation, so whole work items ran in one growing context. Two effects follow. Quality and cost degrade as the context grows. The hand-off the artifacts exist to guarantee is never tested: the model can rely on conversation memory, so a gap in a Plan or Implementation Plan goes unnoticed. Repository evidence (checked 2026-10-19): none of the 14 `.claude/commands/*.md` files sets `context` or `agent`; they say "Act as an implementation engineer" and so on, and the role agents in `.claude/agents/` are never used by a command. The 14 `.github/prompts/*.prompt.md` files name an `agent:`. **Copilot CLI probe (1.0.98, 2026-10-19):** a throwaway plugin first told the session a codeword, then ran a prompt file. A prompt file with `agent: "probe-agent"` ran inline as a skill and reported the codeword, the same as a prompt file with no `agent:`. So `agent:` does not give a fresh context in Copilot CLI. A prompt file that tells the model to delegate to the custom agent as a subagent, passing only the instruction, made the subagent report `CODEWORD=NONE`. That is a fresh context, but the main model writes the subagent's prompt, so it could still pass conversation content on. **Claude Code probe (2.1.277, 2026-10-19):** run in the same continued session after the codeword. A command with no `context` reported `CODEWORD=PELICAN-42`. A command with `context: fork`, `agent: probe-agent` and `background: false` reported `CODEWORD=NONE`, and the main session waited for the result. So `context: fork` gives a fresh context. The PDD skill Approval Status accepts approval "given by the user in the current conversation", which a fresh context cannot see. Claude Code command files support `context: fork` with `agent: <subagent>`: a new subagent with no conversation history, given the command text as its prompt (`background: false` waits for the result). | Plugin | Run every artifact-driven Claude command as a forked subagent: `create-plan`, `create-api-contract` and `create-implementation-plan` with `planner`; `generate-tests` with `test-engineer`; `implement-approved-plan` with `implementation-engineer`; `refactor-code` with `refactoring-engineer`; `review-code`, `review-production-readiness` and `review-architecture` with the matching reviewer. Keep `capture-requirements` and `review-requirements` in the main conversation, because they need back-and-forth with the user. A forked command that needs clarification ends and returns its questions ("ask and stop" already). **Linked to C1:** fix them together. A forked command can rely only on approval recorded in the artifact, so approval given in conversation must be written into the artifact (by the main conversation, at the user's word) before the forked command runs. Copilot needs a different mechanism (see the probe): the prompt body delegates to the role agent as a subagent and passes only the work item and the command's instruction. Supports the external loop decision (each loop step is then already a fresh, self-contained run). |
| C14 | create-api-contract, 0.15.0 trial (`workspace-reservation-service`, work item `recent-reservations`, Claude Code 2.1.277 headless with `--plugin-dir`, 2026-10-20 to 10-24) | The forked `planner` decided all eight decisions the requirements deferred to the contract (path, parameters, body including a new `createdAt` field, empty result, ordering) and asked nothing. `create-api-contract.md:38` says to ask and stop "instead of choosing" for anything the sources do not answer, but `create-plan` makes the CONTRACT milestone own "every decision the requirements defer to the contract", and the contract did not mark the choices as proposals. The user accepted them at review. Same tension as C12, where the model asked first. | Plugin | Make the two rules agree: deferred decisions are proposed in the contract, labelled as proposals for the user to accept at contract review, or are asked before writing. |
| C15 | Copilot CLI 1.0.98, create-plan (same trial, throwaway clone, default model claude-haiku-4.5) | The real prompt (with `tools:` read, search, edit) did delegate via `task` to `production-engineering-standards:planner`; the session codeword did not leak. But before delegating, the main model read the requirements and repository itself and passed its own 2.7k-character summary plus one line ("Apply requirements-analysis and prompt-driven-development to create Plan.md") instead of the command text. The subagent returned the Plan as text, and the main model wrote `Plan.md` and summarized the report instead of relaying it unchanged. The subagent never saw the command's Plan rules or self-checks; the Plan proposed a default route although the external shape was deferred to the contract. C13 predicted this risk. | Model (instruction is explicit), with Plugin exposure | Consider stronger wording ("pass this file's text verbatim; do not read artifacts before delegating; the subagent writes the artifact") and a retest with a stronger model. |
| C16 | create-plan fork (same trial) | The first forked `create-plan` stalled after a tool result (the subagent transcript stopped and the parent emitted heartbeats for about two days, probably across machine sleep). Nothing surfaced a timeout or error; it was killed and rerun, and the rerun succeeded. | Model/runtime (not plugin) | No plugin change. Note for headless trials. |
| C17 | create-implementation-plan RR-M2 and RR-M3 (same trial) | The planner gated approval on records questions unrelated to the milestone (RR-QN2: `initial-build` Implementation Plans say "Not Approved"), and on RR-M3 asks again how to treat the pre-existing RE-Q1 flake (10 of 20 baseline failures), although `reservation-events` already approved a non-blocking rule (RE-G6). Asking was reasonable; making unrelated records hygiene block approval was not. | Model | No change now; watch for a second case. |
| C18 | create-plan (same trial) | A small enhancement ("list reservations made in the last 30 days": one new field, one store query, one GET endpoint) became 7 milestones: CONTRACT plus three RED/GREEN pairs (timestamp, window selection, endpoint), each with its own Implementation Plan and gate. Each Implementation Plan also ran mutation dry-runs and repeated full-suite runs. After RR-M3 the headless session cost was about $52, with 9 more command runs and 4 more approvals still to go, and the user stopped the work item as out of proportion for a small exercise. The Adaptive Milestone Decomposition rule ("for complex requirements spanning independently testable architectural layers, create a separate RED/GREEN pair per layer") was applied to a change that is not complex. | Plugin | Make the single RED to GREEN pair the default, and split by layer only when the Plan states why one pair is not enough (size, risk, or independent reviewability). Consider bounding Implementation Plan dry-run depth for small milestones. |

Trial evidence for PR #11 (same trial): D1 passed: "approve everything" was refused and the requirements file stayed byte-identical; each approval the user gave in conversation (requirements, Plan, baseline contract, contract, RR-M2 Implementation Plan) was written into the artifact by the main conversation before the next command ran; a terse "accept" or "approve" for one shown artifact was recorded, and "1" (an answer, not an approval) was not. D2 passed: `create-plan`, `create-api-contract` and `create-implementation-plan` forked as `planner` and `generate-tests` as `test-engineer` (`subagents/*.meta.json`); each fork's first message held only the command text plus `ARGUMENTS: <work item>`; questions came back to the user and the run stopped (requirements Q1 to Q20 inline; RR-QN1 and RR-GQ1 from forks). Reports ended with their evidence or questions, but rarely with the literal `Stopped — awaiting user` form. `capture-requirements` runs inline by design. Later in the same trial, `implement-approved-plan` forked as `implementation-engineer` (RR-M3 GREEN; the diff was exactly the approved hunks), and `review-code` forked as `code-reviewer` (a read-only milestone review of RR-M2 and RR-M3 that wrote no file). All five role agents were therefore observed in forks. The user stopped the work item after RR-M3 because of its size (see C18): RR-M4's Implementation Plan was written but not approved, RR-M4 to RR-M7 and the Final Review did not run, and the app-repo changes are left uncommitted on branch `recent-reservations`. Side probe: a bare `agent:` name in a throwaway plugin fell back to `general-purpose`, but PES agent names resolved, so this is not a PES finding.

Run notes for `prompt-quality` (two services, but only the backend changed): one verification command set was enough, so this run neither confirms nor refutes G1–G4.

Run notes for the scribe platform (2026-10-16, Claude Code, 0.14.0; seven services, one repository per service, Java and Python): before any PDD command ran, the architecture was settled in conversation and written into the product-level `docs/requirements.md` (services, data ownership, auth boundaries, queue rules, decision log), because no PDD artifact holds it. This is early evidence for G1's question "where do architecture decisions end up": in the product requirements, outside any reviewed work-item artifact. G5 and G6 were raised by the same run. Work items start in `scribe-contracts` (`protocol-v1`); watch them for G1–G6.

## Draft fixes (awaiting user review)

Nothing below is applied. Each draft names the findings it fixes, the proposed rule, the files it touches, and what to verify. Both D1 and D2 change `.github/` first and mirror the change to `.claude/`.

### D1: approval comes only from the user and is recorded in the artifact (fixes C1 and C11; prerequisite for D2)

Proposed rule. It replaces the conversation clause in the `prompt-driven-development` Approval Status section:

1. An approval is valid for one specific, existing artifact, and only the user gives it.
2. When the user approves in conversation, the main conversation writes it into that artifact's Status (`Approved by <user> on <date>`) before any command builds on it.
3. Every command, including a forked one, accepts only approval recorded in the artifact. It never reads approval from the conversation. If no approval is recorded, it asks and stops.
4. Approval of an artifact that does not exist yet, and "approve everything" or "approve on my behalf", is not approval. Record nothing, tell the user it was not recorded, and stop at each gate as usual.
5. Neither a subagent nor an external loop ever records an approval.

**Decision (user, 2026-10-19):** keep rule 4. Delegated or blanket approval is not approval. The recorded delegated form proposed in C1 is rejected.

Files: the `prompt-driven-development` SKILL Approval Status, plus the approval lines in `create-plan`, `create-api-contract`, `generate-tests`, `implement-approved-plan` and `refactor-code`. Those commands now record an approval given in conversation themselves; they should only confirm the approval already recorded. Tests: update the `test_pdd_controls` wording checks.

### D2: artifact-driven commands run in a fresh context (fixes C13)

| Command | Claude Code frontmatter | Copilot prompt body (first line) |
| --- | --- | --- |
| `create-plan`, `create-api-contract`, `create-implementation-plan` | `context: fork`, `agent: planner`, `background: false` | Delegate to `planner` as a subagent |
| `generate-tests` | fork, `test-engineer` | Delegate to `test-engineer` |
| `implement-approved-plan` | fork, `implementation-engineer` | Delegate to `implementation-engineer` |
| `refactor-code` | fork, `refactoring-engineer` | Delegate to `refactoring-engineer` |
| `review-code`, `review-production-readiness`, `review-architecture` | fork, matching reviewer | Delegate to the matching reviewer |
| `capture-requirements`, `review-requirements`, `setup-*`, `migrate-oracle-to-postgres` | unchanged (inline) | unchanged |

- The Copilot delegation line reads: "Run this command in the `<role>` custom agent as a subagent. Pass it only the work item name and this command's text, and nothing from this conversation. Relay its report unchanged." Keep the existing `agent:` frontmatter, because other Copilot surfaces may use it.
- A forked command's report ends with exactly one of these: written or executed with its evidence; `Stopped — awaiting user: <questions or approval needed>`; or `Blocked — <reason>`. The main conversation relays it, and the user answers there.
- The role agents already have Read, Edit, Write, Bash, Grep and Glob, so they need no tool change.
- Validator and tests: every artifact-driven Claude command sets `context: fork` and an `agent` that exists in `.claude/agents/`, and every matching Copilot prompt contains the delegation line.
- Verify before release: rerun the codeword probe against the real plugin's commands on both tools. The throwaway-plugin probe already passed for Claude `context: fork` and for Copilot subagent delegation. Then run one small real work item end to end and confirm each forked step worked from the artifacts alone.

### D3: OTHER covers a human-run validation, and a milestone can wait on an input (fixes C3, which has two cases: RM6 and TM6)

Current text: OTHER allows only tests, build, configuration, tooling, or infrastructure changes. Its Implementation Plan needs exact code (`implementation-planning` OTHER, "exact code"). Execution Status has only Pending, Blocked, and completed.

Proposed:

1. **Validation protocol in OTHER.** A new bullet in the `prompt-driven-development` OTHER section and in `implementation-planning` OTHER. When the requirements call for a check against a running system or with inputs the user supplies, the OTHER milestone may be a validation protocol. Its exact content is then:
   - the exact commands or steps;
   - each input, who supplies it, and where it is placed (never committed unless the requirements say so);
   - the expected observation and the met or not-met rule for each case;
   - a statement that it changes no repository file other than the evidence it records.

   The dry run runs every step that needs no supplied input and lists the steps it could not run.
2. **Waiting status.** A new Execution Status value, `Waiting — <named input> from <who>`, set when an approved milestone cannot start or continue until the user supplies a named input or performs a named action, such as images, a deployment, or credentials entered by the user. It is not `Blocked`: the Plan stays valid, and the milestone resumes on the same approved Implementation Plan once the input exists. `Blocked` remains the only status that needs replanning.
3. Plan template Execution Status comment: list the allowed values as Pending, Waiting, Blocked, and Executed.

Files: the `prompt-driven-development` SKILL (OTHER, Plan Integrity, Plan Progress), `implementation-planning` SKILL (OTHER, dry run), the Plan template, and `implement-approved-plan` (OTHER branch: set Waiting and stop). Tests: wording checks for the new status.

### D4: amendment milestones are new milestones, not continuations (H1 follow-up from the user review)

Current text (Plan Integrity, contract amendment step 2): "`create-plan` revision mode adds, for each executed milestone the amendment lists, a new Pending milestone **of the same type** (`<milestone> amendment`)".

Proposed replacement for step 2: "`create-plan` revision mode adds new Pending milestones that bring the executed work into line with the amended contract. Each gets its own name and is typed by the kind of change it makes (Milestone Types). For example, a test that encodes the old decision is updated in an OTHER or RED milestone, and a production change is a RED and GREEN pair. None is labelled or numbered as part of an executed milestone. They are placed before the revised Blocked milestone, each with its own Implementation Plan numbered as the next `NNN`. The executed milestones' rows and evidence stay unchanged."

Files: the `prompt-driven-development` SKILL and `create-plan`. Both contain the "same type" wording; `create-api-contract` does not. Tests: replace any check that expects "amendment" naming.

### D5: withdraw the H3 allowance and replace it with the narrower C2 rule (B3 reclassified as Model)

Current text: `implementation-planning` RED allows "a new, non-vacuous test that passes at RED … only when an earlier milestone of this work item already delivers its behavior". The Implementation Plan template has `Tests expected to pass at RED: none | <test> — delivered by <milestone>`.

Proposed:

1. Remove the H3 allowance. A RED test for behavior an earlier milestone delivered means the Plan's traceability is wrong (Rule 8). Stop and return to planning, and do not plan a passing test.
2. Add the C2 rule. A RED milestone may include tests for **preserved existing behavior** only when the Plan's traceability assigns that preserved row to this RED milestone (Owning "none — preserved", Verifying this milestone). They are expected to pass at RED, are listed in Expected Evidence as preserved-behavior tests, and are never counted as RED evidence for any requirement.
3. Template field renamed: `Preserved-behavior tests (expected to pass at RED): none | <test> — preserved row <requirement>`.

**Decision (user, 2026-10-19):** withdraw the H3 allowance and its template field, and replace them with the C2 rule above. B3 stays reclassified as Model.

Files: the `implementation-planning` SKILL (RED), the Implementation Plan template, and `generate-tests`, whose RED self-check compares passing tests with the old "Tests expected to pass at RED" list. Tests: update the H3 checks.

### D6: a fourth traceability form for Final Review obligations (fixes C8)

Current text: Rule 8 says "Three kinds of row have no owning milestone": exclusion, not required, and preserved. The Plan template lists the same three.

Proposed: "Four kinds". Add: a requirement that the Final Review itself fulfils (for example a statement the Final Review must make) is a Final Review obligation. It uses Owning "none — Final Review obligation" and Verifying "Final Review". The Final Review template gets a short "Final Review Obligations" section that answers each such row. Never assign one to a delivery milestone.

Files: the `prompt-driven-development` SKILL (Rule 8), the Plan template (traceability comment), the Final Review template, and `review-code` and `review-production-readiness` (answer every Final Review obligation row). Tests: wording checks.

### D7: the contract template covers message, stream, and RPC interfaces (fixes C12, confirming G2)

Current text: `api-design/templates/API-Contract.md` has only HTTP capability fields (Endpoint, HTTP method, status codes). Contract Completeness questions 1, 7, and 8 are HTTP-worded.

Proposed:

1. Rename "API Capabilities" to "Interfaces". Each interface declares its kind, **HTTP**, **Message or stream** (for example WebSocket or an event topic), or **RPC** (for example gRPC), and fills only that kind's fields:
   - HTTP: the current fields, unchanged.
   - Message or stream: connection and authentication (when credentials are presented and when they are checked); framing and envelope; message catalogue in each direction; ordering, acknowledgement, and delivery semantics, including duplicates and idempotency key; state rules (which message is allowed when); keepalive; close or termination codes and their meaning; limits (size, rate, backpressure).
   - RPC: methods, unary or streaming; stream order and completion; metadata; status codes per failure condition; deadlines where the requirements state them.
2. Reword Completeness questions 1, 7, and 8 to cover every interface kind:
   - 1 "malformed or unreadable request body" becomes "malformed or unreadable input (request body, message, or RPC request)".
   - 7 "status code per failure condition" becomes "error signal per failure condition (HTTP status, close code, or RPC status)".
   - 8 "unknown identifiers" applies to every kind.
3. Contract-Wide Rules gains "Versioning and compatibility of message or RPC schemas".

The scribe-contracts `protocol-v1` contract is the worked evidence. Its improvised sections map onto these fields. Product, library, and protocol names stay out of the template (Keep out of the plugin).

Files: `api-design` SKILL (Contract Completeness), the API-Contract template, and `create-api-contract` (one checklist row per question, unchanged). Tests: the template structure and Completeness checks.

### Trial follow-up drafts (awaiting user review)

D1–D7 above are applied on `release/0.15.0` (1bd6fe7). D8–D10 come from the 0.15.0 trial. The user accepted them on 2026-10-26; they are not applied yet. They are planned to go into the same release, before it merges.

### D8: deferred contract decisions are labelled proposals (fixes C14)

Current conflict:

- `create-plan` gives the CONTRACT milestone "every decision the requirements defer to the contract".
- `create-api-contract` ("ask … and stop instead of choosing") and `api-design` Contract Completeness ("do not choose a default on the user's behalf") forbid choosing.
- In scribe (C12) the model asked first. In the trial (C14) it decided all eight decisions silently.

Proposed rule. It applies only to decisions the approved requirements or Plan **explicitly defer to the contract**:

1. The contract proposes a resolution for each one and records it in Decisions Resolved with Source `Proposed — deferred by <requirement or Plan item>`.
2. The command's report lists every proposal, so the user sees them before reviewing the contract.
3. Approving the contract accepts the listed proposals. Rejecting a proposal sends the contract back for revision.
4. Anything the sources neither answer nor defer is still a clarification question: ask and stop, never choose.
5. The scribe flow, which asked a round of proposals before writing, stays allowed as the alternative to 1. The choice is the command's; the labelling is required either way.

Files:

- `create-api-contract`: the self-check sentence, plus a new sentence on deferred decisions.
- `api-design` SKILL: an exception for deferred decisions in the Contract Completeness paragraph.
- The API-Contract template: the Decisions Resolved Source column allows `Proposed — deferred by …`.
- Tests: wording checks.

### D9: Copilot passes the command text verbatim and the subagent writes the artifact (fixes C15)

Current delegation paragraph: "Pass it only the work item and the rest of this command's text (everything after this paragraph), and nothing from this conversation. Relay its report unchanged." In the trial (Copilot CLI with claude-haiku-4.5), the main model read the artifacts first, passed its own 2.7k-character summary instead of the text, and wrote `Plan.md` itself.

Proposed replacement paragraph for the nine prompts:

> Do not read any artifact or repository file before delegating. Run this command in the `<agent>` custom agent as a subagent (`prompt-driven-development` Fresh Context): pass the work item and the rest of this file verbatim — everything after this paragraph — with nothing added, summarized, or taken from this conversation. The subagent reads the artifacts and writes every file; you write none. Relay its report unchanged.

Before release:

- Retest `create-plan` in Copilot CLI with a stronger model than Haiku and with the real prompt (its `tools:` list included). Pass means the `task` call's prompt contains the command text verbatim, the subagent writes `Plan.md`, and the report is relayed unchanged.
- **If the retest still fails:** remove Copilot delegation for 0.15.0, so Copilot prompts run inline as in 0.14.0. The README then states that fresh context is Claude Code only. A Copilot run that summarizes is worse than one that runs inline, because the summary drops the command's rules.

Files: the nine `.github/prompts`, the validator's `COPILOT_DELEGATION_LINE`, the mutation tests, and the PDD skill Fresh Context sentence on Copilot.

### D10: as few milestones as keep each plan reviewable; split only for a stated reason (fixes C18)

Current text: Adaptive Milestone Decomposition says "Do not default to one giant RED/GREEN pair" and "For complex requirements that span multiple independently testable architectural layers, create separate layer-wise implementation milestones". The application instruction templates repeat it. In the trial, a field, a query and an endpoint were read as "spanning layers": the work became 7 milestones and cost about $52 before the user stopped it.

Constraint from existing guidelines: milestone count must not depend on whether a project is new. The PDD skill says "do not decide FOUNDATION from whether the project is labeled greenfield or brownfield". `getting-started.md` says "Choose each milestone's type by the kind of change, not by whether the project is new". New projects split more because they usually have the reasons below, not because they are new.

Proposed rule (replaces the opening of Adaptive Milestone Decomposition):

1. **Every gate stays.** Requirements, Plan, contract when needed, an Implementation Plan for each milestone, execution, and Final Review are each reviewed by the user. Fewer milestones never removes a gate, never merges RED and GREEN, and never leaves a requirement without an owning milestone and a RED test (Rule 8).
2. **Use as few milestones as keep each Implementation Plan reviewable as exact code.** The default for one cohesive behavior change is one RED milestone and one GREEN milestone, plus CONTRACT and FOUNDATION when the Milestone Types call for them.
3. **Split only for a stated reason.** The Plan records `Decomposition: one pair` or `Split: <reason>` for every work item, and the user approves it at Plan review. Valid reasons:
   - **size:** one Implementation Plan would be too large to review well as exact code;
   - **independent capabilities:** separate behaviors that can be verified on their own, for example create, cancel and list;
   - **different risk:** a data migration or a security change needs its own gate;
   - **ordering:** one part must be verified before the next can be planned;
   - **different verification setup:** a part needs its own test infrastructure.
4. **Layers alone are not a reason.** When a stated reason applies to complex layered work, the layer boundaries are still the preferred split. The existing layer-wise guidance and "not a mandatory architectural template" stay. So a new service with several capabilities normally gets FOUNDATION, CONTRACT, and a pair for each capability or layer. A small new service, or a small enhancement such as `recent-reservations`, gets CONTRACT and one pair.
5. **Lighter planning dry runs, with no lost checks.**
   - Kept: apply the exact code in a disposable copy, run the tests the milestone adds or affects, and, for RED, prove those tests fail without the change and pass with it.
   - Dropped: the full verification suite runs once at execution, not repeatedly during planning. Repeated isolated runs stay where the existing rule requires them (tests that touch persistent state).
   - No mutation testing beyond the RED fail-and-pass proof unless the requirements ask for it.

**Decision (user, 2026-10-26):** D8, D9 and D10 are accepted, including rule 4's narrowing of the layer-wise rule: split by layer only when a stated reason applies. `test_pdd_skill_expresses_layer_wise_decomposition_for_complex_work` and `test_application_instructions_prefer_layers_without_forcing_them` are updated to the new wording, not deleted.

Files:

- The `prompt-driven-development` SKILL: Adaptive Milestone Decomposition.
- Both application instruction templates: the PDD Workflow paragraph.
- The Plan template: a `Decomposition:` line.
- `create-plan`: record the decomposition line.
- `implementation-planning` Planning-Time Dry Run.
- README and `getting-started.md`, which describe decomposition.
- Tests: the two layer tests above, plus new checks for the `Decomposition:` line and the dry-run scope.

### Not in this batch

- G1 and G3–G6 stay predictions until a run shows them.
- C9 stays on Watch.
- The H4 follow-up (dropping the planning trigger and keeping the `security` line) was raised in the user review but not chosen for 0.15.0.

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
- **Development loop (user decision, 2026-10-19):** do not add a loop, runner, or "keep going" command to the plugin. The plugin owns the rules, the artifacts, and where each command stops. A loop outside the plugin (Claude Code `/loop`, headless `claude -p`, Copilot CLI, or a script) may drive a whole work item. Each round it reads `Plan.md` and the approval status of each artifact. It then either runs the single next allowed command, or stops and reports what waits for the user. It never records an approval and never retries a failed verification. The loop does not iterate fixes inside an approved milestone. `implement-approved-plan` applies the plan's exact code, and any difference stops execution for re-approval. Iteration is allowed only on unapproved drafts.
  - **Depends on C1:** the delegated-approval rule must state who may record an approval, so that a loop cannot record one itself.
  - **Depends on C3:** a "waiting on input" status, so that a loop can tell "waiting for the user" apart from `Blocked`.
  - Build and test the runner in its own repository after the release that fixes C1 and C3.

These are evidence only, never skill text: the service names, the speech or LLM provider, the broker product, WebSocket libraries, and any audio format.
