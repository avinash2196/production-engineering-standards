# ConfigProvider

## Purpose

Define the capability interface for resolving configuration values with an explicit precedence hierarchy, refresh semantics, and observability. Services depend on this abstraction for all non-secret configuration.

## Interface Contract

- `get(key)` → returns the current value for the key, or `null`/`None` if not found.
- `get(key, defaultValue)` → returns the value or the provided default.
- `getRequired(key)` → returns the value or throws `ConfigNotFoundException`. Use for mandatory configuration.
- `getAs(key, type)` → returns the value cast to the specified type (int, bool, duration, list).
- `addChangeListener(key, callback)` → registers a listener invoked when the value changes (dynamic config support).

## Configuration Precedence

Values are resolved in this order. First match wins:

| Priority | Source | Example | Mutable at Runtime |
|----------|--------|---------|-------------------|
| 1 (highest) | Operator overrides | Feature flags, kill switches | Yes |
| 2 | Dynamic config | Config service, database-backed config | Yes |
| 3 | Environment variables | `DATABASE_URL`, `LOG_LEVEL` | No (restart required) |
| 4 | Local config files | `application.yml`, `.env` | No (restart required) |
| 5 (lowest) | Build defaults | Hardcoded in code | No |

## Required Semantics

- **Precedence is strict.** A value from a higher-priority source always overrides a lower one.
- **Dynamic refresh:** sources at priority 1-2 may change at runtime. The provider must poll or subscribe for changes and notify registered listeners.
- **Refresh interval:** configurable, default 30 seconds for polled sources.
- **Type safety:** the provider must support type coercion for common types (string, int, boolean, duration, list) with clear error messages on coercion failure.
- **Namespace isolation:** keys should be prefixed by service name to avoid collisions in shared config stores (e.g., `order-service.max-retries`).

## Error Handling

- `ConfigNotFoundException` on `getRequired` when key is missing → fail fast at startup for mandatory config.
- Type coercion failure → throw `ConfigTypeMismatchException` with key name, expected type, and actual value.
- Config source unavailable → fall through to next source in precedence. Log a WARNING. Never silently use defaults without logging.

## Observability

- Metrics: `<service>_config_access_total`, `<service>_config_refresh_total`, `<service>_config_errors_total`, `<service>_config_change_events_total`.
- Log config changes at INFO level: key name, old value, new value (redact if the value looks sensitive).
- Emit a metric on each dynamic refresh cycle, even if no values changed.

## Production vs Local Differences

- **Production:** all 5 precedence levels active. Dynamic config via centralized config service (Spring Cloud Config, Consul, Azure App Configuration, etc.).
- **Local:** environment variables and local config files only (levels 3-5). Operator overrides and dynamic config typically not available locally.
- No separate local-adapter toggle for config — it works the same way everywhere, just with fewer sources locally.

## Java Example

```java
public interface ConfigProvider {
    String get(String key);
    String get(String key, String defaultValue);
    String getRequired(String key);
    <T> T getAs(String key, Class<T> type);
    void addChangeListener(String key, Consumer<ConfigChangeEvent> listener);
}

@Component
public class HierarchicalConfigProvider implements ConfigProvider {
    private final List<ConfigSource> sources; // ordered by precedence
    
    @Override
    public String get(String key) {
        return sources.stream()
            .map(source -> source.get(key))
            .filter(Objects::nonNull)
            .findFirst()
            .orElse(null);
    }
}
```

## Python Example

```python
class ConfigProvider(Protocol):
    def get(self, key: str, default: str | None = None) -> str | None: ...
    def get_required(self, key: str) -> str: ...
    def get_as(self, key: str, type_: type[T]) -> T: ...
    def add_change_listener(self, key: str, callback: Callable[[ConfigChangeEvent], None]) -> None: ...
```

## Relationship to SecretProvider

- `ConfigProvider` handles non-sensitive configuration. Secrets (credentials, API keys, encryption keys) must use `SecretProvider`.
- A config value that looks like a secret (contains "password", "key", "token") should trigger a warning in code review.
- See [SecretProvider.md](SecretProvider.md).

## Anti-Patterns

- **Hardcoded config in business logic:** all tuneable values must come from `ConfigProvider`.
- **Secrets in ConfigProvider:** use `SecretProvider` for sensitive values.
- **No default for optional config:** optional config should always have a sensible default.
- **Ignoring precedence:** never skip the precedence hierarchy by reading environment variables directly.

## LLM Instructions

- When a service needs a configurable value, use `ConfigProvider.get()` or `getRequired()`, never hardcode.
- Ask the user if the value is a secret before choosing ConfigProvider vs SecretProvider.
- Generate change listeners for values that may be toggled at runtime (feature flags, rate limits).
- Document the expected config keys in the service README.

## Review Checklist

- [ ] All configurable values resolved via `ConfigProvider`, not hardcoded.
- [ ] Mandatory config uses `getRequired` with fail-fast at startup.
- [ ] Sensitive values use `SecretProvider`, not `ConfigProvider`.
- [ ] Dynamic config values have change listeners where appropriate.
- [ ] Config keys namespaced by service name.
- [ ] Type coercion used instead of manual string parsing.
