---
name: code-quality
description: Use when writing exact code in an Implementation Plan, executing or refactoring it, or reviewing changed code, for size, naming, reuse, comments, and the High/Medium/Low severity scale.
---

# Code Quality

One set of rules for every stage: the planner applies them to the exact code in an Implementation Plan, the implementation and refactoring engineers apply them when executing, and the code reviewer checks against them.

## Precedence

1. **Project overrides win.** When `docs/code-standards.md` exists, its values (limits, shared-code location, domain packages) replace the defaults below.
2. **Existing conventions win next.** Where the repository already has a clear convention (naming, folder layout, error shape, layering, API style), follow it. The defaults apply only where there is none.
3. **Defaults last.** The numbers below are defaults, not rules.

These are review rules. Formatting, line length, import order, and linter configuration belong to the project's own tooling.

## Severity

One scale across planning, review, and `prepare-pr`:

| Severity | Meaning |
| --- | --- |
| **High** | Must be fixed before approval, or before a PR is opened. |
| **Medium** | Fix it, or record a one-line justification in the Implementation Plan, the review, or the PR body. A justified Medium finding counts as satisfied. |
| **Low** | Optional polish. Listed, never blocking. |

A severity is given only with a concrete failure scenario (`code-review`). A rule that does not apply to the change is not reported.

## Findings

Every finding gives the rule ID, `file:line`, severity, the failure scenario, and the recommended fix. Findings are ordered High, Medium, Low. Do not manufacture findings to fill categories.

## Size and shape

| ID | Rule | Default | Severity |
| --- | --- | --- | --- |
| SZ1 | A source file holds one responsibility. Above the default, say why or split by responsibility. Test files are exempt. | 400 lines | Medium |
| SZ2 | A method does one thing. Above the default, extract named steps. | 40 lines | Medium |
| SZ3 | Nesting depth. Use guard clauses and early returns instead. | 3 levels | Medium |
| SZ4 | Parameter count. Above it, introduce a parameter object. No boolean flag parameters that switch behavior; use two methods. | 4 | Medium |

## Naming

| ID | Rule | Severity |
| --- | --- | --- |
| NM1 | A method name is a verb phrase at the domain level that says what it does (`reserveDesk`, `findActiveReservations`), not how or vaguely (`process`, `handle`, `doWork`). A boolean method reads as a question (`isExpired`, `hasConflict`). | Medium |
| NM2 | A class name is a noun for its one responsibility. Avoid `Manager`, `Helper`, or `Util` without a domain word. | Medium |
| NM3 | No unexplained abbreviations. Configuration keys and environment variables use one naming scheme across every file that reads them. | Medium |
| NM4 | A test name states the behavior and the expected result. | Medium |

## Reuse and shared code

| ID | Rule | Severity |
| --- | --- | --- |
| RU1 | Search the repository for existing code before writing new code. Do not duplicate logic that already exists. | Medium |
| RU2 | A helper with two or more callers and no business logic goes in the project's shared location (`docs/code-standards.md`, else the repository's existing `util` or `common` package). Code with business logic stays in its domain package; no `utils` dumping ground. | Medium |
| RU3 | No code copied between services or modules where a shared library already exists. | Medium |

## Comments

| ID | Rule | Severity |
| --- | --- | --- |
| CM1 | A comment explains **why** (a constraint, a decision, a workaround and its reason), never **what** the code already says. | Medium |
| CM3 | No commented-out code. | High |
| CM4 | A TODO or FIXME names a ticket or an owner. | Medium |

## Rules owned by other skills

Logging (LG1–LG5) is in `observability`. Layering is in `java-spring-boot` and `python-fastapi` (LY1–LY3) and `architecture-design` (LY4). HTTP API conventions (AP1–AP5) are in `api-design`. Review scope (RV1–RV6) is in `code-review`. Apply them where the change touches that area.
