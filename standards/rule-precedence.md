# Rule Precedence

Defines the precedence and separation between configuration sources, secrets, and dynamic overrides.

Precedence (highest → lowest):
1. Runtime overrides (operator-supplied, e.g., Kubernetes `--set` or operator API)
2. Dynamic configuration service (ConfigProvider with versioning/roll-back)
3. Environment variables
4. Local config files (development only)
5. Built-time defaults / templates

Notes:
- Secrets must be resolved via `SecretProvider` which prefers a secret manager (cloud) and falls back to environment variables only when explicitly enabled for dev.
- Dynamic config updates must include a version or change token to prevent accidental rollbacks; services should support safe refresh with graceful degradation.
- Configuration that affects security posture (e.g., selecting an in-memory local cache adapter) requires explicit environment toggles and CI gating; never enabled silently.

Override rules:
- Operator-level overrides for emergency fixes must be auditable and limited to a narrow set of keys.
- Dynamic config may be used for feature flags and non-sensitive tuning; secrets and access controls are not allowed in dynamic config unless encrypted and access-controlled.
