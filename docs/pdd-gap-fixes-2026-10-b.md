# PDD Gap Fixes — October 2026 (batch B)

Status: closed. H1–H4 were released in 0.14.0. B5 (Watch) moves to `docs/pdd-gap-fixes-2026-10-c.md`.

`docs/pdd-gap-fixes-2026-10.md` is closed (released in 0.12.0). This brief starts the next batch.
Every gap below was checked against 0.13.0 (`.github/` on `fix/review-routing-replanning-llm`)
before it was logged.

## Evidence sources

| Project | Work item | Executor | Plugin |
| --- | --- | --- | --- |
| approval-service (new app: 3 HTTP operations, file-based embedded DB, observability, container image) | `initial-build` (CONTRACT, FOUNDATION, 2 × RED/GREEN, OTHER) | Claude Code | 0.11.0 (`.claude/` cache) |

The Final Review for this work item is `docs/.ai/initial-build/Final-Review.md` in the application
repository. Findings F8 and F11–F15 there are the evidence for this brief.

## Rules for this batch

The rules are the same as in the closed brief:

- Fixes must be project-neutral.
- Only plugin gaps get a fix. A finding where the model broke a rule the plugin already states clearly is listed under "No plugin change".
- Prefer structure over prose.
- Use the smallest wording that works.

## Findings Log

| ID | Phase | Finding | Kind | Fix |
| --- | --- | --- | --- | --- |
| B1 | GREEN execution | The approved contract named a metric the runtime cannot emit (the metrics client strips a reserved suffix). The contract had to be amended mid-execution, and an already-executed RED milestone's test had to change. | Plugin (partly addressed in 0.13.0) | H1 |
| B2 | RED planning | Environment-variable names and the configuration-property shape that operators set had no owning artifact. RED test plans decided them implicitly. | Plugin | H2 |
| B3 | RED execution | Four new tests in a RED milestone passed at RED. One was vacuous (B9). Three legitimately checked behavior an earlier milestone already delivered. Nothing says whether that is allowed or how to record it. | Plugin | H3 |
| B4 | Final Review | An authorization defect passed every gate: users are looked up without regard to username case, but ownership is compared exactly, which allowed self-assignment and left requests undecidable. The `security` skill was never applied while planning the milestones that own authorization. | Plugin + Model (B10) | H4 |
| B5 | Requirements | A brand-new application folder had no application instruction file. `capture-requirements` did not notice or mention it. | Plugin (minor) | Watch |
| B6 | All gates | The user gave a standing "approve next steps by yourself"; the model then recorded its own approvals. | Model | — |
| B7 | Requirements | The user answered "use recommended", but the clarification options had no recommended marking. The model picked the options and recorded them as delegated. | Model | — |
| B8 | RED planning | The RED soundness probe (implementation-planning: "confirm the new tests … can pass with it") was skipped. That probe would have caught B1 before the contract was approved. | Model | — |
| B9 | RED execution | A negative-only test (a field "does not exist") passed vacuously at RED and was accepted. | Model | — |
| B10 | RED and GREEN planning | The `security` skill was not loaded, although the milestones owned authentication and authorization. | Model | — |
| B11 | RED planning | The contract's error bodies were verified only through the in-process test client. The real transport asserted only one status code, not a body. | Model | — |
| B12 | FOUNDATION planning | A version choice was justified partly by "available locally". | Model | — |

## Fixes

All four fixes were applied as planned in 0.14.0 to `.github/` and mirrored to `.claude/`.

### H1 — Amending an approved contract during execution (B1)

**Evidence:** the dry run of a GREEN milestone showed that a contract-defined name cannot be produced by the runtime. The model amended the contract itself, wrote an "amendment" Implementation Plan for the already-executed RED milestone, which was numbered after the next milestone's plan, and then ran GREEN.

**Already in 0.13.0:** execution stops, the milestone is marked `Blocked`, the Plan is revised through `create-plan` revision mode, executed milestones keep their evidence, and work resumes after approval. That procedure covers changes to the **Plan**. It says nothing about:

- a change to the **contract** when the Plan itself is unchanged;
- an **executed** milestone whose tests encode the decision that changed.

**Change:**

- `prompt-driven-development` replanning section, one paragraph: when execution shows that an approved contract decision cannot be met, use the same Blocked stop. Then:
  - `create-api-contract` revision mode records the change in an `## Amendments` section, with the change, the reason (evidence), the impact, and the executed milestones that encode the old decision.
  - The Plan revision adds, for each affected executed milestone, a new Pending milestone of the same type (for example "<milestone> amendment"). It gets its own Implementation Plan with the next `NNN`.
  - The original rows and their evidence stay unchanged.
- `templates/API-Contract` guidance, or the `create-api-contract` prompt: describe the Amendments section.

**Files:** `skills/prompt-driven-development/SKILL.md`, `prompts/create-api-contract.prompt.md`, `prompts/create-plan.prompt.md` (revision mode handles contract-amendment Blocked rows).

### H2 — Operator-facing configuration names have an owner (B2)

**Evidence:** the requirements said settings must be overridable through the environment, but neither the Plan rules nor the contract scope assign the names. RED tests fixed the environment-variable names and the property shape, and GREEN had to match them.

**Change:** add one line to Plan Content Rule 2 and to the CONTRACT decision list. When the requirements require externally settable configuration (environment variables, configuration keys, profiles), the names and shapes that operators set are contract decisions. When no CONTRACT milestone exists, they are decided in the first Implementation Plan that needs them, and recorded under Carried-Forward Decisions afterwards.

**Files:** `skills/prompt-driven-development/SKILL.md` (Rule 2), `prompts/create-api-contract.prompt.md`.

### H3 — New tests that already pass at RED (B3)

**Evidence:** the testing skill says "A RED test must fail for the intended missing behavior". The vacuous-negative rule covers only negative-only tests. A positive test whose behavior an earlier milestone already delivered fits neither rule.

**Change:**

- In the `implementation-planning` RED section, one line: a new non-vacuous test that passes at RED is allowed only when an earlier milestone of the work item already delivers its behavior. The Implementation Plan names each such test and that milestone, and the test is not RED evidence for any requirement.
- Add an Implementation Plan template field under Expected Evidence: `Tests expected to pass at RED: none | <test> — delivered by <milestone>`.

**Files:** `skills/implementation-planning/SKILL.md`, `skills/prompt-driven-development/templates/Implementation-Plan.md`, `prompts/generate-tests.prompt.md` (verify that the actual passing set equals the planned set).

### H4 — Apply `security` where authorization is owned; identity comparison (B4)

**Evidence:** the authentication store matched usernames without regard to case, and the ownership checks used exact equality. No gate asked whether identities are compared in one canonical form. The `security` skill is a list of headings with no trigger in the PDD flow.

**Change:**

- `create-implementation-plan`: for a RED or GREEN milestone that owns or verifies an authentication or authorization requirement, apply `security`. The Implementation Plan's Risks section lists any identity, role or ownership comparison and how it is made consistent.
- `security` skill, one line under "authentication and authorization": "identities compared in authorization (ownership, self-action rules) use the same canonical form as authentication (case, whitespace, normalization)."

**Files:** `prompts/create-implementation-plan.prompt.md`, `skills/security/SKILL.md`.

## No plugin change (model broke a stated rule)

| Finding | Existing rule |
| --- | --- |
| B6 self-recorded approvals | `prompt-driven-development` Approval Status: "Only the user approves … approval … in response to a request to approve that specific plan." A standing-delegation mode would be a feature request, not a gap. |
| B7 "use recommended" with no marked option | `requirements-analysis`: "Options you wrote are not the user's words … record only what the user confirmed". AskUserQuestion convention: mark the recommended option. |
| B8 skipped RED soundness probe | `implementation-planning` Planning-Time Dry Run: "For RED, also show the tests are sound … confirm the new tests fail without the behavior and can pass with it" |
| B9 vacuous negative test accepted | `testing` skill and `implementation-planning`: a negative-only test must first exercise the positive case |
| B10 `security` not loaded | `security` skill description: "Use when a change touches authentication, authorization" (H4 adds a structural trigger) |
| B11 error body not verified over the real transport | `testing` skill: "When an approved contract fixes an error status or error body, verify it at least once through the real transport." |
| B12 version justified by the local cache | `implementation-planning`: "never choose a version because it is already in a local cache" |

## Watch (do not hard-code unless it recurs)

- **B5:** a new application folder with no application instruction file. `capture-requirements` could mention that `setup-claude-instructions` / `setup-copilot-instructions` has not been run. Seen once.

## Keep out of the plugin

These are evidence only, never skill text: the metrics library and its reserved suffix, the database product, environment-variable names, the container base image, and test names and counts.
