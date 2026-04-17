# File Provider

## Purpose

Local file-based configuration provider. Reads structured config from YAML, properties, or TOML files. Primarily used for environment-specific config profiles, connection pool settings, logging configuration, and other structured values that don't change per-deployment.

## Resolution Behavior

- Files loaded at startup and cached in memory. Not reloaded at runtime (static config).
- Multiple files can be layered: base config + environment-specific overlay.
- Returns `null`/`None` for missing keys (falls through to build defaults).

## Priority in Config Chain

```
operator overrides → dynamic config → env-provider → ★ file-provider ★ → build defaults
                                                      (priority 4)
```

File-based config is overridden by environment variables, dynamic config, and operator overrides.

## File Structure Convention

### Java (Spring Boot)

```
src/main/resources/
├── application.yml              # base config (all environments)
├── application-local.yml        # local development overrides
├── application-staging.yml      # staging overrides
└── application-production.yml   # production overrides
```

Active profile selected via `SPRING_PROFILES_ACTIVE=local|staging|production`.

### Python (FastAPI)

```
config/
├── base.toml                    # base config (all environments)
├── local.toml                   # local development overrides
├── staging.toml                 # staging overrides
└── production.toml              # production overrides
```

Active config selected via `APP_ENV=local|staging|production`.

## Layering Rules

1. Load base config file first.
2. Load environment-specific overlay on top (overrides matching keys).
3. Result is the merged config.

```yaml
# application.yml (base)
server:
  port: 8080
database:
  pool:
    max-size: 10
    min-idle: 2

# application-production.yml (overlay)
database:
  pool:
    max-size: 50
    min-idle: 10
```

Production result: `server.port=8080`, `database.pool.max-size=50`, `database.pool.min-idle=10`.

## What Belongs in Config Files

| Suitable | Not Suitable |
|----------|-------------|
| Connection pool settings | Secrets (use `SecretProvider`) |
| Logging configuration | Per-deployment values like URLs (use env vars) |
| Default timeouts and retry policies | Values needing runtime change (use dynamic provider) |
| Structured/nested configuration | |
| Framework-specific settings | |

## Java Implementation

```java
public class FileConfigSource implements ConfigSource {
    private final Map<String, String> flattenedProperties;

    public FileConfigSource(String profile) {
        Properties base = loadYaml("application.yml");
        Properties overlay = loadYaml("application-" + profile + ".yml");
        base.putAll(overlay); // overlay wins
        this.flattenedProperties = flatten(base);
    }

    @Override
    public String get(String key) {
        return flattenedProperties.get(key);
    }

    @Override
    public int priority() {
        return 4;
    }
}
```

## Python Implementation

```python
import tomllib
from pathlib import Path

class FileConfigSource:
    def __init__(self, env: str = "local"):
        base = self._load("config/base.toml")
        overlay = self._load(f"config/{env}.toml")
        self._config = {**base, **overlay}

    def get(self, key: str) -> str | None:
        parts = key.split(".")
        value = self._config
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return None
        return str(value) if value is not None else None

    @property
    def priority(self) -> int:
        return 4
```

## Security Considerations

- Config files must not contain secrets. If a YAML file has a key like `database.password`, it must be removed and the value sourced from `SecretProvider`.
- Config files are committed to version control. Treat their contents as potentially public.
- Environment-specific files may contain internal URLs — ensure the repo access controls are appropriate.

## Anti-Patterns

- **Secrets in config files:** use `SecretProvider` for credentials, keys, tokens.
- **Environment-specific logic in code:** use config file overlays, not `if (env == "prod")`.
- **Reloading config files at runtime:** file provider is for static config. Use dynamic provider for runtime changes.
- **Single monolithic config file:** split base and environment overlays for clarity.

## LLM Instructions

- When generating structured configuration (pool sizes, timeouts, logging), use config files.
- Generate both base and environment-specific overlay files.
- Never put secrets in generated config files.
- Use the stack-appropriate format: YAML for Spring Boot, TOML or YAML for Python.

## Review Checklist

- [ ] No secrets in config files.
- [ ] Base + environment overlay structure used.
- [ ] Config files committed to version control.
- [ ] Complex/nested values in config files, simple per-deployment values in env vars.
- [ ] Environment profile activation documented.
