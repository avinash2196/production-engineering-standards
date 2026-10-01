---
description: "Generate or update the application's .github/copilot-instructions.md from the PDD template. Run first when adopting these standards."
argument-hint: "optional: application name and any values to use for CUSTOMIZE placeholders"
agent: "agent"
tools:
  - read
  - search
  - edit
---
Apply `prompt-driven-development` and `requirements-analysis`.

Generate or update the adopting application's `.github/copilot-instructions.md` from the `prompt-driven-development` skill's `templates/application-copilot-instructions.md`. This is the first step when an application starts using these standards with Copilot, and the step to repeat when the template changes.

This command changes one instruction file only. It creates no work item, requirements, Plan, test, or code, and does not edit `CLAUDE.md` or the product-level `docs/requirements.md`.

1. **Inspect the repository** for each CUSTOMIZE value in the template: runtime and version, framework and version, build system, test framework, application-specific constraints (for example scope exclusions stated in `docs/requirements.md`), the API/external contract path, and the verification commands. Note the file and line each value comes from. Where sources disagree (for example two different runtime versions), record the conflict instead of choosing.
2. **If `.github/copilot-instructions.md` already exists**, read it. Propose its project-specific values for carry-over. Do not carry over anything that contradicts or weakens a FIXED section, and list FIXED sections it is missing or has paraphrased.
3. **Ask the user** to confirm or supply every CUSTOMIZE value, showing the proposed value and its source, and to resolve every conflict. Propose a constraint only when the user or a repository document states it. Stop until answered.
4. **Write `.github/copilot-instructions.md`** from the template: copy every FIXED section verbatim, fill each CUSTOMIZE placeholder with the confirmed value, keep the FIXED and CUSTOMIZE markers, title it `# <application name> — Copilot Instructions`, and replace the template's introductory paragraph with: `Generated from the production-engineering-standards template; regenerate with the setup command when the template changes.`
5. **Report** each CUSTOMIZE value with its source, and — when the file existed — which FIXED sections were added or restored and which previous content was dropped and why.
