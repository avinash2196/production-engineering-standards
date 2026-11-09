# PDD Gap Fixes — November 2026 (batch D): code quality, review, and API conventions

Status: draft for user review. Nothing here is applied. Skill text changes start only after 0.15.0 is released and the user approves this brief (user decision, 2026-10-30).

## Why this brief

The user asked (2026-10-30) for rules on good code and good review. The plugin currently has almost none:

- `code-review` is 18 lines: correctness, scope, production safety, evidence.
- `java-spring-boot` is 17 lines and has no layering rule.
- `observability` says only "structured logs with safe identifiers" and "do not log secrets".
- `api-design` covers contract completeness, but not verb choice, path design, or where parameters go.

Nothing covers file or method size, naming, reuse and shared code, comments, PR size, or work that spans business domains. Nothing reviews a milestone's diff before a PR is opened, or turns it into a commit and PR (added 2026-11-09).

## Design (agreed in conversation, 2026-10-30)

1. **One source of truth.** A new language-neutral `code-quality` skill. The planner applies it when writing exact code in an Implementation Plan, the implementation and refactoring engineers apply it when executing, and the code reviewer checks against it. The same rules apply at every stage, so the review finds less.
2. **Numbers are defaults, not plugin rules.** The plugin stays project-neutral. Each limit is a default that a project can override in a `## Code Standards` section of its CLAUDE.md or copilot-instructions (added to both setup templates). A project value always wins.
3. **The existing repository wins.** Where the repository already has a clear convention (naming, folder layout, error shape, API style), follow it. The defaults apply only where there is none.
4. **Severities: High, Medium, Low (user decision, 2026-11-09, replacing Blocker/Warning).** One scale across planning, review and `prepare-pr`. **High** (was Blocker): must be fixed before approval or before a PR is opened. **Medium** (was Warning): fix it, or record a one-line justification in the Implementation Plan, the review or the PR body; a justified Medium finding counts as satisfied. **Low**: optional polish; listed, never blocking. A severity is given only with a concrete failure scenario (`code-review` rule 7).
5. **No noise.** Every finding cites a rule ID and `file:line`. The existing rule "do not manufacture checklist findings" stays. A rule that does not apply to the change is not reported.
6. **Evidence first.** Each rule cites a run or a user decision. The user's articles say "add structure when it solves an observed problem". Rules without run evidence are marked *(user decision)*. They can be dropped at review.

## Evidence from past runs

| ID | Run | What happened | Rules it supports |
| --- | --- | --- | --- |
| E1 | medgemma `xray-pipeline` Final Review F9 | `xray ask` logged the image file name; a file named after a patient would put that name in `run.log`. | LG3 |
| E2 | medgemma `xray-pipeline` Final Review F10 | Leftovers outside the code: README still described the removed demo and its endpoints. | RV3 |
| E3 | workspace-reservation `reservation-events` (RE-M6) | Event publishing was injected into `ReservationController` and called after the create, so a side effect sits in the controller rather than the service. The Final Review lists the change with no layering comment. | LY1, LY2 |
| E4 | order-management `oracle-persistence` Final Review | Environment-variable naming mismatch reported between `docker-compose.yml` and `application.properties`. Later rejected as not real, but naming of configuration keys was reviewed only by chance. | NM3 |
| E5 | 0.15.0 trial `recent-reservations` (C14) | Contract decisions (path, parameters, empty result, ordering) were chosen silently. Models know REST; the failure was an unreviewed choice, not ignorance. | AP1 |
| E6 | User request, 2026-10-30 | File size, utilities folder, method naming, logging, comments, controller → service → DAO, PR size, multi-domain PRs, related changes only, HTTP verbs, path vs query vs body. | all *(user decision)* |

Before applying, sweep the remaining Final Reviews and code-review outputs (approval-service, scribe, workspace-reservation) for more E rows. A rule with no E row other than E6 stays in only if the user keeps it at review.

## Proposed rules

### Size and shape (`code-quality`)

| ID | Rule | Default | Severity |
| --- | --- | --- | --- |
| SZ1 | A source file holds one responsibility. Above the default, say why or split by responsibility. | 400 lines | Medium |
| SZ2 | A method does one thing. Above the default, extract named steps. | 40 lines | Medium |
| SZ3 | Nesting depth. Use guard clauses and early returns instead. | 3 levels | Medium |
| SZ4 | Parameter count. Above it, introduce a parameter object. No boolean flag parameters that switch behavior; use two methods. | 4 | Medium |

### Naming (`code-quality`)

| ID | Rule | Severity |
| --- | --- | --- |
| NM1 | A method name is a verb phrase at the domain level that says what it does (`reserveDesk`, `findActiveReservations`), not how or vaguely (`process`, `handle`, `doWork`). A boolean method reads as a question (`isExpired`, `hasConflict`). | Medium |
| NM2 | A class name is a noun for its one responsibility. Avoid `Manager`, `Helper`, `Util` without a domain word. | Medium |
| NM3 | No unexplained abbreviations. Configuration keys and environment variables use one naming scheme across all files that read them. | Medium |
| NM4 | Test names state the behavior and the expected result. | Medium |

### Reuse and shared code (`code-quality`)

| ID | Rule | Severity |
| --- | --- | --- |
| RU1 | Search the repository for existing code before writing new code. Do not duplicate logic that already exists. | Medium |
| RU2 | A helper with two or more callers and no business logic goes in the project's declared shared location, which defaults to the repository's existing `util`/`common` package. Code with business logic stays in its domain package; no `utils` dumping ground. | Medium |
| RU3 | No code copied between services or modules where a shared library already exists. | Medium |

### Comments (`code-quality`)

| ID | Rule | Severity |
| --- | --- | --- |
| CM1 | Comments explain **why** (a constraint, a decision, a workaround and its reason), never **what** the code already says. | Medium |
| CM2 | A public API (exported class, public method of a library, endpoint handler) has a doc comment stating its contract. | Medium |
| CM3 | No commented-out code. | High |
| CM4 | A TODO or FIXME names a ticket or an owner. | Medium |

### Logging (`observability`, extended)

| ID | Rule | Severity |
| --- | --- | --- |
| LG1 | Levels: ERROR when someone must act, WARN for a handled problem worth counting, INFO for business events, DEBUG for diagnostics. | Medium |
| LG2 | Log a failure once, where it is handled. No log-and-rethrow. | Medium |
| LG3 | Never log secrets, tokens, personal data, full payloads, or file names that can carry personal data (E1). | High |
| LG4 | Each log line carries the correlation ID and the stable identifiers needed to trace it. | Medium |
| LG5 | No empty catch blocks and no swallowed exceptions. | High |

### Layering (`java-spring-boot`, `python-fastapi`, `architecture-design`)

| ID | Rule | Severity |
| --- | --- | --- |
| LY1 | Controller (or router) → service → repository (or DAO). A controller handles HTTP only: binding, validation, mapping to the response. It never calls a repository. | High |
| LY2 | Business rules, side effects (publishing events, calling other services), and transaction boundaries belong in the service (E3). | Medium |
| LY3 | A service takes no HTTP or framework web types. A repository returns domain or persistence types, not response DTOs. | High |
| LY4 | Dependencies point inward. Nothing in the domain depends on the web or persistence layer (`architecture-design`, language-neutral). | Medium |

### HTTP API conventions (`api-design`)

| ID | Rule | Severity |
| --- | --- | --- |
| AP1 | The repository's existing API conventions win. Any deviation from them or from these defaults is recorded in API-Contract.md for review (E5). | Medium |
| AP2 | GET reads with no side effects. POST creates or runs a non-idempotent action. PUT replaces the whole resource and is idempotent. PATCH updates part of it. DELETE removes and is idempotent. | High |
| AP3 | Paths are plural nouns, not verbs (`/reservations`, not `/getReservations`). An action that does not fit CRUD is a sub-resource (`POST /reservations/{id}/cancellation`). One casing style. No more than about two nesting levels. | Medium |
| AP4 | The path identifies a resource (`/reservations/{id}`). The query holds optional filtering, sorting, and paging for a collection. The body holds the data being created or changed. No personal or sensitive data in the path or query, because both end up in logs. | High for sensitive data; else Medium |
| AP5 | Status codes: 200, 201 with `Location` on create, 204 with no body, 400 invalid input, 404 not found, 409 conflict (422 only if the repository already uses it). One error shape everywhere. | Medium |

### Review scope (`code-review`)

| ID | Rule | Severity |
| --- | --- | --- |
| RV1 | PR size. Above the default changed lines (excluding tests, generated files, and lock files), warn and suggest a split. In PDD, a PR is one milestone or one related set of milestones of one work item. | Medium, default 400 lines |
| RV2 | Related changes only. In PDD, a file outside the Implementation Plan's file list is High. Outside PDD, unrelated refactors and drive-by changes are Medium. | High in PDD; else Medium |
| RV3 | Leftovers. Docs, configuration, and references made stale by the change are updated in the same PR (E2). | Medium |
| RV4 | Business domains. When one PR touches more than one business domain (bounded context or top-level domain package), warn and ask for the reason. | Medium |
| RV5 | Layering and API conventions are checked against LY1–LY4 and AP1–AP5, and implemented endpoints against the approved contract. A mismatch with the contract is High. | as listed |
| RV6 | Every finding gives the rule ID, `file:line`, severity, the failure scenario, and the recommended fix. Findings are ordered High, Medium, Low. | — |

### Pre-PR review, commit and PR (`prepare-pr` command) *(user decision, 2026-11-09)*

The lifecycle has no step between an executed milestone and a pull request. `review-code` writes the Final Review only, and nothing turns verified work into a reviewed commit and PR. No run has shown this yet; the user asked for it.

| ID | Rule |
| --- | --- |
| PR1 | One command, `prepare-pr <work-item>`. In Claude Code it is a fork bound to `production-engineering-standards:code-reviewer`; no new agent. It covers one executed milestone, or a RED/GREEN pair of the same work item (RV1). |
| PR2 | **Stop 1, review (writes nothing).** Diff the branch against its base. Check the diff against the Implementation Plan's file list (RV2), the approved contract (RV5), `code-quality`, and the relevant domain skills. Report findings ordered High, Medium, Low (RV6). Draft the commit message and PR body from the artifacts: work item and milestone IDs, requirements covered, verification command and its recorded result, and any justified Medium finding. Then stop. |
| PR3 | **Recommend, never fix.** A finding's fix is a recommendation. Any code change goes through PDD: an amendment milestone (D4) or a small fix work item (brief E, C27). A High finding blocks stop 2 until it is fixed that way and stop 1 runs again. |
| PR4 | **Stop 2, commit and PR (on the user's word only).** Only after the user says go in a new message, and with no open High finding: commit with the drafted message, push the branch, and open the PR as a draft unless the user asks otherwise. Never merge, never force-push, never commit to the default branch. Report the commit hash and the PR link. |
| PR5 | **Copilot.** The prompt runs inline (C19), so it ends after stop 1. Stop 2 needs a new chat and the user's go. |
| PR6 | **Evidence.** The PR body quotes only verification that was actually run and recorded in `Plan.md`. It never claims a check passed that did not run. |

## Files (when applied)

- New `.github/skills/code-quality/SKILL.md`: SZ, NM, RU, CM. Mirrored to `.claude/`.
- `observability`: LG. `java-spring-boot` and `python-fastapi`: LY1–LY3 in each stack's terms. `architecture-design`: LY4. `api-design`: AP. `code-review`: RV, plus "apply `code-quality`".
- Agents: planner, implementation-engineer, refactoring-engineer, and code-reviewer reference `code-quality`.
- `implementation-planning`: the exact code in a plan follows `code-quality`, and the self-check lists any justified Medium finding.
- New `.github/prompts/prepare-pr.prompt.md` and `.claude/commands/prepare-pr.md` (PR1–PR6). README Quickstart and `docs/getting-started.md`: the step after each executed milestone. `prompt-driven-development` lifecycle: where `prepare-pr` sits.
- Both setup templates: an optional `## Code Standards` section for project overrides (limits, shared-code location, domain packages).
- Validator and tests: the skill exists and is mirrored, every rule ID is unique, the agents reference it, the template has the override section, and `prepare-pr` is mirrored and bound to the namespaced code-reviewer.

## Open decisions for the user

1. Keep the default numbers (400-line file, 40-line method, nesting 3, 4 parameters, 400-line PR) or change them.
2. Which rules without run evidence (E6 only) stay.
3. Whether SZ and NM are Medium everywhere (proposed) or High for new code.
4. Release target: 0.16.0 together with C20 and lighter plans (proposed), or its own release.
5. `prepare-pr`: whether stop 2 opens the PR as a draft by default (proposed), and whether it runs after every executed milestone or only after the GREEN of a pair.

## Keep out of the plugin

- Formatter and linter configuration (line length, import order, brace style). These belong to the project's tooling.
- Language style guides beyond the rules above.
- Automatic enforcement. These are review rules; only `tooling/` checks can fail.
