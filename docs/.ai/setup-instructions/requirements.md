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

- FIXED sections are copied verbatim from the template; only CUSTOMIZE values are project-specific.
  [Repo: templates/application-*-instructions.md, generation comment]
- CUSTOMIZE values are proposed from repository inspection, each with its source, and confirmed by the
  user before the file is written. Conflicting evidence is asked, not chosen. [Derived from
  `requirements-analysis` Clarification Gate]
- When the target file exists, its project-specific values are proposed for carry-over; content that
  contradicts a FIXED section is not carried over. [Derived from the drift described in Context]
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

- AC-1: Running the Claude command in an application with an outdated `CLAUDE.md` produces a file whose
  FIXED sections match the template verbatim and whose CUSTOMIZE values were confirmed by the user.
- AC-2: Same for the Copilot prompt and `.github/copilot-instructions.md`.
- AC-3: `README.md` and `docs/getting-started.md` present the command as step 1.
- AC-4: Validator and unittest suite pass.
