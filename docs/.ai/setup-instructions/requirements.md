# Requirements — setup-instructions

## Context

Adopting the plugin requires an application-level instruction file — `CLAUDE.md` for Claude Code,
`.github/copilot-instructions.md` for Copilot — built from the `prompt-driven-development` templates.
Today this is a manual copy (`README.md` Adopting the Standards Repository, `docs/getting-started.md`
§3). An evaluation repository showed the manual path drifting: its `CLAUDE.md` was produced from an
older template and lacked the FIXED "No Code Change Without Approval" section and the current
milestone workflow, and its `.github/copilot-instructions.md` still described flat `docs/.ai/` paths
and capabilities the application had since added.

## Requirements

- **SI-1** — Provide a command that generates or updates the adopting application's `CLAUDE.md` from
  `templates/application-claude-instructions.md`. [User]
- **SI-2** — Provide a command that generates or updates the adopting application's
  `.github/copilot-instructions.md` from `templates/application-copilot-instructions.md`. [User]
- **SI-3** — The commands are the documented first step for using the plugin in an application. [User]
- **SI-4** — Both commands exist for Copilot (prompt) and Claude Code (command). [Derived from the
  repository convention that every workflow entry point exists in both environments — confirmed by the
  user's request for commands usable with "these plugins"]
- **SI-5** — Update both templates so they support generation. [User]
- **SI-6** — Update the documentation. [User]

## Behavior of the commands

- **SI-7** — The instruction file holds process rules and pointers only. Project facts — stack,
  versions, constraints, persistence, verification commands — are not written into it; they live in
  requirements, the build file, the Plan, and Implementation Plans. [User, 2026-10-01; confirmed
  "yes make the changes"]
- **SI-8** — The command copies the template verbatim (only the title names the application) and asks
  no questions, so it works for a new project before any code exists. [Derived from SI-7 — confirmed
  by the user's approval]
- **SI-9** — If the template cannot be read, the command stops; it never writes the file from memory.
  [User-observed Copilot run: template path not found, command continued]
- **SI-11** — The command opens the template by its exact path under the plugin root and verifies its
  first line; it never locates it by searching file contents. [User-observed Copilot run on 0.9.1: a
  content search for the file name opened the Claude template, which mentions the Copilot one]
- **SI-10** — When the target file exists, the command lists every line not in the template with the
  reason it is dropped and where it belongs; it does not move that content. [Derived from SI-7 —
  confirmed by the user's approval]
- The command writes only its one target file. It is an instruction-file change, not a code change.
  [Repo: CLAUDE.md, No Code Change Without Approval — documentation-only exception]

## Repository-Confirmed Facts

- The validator requires the No-Code-Change block in both templates and requires every
  `REQUIRED_PDD_OPERATIONS` command in both environments; new commands need no validator change.
  [Repo: tooling/scripts/validate_repository.py:45-76, 203-219]
- Prompts must bind to an existing agent or a built-in agent. [Repo: tooling/tests/test_prompts_and_links.py:8-21]

## Operational Characteristics

Instruction text only; no running system. All six characteristics: not required for this work item.

## Acceptance Criteria

- AC-1: Running the Claude command in an application with an outdated `CLAUDE.md` asks no questions,
  produces a file identical to the template apart from the title, and lists the dropped
  project-specific lines.
- AC-2: Same for the Copilot prompt and `.github/copilot-instructions.md`.
- AC-3: `README.md` and `docs/getting-started.md` present the command as step 1.
- AC-4: Validator and unittest suite pass.
