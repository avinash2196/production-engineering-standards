# Allowed Commands Template

Purpose
- Document the allowed CLI and operator commands for local development and production operations, including any guarded or auditable operator overrides.

Placeholders
- Local dev commands: `docker compose up -d`, `./tooling/scripts/generate-template.py`
- CI commands: `mvn -DskipTests=false test`, `pytest -q`

Operator/override commands
- Document commands that require operator-level access and must be auditable (e.g., `kubectl set image`, `az keyvault set-policy`).
- All operator commands require a documented reason and an entry in `config/overrides.md`.

Fallback toggles
- Provide commands and env variables to enable fallbacks for dev only; ensure commands include a step to disable before producing artifacts for release.

Validation
- Ensure a local developer can run `make dev` or given commands to start essentials with fallbacks enabled.
