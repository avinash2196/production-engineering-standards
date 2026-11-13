# PDD Gap Fixes — November 2026 (batch G): real verification, light dry runs, fix escalation

Status: change plan awaiting the user's approval. Nothing applied. Target release 0.16.2, one PR into `main`, then tag `v0.16.2`. Brief F S1–S6 stay in 0.17.0.

## Evidence

| ID | Source | What happened | Class |
| --- | --- | --- | --- |
| G1 | Local transcripts, 15 `create-implementation-plan` forks (2026-11-09 to 11) | The two slowest (55 min each, Voice-Narration) spent 47 and 32 minutes in tools: full `docker build` of the GPU Chatterbox image (torch, CUDA), `pip install --dry-run` in containers, a throwaway venv, 10-minute polling loops on background build logs. A revision rebuilt everything again. Fast runs (1–13 min) had no image builds. | Plugin: `implementation-planning` Planning-Time Dry Run asks to cover "runtime or infrastructure definitions" with "each tool's own validation", with no limit on builds, downloads, or time. |
| G2 | Voice-Narration `chatterbox-cloud-run` | AC-CCR-1 names the real Cloud Run service, but every milestone tested against fakes; RSK-10: "no milestone observes the real model loading on the deployed GPU". The real defect (watermarker import at startup) was found only by the user's manual deploy; CRM-9 was added after. | Plugin: nothing asks how a real external system is proven; Plan Content Rule 3 leaves test isolation to the Implementation Plan, which defaults to fakes; Final Review does not separate fake from real evidence. |
| G3 | Voice-Narration `initial-build` | Mock inference was planned (FR-040), a real Google provider got wired; the Plan shows "Blocked — drift reconciliation required". | Plugin: same missing decision (dev adapter vs test double vs real evidence). |
| G4 | User, 2026-11-13 | Fixes jump straight to code and can loop on guesses instead of diagnosing from logs and evidence. | Plugin: Fix Work Items say what the requirements hold, not how the cause is found or when to stop. |

## Decisions (user, 2026-11-11 to 13)

| ID | Decision |
| --- | --- |
| D1 | How each external system is proven for real is **asked in the requirements interview**, and **re-confirmed per milestone in `create-plan`**, because the picture changes in big apps. The plugin never decides it. |
| D2 | An AC that names a real system but cannot be proven for real in this work item is allowed only when the user accepts it; it is recorded and listed at Final Review. |
| D3 | The agent may call a declared deployed test service and read its revision; deploys and anything with spend or production credentials are run by the user or CI, and the output is pasted in. Testing against the deployed GPU or cloud service replaces local image builds. |
| D4 | The interview asks what a fake may be built from (approved contract, recorded real response, other); fakes are never invented. |
| D5 | Final Review: an AC that names a real system with only fake evidence, and no user acceptance, is a blocking finding. (Recommended; confirmed by approving this plan.) |
| D6 | Fix escalation: one quick attempt when the cause is evident; escalation triggers move to diagnosis; at most 3 attempts in all, each on a different basis; transient re-runs of the same command (up to 3, no code change) do not count. (3 attempts: user; structure: confirmed by approving this plan.) |
| D7 | Stop and discuss: when attempts run out, no hypothesis survives, evidence is out of reach, or about 20–30 minutes pass with no new information, stop and report back with evidence, attempts, open hypotheses, what is needed, and options. Applies to every command. |
| D8 | Planning dry runs stay light; heavy checks move to execution in the environment the Plan names. |

## Change plan

No other rule changes. `.github/` is edited and mirrored byte for byte to `.claude/`.

| # | File | Change |
| --- | --- | --- |
| 1 | `skills/requirements-analysis/SKILL.md` | New section **Real-System Verification** (after Operational Characteristics). Three kinds kept apart: local-development adapter (a product feature), test double (a test technique), real verification (evidence). For each external system the work item calls (model, API, cloud service, database, broker), ask: (1) is it proven for real in this work item, and how — local tests, local container, deployed test service, CI, manual user run, or not proven; (2) where the real one runs (service name or URL, region); (3) who deploys it and how the deployed revision is read; (4) whether tests may use a fake and what it is built from; (5) what cannot run locally (no GPU, image or download too large, no credentials); (6) if not proven for real, does the user accept that. Never answer for the user; reuse answers from `docs/verification-environments.md` when present (project-owned, cited as `[Repo: …]`) and ask only the rest. Material: an unanswered (1) blocks planning. |
| 2 | `skills/requirements-analysis/SKILL.md` | New section **Diagnosis Before a Fix** for fix work items: collect evidence (error output, logs, deployed revision, diff since the last good state, failing test output; reuse what is already known in the session, read fresh anything that changes), reproduce or say why not, one root cause with citations and the alternatives ruled out, unproven causes labelled hypotheses, missing evidence requested from the user, no fix proposed. Quick path: when the error itself shows the cause (for example a stack trace pointing at one line), the requirements say so in one line and skip the section. |
| 3 | `prompts/capture-requirements.prompt.md` | One line each: apply Real-System Verification; for a fix work item, apply Diagnosis Before a Fix and say which path (quick or diagnosis) and why. |
| 4 | `templates/requirements.md` | New sections **Real-System Verification** (table: system, proven how, where it runs, who deploys, revision read by, fake built from, local limits, accepted gap, source) and **Diagnosis** (fix work items only; omitted otherwise). |
| 5 | `prompt-driven-development/plan-rules.md` | New Plan Content Rule 14 **Verification per milestone**: the Plan holds a Verification Environment table, one row per milestone (level, target, who deploys, fake source), prefilled from requirements; `create-plan` asks the user to confirm every row that differs from the requirements, is new, or is not covered, and records changes with the user as source. A change that turns an AC into "not proven for real" goes back through `capture-requirements`. A milestone that changes a deployed service itself is verified only after a redeploy of that change. Rule 3 unchanged: the Plan states real or double per AC, never a mocking library. |
| 6 | `prompt-driven-development/plan-rules.md` | Rule 12 addition: each Final Acceptance Criterion that names a real system states its evidence kind (real, double, or not proven — accepted Qn). |
| 7 | `templates/Plan.md` | New section **Verification Environment** (table) after Verification Commands; Final Acceptance Criteria comment names the evidence kind. |
| 8 | `prompts/create-plan.prompt.md` | One line: apply Rule 14 and ask before writing the Plan. |
| 9 | `skills/implementation-planning/SKILL.md` | Planning-Time Dry Run: always local and light — apply the diff, compile, the Test Scope tests, static or validate-only checks (for example `docker build --check`, a linter, `--dry-run` resolution against what is already installed or cached). Never during planning: building a container image, a download over about 500 MB, starting a container or cloud resource, deploying, or waiting on a background job. Budget about 10 minutes in all; a step over budget is listed as "deferred to execution in <the Plan's environment>" with its exact command. A revision re-runs only checks whose files changed. A dry run that would need more stops and asks. |
| 10 | `prompts/create-implementation-plan.prompt.md` | One line: follow the Plan's Verification Environment row; if the repository shows it cannot work, stop and ask. |
| 11 | `prompt-driven-development/execution.md` | Real-verification evidence records the target, the deployed revision or image digest, and the commit it was built from; evidence from a revision that does not match the branch does not count. The agent calls only declared test targets and never deploys or spends unless the approved Implementation Plan names the command and the Plan row says the agent runs it (D3 default: the user or CI). |
| 12 | `prompt-driven-development/SKILL.md` (core) | New section **Attempts and Escalation** (every command loads it): one quick attempt; escalation triggers (the attempt failed, the error returns or moves, the cause is not visible in the error, the fix spreads beyond where the error points, evidence contradicts the explanation); diagnosis; at most 3 attempts, each on a different basis and each stating what it expects to see; a repeated or merely widened change is never an attempt; transient re-runs separate. Then **stop and discuss** with the six-part report (symptom, evidence, attempts, ruled out and open hypotheses, what is needed, options with a recommendation). Approval gates are unchanged: inside execution a failed check still stops at once (Plan Integrity); the budget governs diagnosis, dry runs, and free-form debugging. |
| 13 | `prompt-driven-development/milestone-types.md` | Fix Work Items: quick path or Diagnosis (requirements-analysis), and a fix Plan cites the diagnosed cause; a fix aimed elsewhere stops and asks. |
| 14 | `prompt-driven-development/final-review.md`, `templates/Final-Review.md` | D5: a criterion that names a real system with only double evidence and no recorded acceptance is a blocking finding; the evidence table shows the evidence kind. |
| 15 | `templates/application-claude-instructions.md`, `application-copilot-instructions.md` | Project Context: one pointer line to `docs/verification-environments.md` (project-owned, optional; the setup command never writes it). Command Routing: "something is broken" keeps routing to a fix work item; no new section. |
| 16 | Core `SKILL.md` Parts table | Unchanged parts; Attempts and Escalation lives in the core. |
| 17 | `tooling/scripts/validate_repository.py` | Required-token checks for the new sections (requirements-analysis, requirements and Plan templates, Rule 14, dry-run limits, Attempts and Escalation, D5); both trees. |
| 18 | `tooling/tests/` | New `test_real_verification.py` (tokens and placement for items 1–15) and mutation tests for the new validator checks; no existing assertion deleted or weakened. |
| 19 | Manifests, history | Version 0.16.2 in all four manifest places; this brief marked applied with measured word counts; History README row. |

## Verification

Validator and the full test suite, run and reported. Word count per command before and after (core grows by about 300 words). Not covered by tests: behavior in a real run — checked in the user's projects (Voice-Narration, work-order) after release: a `create-implementation-plan` on a GPU-service milestone should finish without an image build, and a fix work item should show the quick or diagnosis path.

## Not in this batch

- Brief F S1–S6 (strategy level, parallel work items): 0.17.0.
- Recommending a cloud provider or platform: the plugin lists what the project declared, never picks.
