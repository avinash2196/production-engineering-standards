# Allowed Commands Template
<!--
  HOW TO USE:
  Copy to docs/allowed-commands.md (or an equivalent project-controlled location).
  Keep only commands that actually exist in the target repository.
  This file documents agent/operator command boundaries; it does not grant production authorization.
-->

# Allowed Commands: [SERVICE / REPO NAME]

**Owner:** [Team]  
**Last updated:** YYYY-MM-DD

## Local Development Commands

Examples below must be adapted to the target repository.

```bash
# Install dependencies
./mvnw dependency:resolve          # Maven wrapper project
poetry install                     # Poetry-managed Python project

# Run tests
./mvnw test
poetry run pytest

# Python lint/format checks when Ruff is configured
poetry run ruff check .
poetry run ruff format --check .
```

If the service implements approved local adapters, document the exact selectors it supports. Do not invent adapters that are not implemented and tested.

## CI Commands

List only checks configured in the target project, for example:

```bash
./mvnw -DskipTests=false verify
poetry run pytest -q
poetry run ruff check .
poetry run ruff format --check .
```

Add static analysis, secret scanning, dependency scanning, container scanning, and contract/integration tests only when the corresponding tool is actually configured.

## Operator Commands

Production-changing commands require the target organization's approved access-control, change-management, and audit process. Document those project-specific commands here rather than copying generic credentials, vault paths, namespaces, or approval roles.

## Local-Adapter Commands

Local-only adapter values may be documented for development/test environments. Production configuration must use approved production values, and startup validation must reject local-only selections.

```bash
export MESSAGING_ADAPTER=db
export CACHE_ADAPTER=jsonfile
export STORAGE_ADAPTER=local
export SECRET_ADAPTER=env
```

Use only the values implemented by the target service.

## Forbidden Command Categories

Agents and automated pipelines must not perform destructive or unapproved actions, including:

- force-pushing protected branches or rewriting protected history;
- destructive production namespace/database operations outside an approved change procedure;
- passing raw production secrets in command arguments or logs;
- arbitrary executable downloads or execution from unapproved sources.

CI downloads must use approved sources and pinned/versioned artifacts where practical.

## References

- [Agent Execution](../../standards/agent-execution.md)
- [Security Standards](../../standards/security/security-standards.md)
