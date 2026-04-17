# Env Provider

## Purpose

Environment variable configuration provider. Reads values from the OS environment at startup. This is the primary mechanism for per-deployment static configuration (database URLs, external service endpoints, feature toggles, port numbers).

## Resolution Behavior

- Reads `System.getenv(key)` (Java) or `os.environ.get(key)` (Python).
- Keys are case-sensitive. Convention: `UPPER_SNAKE_CASE` for env vars.
- Mapping to application keys: `order-service.max-retries` → `ORDER_SERVICE_MAX_RETRIES`.
- Returns `null`/`None` if the key is not set (falls through to next provider in chain).

## Priority in Config Chain

```
operator overrides → dynamic config → ★ env-provider ★ → file-provider → build defaults
                                      (priority 3)
```

Environment variables override file-based config but are overridden by dynamic config and operator overrides.

## Naming Convention

| Application Key | Environment Variable |
|----------------|---------------------|
| `database.url` | `DATABASE_URL` |
| `server.port` | `SERVER_PORT` |
| `log.level` | `LOG_LEVEL` |
| `order-service.max-retries` | `ORDER_SERVICE_MAX_RETRIES` |
| `feature.new-checkout.enabled` | `FEATURE_NEW_CHECKOUT_ENABLED` |

Rules:
- Replace `.` and `-` with `_`.
- Convert to uppercase.
- Prefix with service name for service-specific keys to avoid collisions.

## What Belongs in Env Vars

| Suitable | Not Suitable |
|----------|-------------|
| Database connection URLs | Secrets (use `SecretProvider`) |
| External service endpoints | Complex structured config (use file-provider) |
| Port numbers | Large config blocks (use file-provider) |
| Log level | Values needing runtime change (use dynamic provider) |
| Fallback toggles (`FALLBACK_KAFKA=db`) | Multi-line values |
| Simple feature toggles (static) | |

## Java Implementation

```java
public class EnvConfigSource implements ConfigSource {
    @Override
    public String get(String key) {
        String envKey = key.replace(".", "_").replace("-", "_").toUpperCase();
        return System.getenv(envKey);
    }

    @Override
    public int priority() {
        return 3; // after operator overrides (1) and dynamic (2)
    }
}
```

## Python Implementation

```python
import os

class EnvConfigSource:
    def get(self, key: str) -> str | None:
        env_key = key.replace(".", "_").replace("-", "_").upper()
        return os.environ.get(env_key)

    @property
    def priority(self) -> int:
        return 3
```

## Validation at Startup

Required env vars should be validated at startup:

```java
// Java
List<String> required = List.of("DATABASE_URL", "SERVER_PORT");
for (String key : required) {
    if (System.getenv(key) == null) {
        throw new IllegalStateException("Required env var missing: " + key);
    }
}
```

## Security Considerations

- **Never put secrets in env vars in production.** Use `SecretProvider` with Vault/Key Vault.
- Env vars may be visible in process listings, container inspection, and crash dumps.
- `FALLBACK_SECRETS=env` is acceptable only for local development.
- Log which env vars are present at startup (names only, never values for sensitive-looking keys).

## LLM Instructions

- When generating deployment config, use env vars for per-deployment values (URLs, ports, toggles).
- Never generate code that puts secrets in env vars for production.
- Use the naming convention above (UPPER_SNAKE_CASE).
- Generate startup validation for any required env var.

## Review Checklist

- [ ] Env var names follow UPPER_SNAKE_CASE convention.
- [ ] Required env vars validated at startup.
- [ ] No secrets stored as env vars in production.
- [ ] Env var values not logged (only names logged at startup).
