# Repository Instructions Template

## Purpose

Provide a minimal onboarding and usage guide for an adopting repository without assuming every standards-repository capability is used.

## Project Context

- Service/project: `<SERVICE_NAME>`
- Owner: `<TEAM_OR_ROLE>`
- Stack: `<STACK>`
- Production runtime: `<RUNTIME_OR_UNKNOWN>`

## Copilot Customizations

If copied into the adopting repository, use GitHub-native locations:

- repository instructions: `.github/copilot-instructions.md`
- path-specific instructions: `.github/instructions/*.instructions.md`
- custom agents: `.github/agents/*.agent.md`
- prompt files: `.github/prompts/*.prompt.md`
- Agent Skills: `.github/skills/<skill-name>/SKILL.md`

Copy only the customizations the project intends to maintain. Do not assume a link to another local repository automatically loads those files.

## Engineering Standards

List the standards this project has explicitly adopted and any project-specific overrides/ADRs.

## Configuration and Secrets

- Document only configuration sources the project actually uses.
- Define deterministic precedence when multiple sources exist.
- Production secrets must use the project's approved secure delivery/access mechanism.
- If the project adopts the repository `SecretProvider` capability or local `SECRET_ADAPTER=env` reference, document that choice explicitly and prevent local-only behavior from activating in production.

## Local Development

Document the actual local profile/file convention used by the selected stack (for example Spring `application-local.yml` or a project-defined Python settings source). Keep local-only files and real credentials out of version control.

## Infrastructure Dependencies

List only required dependencies and how developers obtain realistic local equivalents (containers, official emulators, fakes, or approved local adapters).

## Repository Commands

- Plan: `/create-plan`
- Milestone Implementation Plan: `/create-implementation-plan`
- RED milestone: `/generate-tests`
- GREEN/non-behavior milestone: `/implement-approved-plan`
- REFACTOR milestone: `/refactor-code`
- Repository validation: `python tooling/scripts/validate_repository.py` when this tooling is copied into the adopting repository

## Human Review

Custom agents, prompts, and skills support the workflow; they do not waive Plan, milestone approval, security, or production-readiness review gates.
