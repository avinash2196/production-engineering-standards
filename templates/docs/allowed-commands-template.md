# Allowed Commands Template
<!--
  HOW TO USE:
  Copy to docs/allowed-commands.md (or config/allowed-commands.md).
  Fill in each section. This file governs what agents and operators may run.
  See: playbooks/create-doc.md for full process.
-->

# Allowed Commands: [SERVICE / REPO NAME]

**Owner:** [Team]  
**Last updated:** YYYY-MM-DD

## Local Development Commands

Any developer may run these. No approval required.

```bash
# Install dependencies
./mvnw dependency:resolve          # Java
pip install -r requirements.txt    # Python

# Start local stack (Docker required)
docker compose -f templates/infra/docker-compose.dev.yaml up -d

# Start service with fallbacks (no Docker needed)
MESSAGING_ADAPTER=db CACHE_ADAPTER=jsonfile STORAGE_ADAPTER=local SECRET_ADAPTER=env \
  ./mvnw spring-boot:run -Dspring-boot.run.profiles=local
# or
MESSAGING_ADAPTER=db CACHE_ADAPTER=jsonfile STORAGE_ADAPTER=local SECRET_ADAPTER=env \
  uvicorn src.<service>.main:app --reload --port 8000

# Run tests
./mvnw test                        # Java unit tests
pytest                             # Python unit tests
./mvnw test -Dgroups=integration   # Java integration tests (requires Docker)
pytest -m integration              # Python integration tests (requires Docker)

# Validate repo structure
pwsh tooling/scripts/validate-repo-structure.ps1

# Generate a new service scaffold
python tooling/scripts/validate-repository.py --stack [java|python] --name <service-name>
```

## CI Commands (automated, no human approval)

Run by the CI pipeline on every PR and merge.

```bash
./mvnw -DskipTests=false verify    # Java: compile + test + package
pytest -q --tb=short               # Python: test suite
./mvnw spotbugs:check              # Java: static analysis
ruff check . && black --check .    # Python: linting + format check
trivy image <image>:<tag>          # Container vulnerability scan
```

## Operator Commands (requires approval + audit entry)

These commands change production state. They MUST be:
1. Approved by the tech lead or on-call engineer.
2. Logged in `config/overrides.md` with reason, timestamp, and operator name.

```bash
# Force-restart a running pod / task
kubectl rollout restart deployment/<service-name> -n <namespace>

# Override a feature flag in production
vault kv put secret/prod/<service-name>/feature-flags <key>=<value>

# Grant temporary elevated access
az keyvault set-policy --name <vault> --object-id <id> --secret-permissions get list

# Manual database migration (emergency only)
psql $DATABASE_URL -f migrations/<NNN>-emergency-fix.sql

# Rotate a secret
vault kv patch secret/prod/<service-name> <key>=<new-value>
```

## Fallback Toggle Commands

Fallbacks are **development-only**. Never set these in production.

```bash
# Enable all fallbacks (dev/test only)
export MESSAGING_ADAPTER=db
export CACHE_ADAPTER=jsonfile
export STORAGE_ADAPTER=local
export SECRET_ADAPTER=env

# Disable before building release artifacts
unset MESSAGING_ADAPTER CACHE_ADAPTER STORAGE_ADAPTER SECRET_ADAPTER
```

## Forbidden Commands

Agents and automated pipelines MUST NOT run these:

| Command | Reason |
|---------|--------|
| `git push --force`, `git reset --hard HEAD~N` on main | Destroys audit history |
| `kubectl delete namespace <prod-ns>` | Destroys production workloads |
| `DROP TABLE`, `DROP DATABASE` without migration | Irreversible data loss |
| Any command with raw production secrets in args | Secrets appear in shell history / logs |
| `curl` or `wget` to external URLs in CI | Prevents supply-chain attacks |

## References

- [standards/agent-execution.md](../../standards/agent-execution.md)
- [standards/security/security-standards.md](../../standards/security/security-standards.md)
- [config/overrides.md](../../config/overrides.md) — operator override audit log

