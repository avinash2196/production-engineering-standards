# Repository Instructions Template

Purpose
- Provide a clear, minimal onboarding and usage guide for this repository and its agents. Link to responsible agents and explain safe tool usage and override policies.

Placeholders
- Service name: <SERVICE_NAME>
- Owner: <TEAM/OWNER>
- Contact: <EMAIL>
- Stack: Java|Python

Quick links
- Agents: `agents/` (compliance-reviewer, backend-service-builder, code-reviewer)
- Standards: `standards/`
- Stacks: `stacks/`

Agent usage and tool policy
- Use `backend-service-builder` to scaffold new services and `code-reviewer` for PR checks.
- Agents may read and write template files and generate scaffolding. They MUST NOT commit secrets or run external network commands without explicit human consent.
- Overrides: Operators may provide runtime overrides via operator-level config (see `rule-precedence.md`). Operator overrides must be auditable.

Local adapters and local development
- All local adapters are explicit. Select only implemented local adapters using typed configuration documented by the project (e.g., `MESSAGING_ADAPTER=db`, `CACHE_ADAPTER=jsonfile`).
- Local-only config files must be named `application.local.yml` or `settings.local.yaml` and excluded from production bundles.

Config sources summary
- Operator/runtime overrides → Dynamic config service (ConfigProvider) → Environment variables → Local files (dev only) → Build-time defaults.

Infra dependencies
- List expected infra (for example): Kafka, Redis, PostgreSQL, Object Storage, Secret Manager.
- For local dev use `templates/infra/docker-compose.dev.yaml` and select approved local adapters as needed.

Repository commands
- Validate structure: `tooling/scripts/validate-repo-structure.ps1`
- Create the Plan with `/create-plan`, then the milestone Implementation Plan with `/create-implementation-plan`; use `/implement-approved-plan` only after review.

Manual overrides
- To change a generated scaffold, open a PR and reference the agent output in the description. For emergency operator overrides, document the change in `config/overrides.md` and increment the override audit log.
