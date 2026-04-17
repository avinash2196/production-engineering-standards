# Configuration Model

## Purpose

Define the three categories of configuration, their resolution order, and the boundaries between them. Every configurable value in a service falls into exactly one category. This model drives which provider is used and which security controls apply.

## Configuration Categories

| Category | Description | Provider | Mutable at Runtime | Examples |
|----------|-------------|----------|-------------------|----------|
| **Static config** | Values fixed per deployment. Change requires restart or redeployment. | `ConfigProvider` (env, file, build defaults) | No | Database host, service port, log level, feature toggles (static) |
| **Dynamic config** | Values that may change at runtime without restart. Polled or pushed from a config service. | `ConfigProvider` (dynamic-db, operator overrides) | Yes | Rate limits, circuit breaker thresholds, feature flags (dynamic), kill switches |
| **Secrets** | Credentials, API keys, encryption keys, tokens. Highest security controls. | `SecretProvider` | Yes (rotation) | DB password, API key, JWT signing key, TLS certificates |

## Resolution Order

When `ConfigProvider.get(key)` is called, sources are checked in this order. First match wins:

```
1. Operator overrides      (dynamic, highest priority)
2. Dynamic config service   (dynamic)
3. Environment variables    (static, per-deployment)
4. Local config files       (static, per-environment)
5. Build defaults           (static, compiled in)
```

Secrets are **never** resolved through `ConfigProvider`. If a key is a secret, use `SecretProvider` exclusively.

See [ConfigProvider.md](../abstractions/ConfigProvider.md) for the full interface contract.

## Static Configuration

### Characteristics
- Set at deployment time via environment variables, config files, or build defaults.
- Requires process restart to change.
- Validated at startup — missing required static config fails startup immediately.

### Provider Chain
```
env-provider → file-provider → build defaults
```

### Guidelines
- Use environment variables for per-deployment values (database URL, external service endpoints).
- Use config files for structured configuration (logging format, connection pool sizes).
- Use build defaults for sensible fallbacks that rarely change.

See: [env-provider.md](providers/env-provider.md), [file-provider.md](providers/file-provider.md)

## Dynamic Configuration

### Characteristics
- Changeable at runtime without restart or redeployment.
- Polled from a config service or database at a regular interval (default: 30s).
- Change listeners notify the application when a value updates.
- Used for operational controls: rate limits, feature flags, kill switches, circuit breaker tuning.

### Provider
```
operator overrides → dynamic-db-provider
```

### Guidelines
- Only values that genuinely need runtime change should be dynamic. Don't make everything dynamic.
- Every dynamic config key must have a fallback static default so the service starts even if the config service is unavailable.
- Log every dynamic config change at INFO level with old and new values.
- Emit `<service>_config_change_events_total` metric on each change.

See: [dynamic-db-provider.md](providers/dynamic-db-provider.md)

## Secrets

### Characteristics
- Resolved exclusively via `SecretProvider`, never via `ConfigProvider` or environment variables in production.
- Cached with short TTL (default 5 min). Rotation supported without restart.
- Never logged, never in error messages, never in metrics.
- In local development, `FALLBACK_SECRETS=env` allows env-var resolution.

See: [SecretProvider.md](../abstractions/SecretProvider.md), [vault-provider.md](providers/vault-provider.md)

## Deciding the Category

```
Is the value a credential, key, or token?
  → Yes → Secret (use SecretProvider)
  → No →
      Does it need to change at runtime without restart?
        → Yes → Dynamic config
        → No → Static config
```

## Environment-Specific Config Structure

Each environment has its own config layer:

| Environment | Static Sources | Dynamic Sources | Secrets Source |
|-------------|---------------|----------------|----------------|
| Local dev | `.env.local`, `application-local.yml` | None (static defaults used) | `FALLBACK_SECRETS=env` |
| Staging | Env vars from deployment | Config service (staging) | Vault (staging) |
| Production | Env vars from deployment | Config service (production) | Vault (production) |

See: [config-per-env patterns](#) (documented per stack guide)

## Anti-Patterns

- **Secrets in ConfigProvider:** credentials must use `SecretProvider`.
- **Everything dynamic:** only operational controls need runtime change. Over-dynamism adds complexity.
- **No defaults:** every optional config should have a sensible build default.
- **Config scattered in code:** all configurable values centralized through `ConfigProvider`.
- **Environment-specific logic in code:** use per-environment config files, not `if (env == "prod")`.

## LLM Instructions

- When generating configurable values, classify each as static, dynamic, or secret.
- Use `ConfigProvider.get()` for static and dynamic config. Use `SecretProvider.getSecret()` for secrets.
- Generate startup validation for all required static config.
- Ask the user whether a value needs runtime change before making it dynamic.

## Review Checklist

- [ ] Every configurable value classified as static, dynamic, or secret.
- [ ] Secrets resolved via `SecretProvider`, not `ConfigProvider`.
- [ ] Required static config validated at startup with fail-fast.
- [ ] Dynamic config has static fallback defaults.
- [ ] No environment-specific branching in code — config files per environment instead.
