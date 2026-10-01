---
description: "Generate or update the application's CLAUDE.md (PDD process rules) from the template. Run first when adopting these standards."
argument-hint: "optional: application name"
agent: "agent"
tools:
  - read
  - search
  - edit
---
Apply `prompt-driven-development`.

Generate or update the adopting application's `CLAUDE.md` from the `prompt-driven-development` skill's `templates/application-claude-instructions.md`. Run this first when an application — new or existing — starts using these standards with Claude Code, and again whenever the template changes.

The file holds process rules and pointers only. Project facts — technology stack, versions, constraints, verification commands — are not written into it; they live in requirements, the build file, the Plan, and Implementation Plans. This command asks no questions and changes only `CLAUDE.md`: no work item, requirements, Plan, test, or code, and not `.github/copilot-instructions.md` or `docs/requirements.md`.

1. **Read the template** from the `prompt-driven-development` skill's `templates/` folder, next to its `SKILL.md`. If it cannot be read, stop and report the locations tried. Never write the file from memory or from another file.
2. **Determine the application name** from the repository (build file project name, else the repository folder name) and note its source.
3. **If `CLAUDE.md` already exists**, read it and list every line that is not in the template — for example stack, versions, constraints, persistence, commands, or older workflow text — with the reason it is dropped and where that information belongs instead (`docs/requirements.md`, the build file, or the Plan / Implementation Plan). Do not move it there; that is the user's decision.
4. **Write `CLAUDE.md`**: the template verbatim, titled `# <application name> — Claude Code Instructions`, with the template's introductory paragraphs replaced by `Generated from the production-engineering-standards template; regenerate with the setup command when the template changes.`
5. **Report** the application name and its source, and — when the file existed — the dropped lines from step 3.
