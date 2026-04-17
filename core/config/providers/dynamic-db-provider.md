# Dynamic DB Provider

## Purpose

Specification for a database-backed or config-service-backed dynamic configuration provider. Supplies runtime-changeable values (feature flags, rate limits, kill switches, circuit breaker thresholds) without requiring service restart.

## How It Works

```
┌─────────────┐    poll (30s)    ┌──────────────────┐
│   Service    │ ◄────────────── │  Config Service / │
│  (in-memory  │                 │  Config Database   │
│   cache)     │                 └──────────────────┘
└─────────────┘
       │
       ▼
  Change listeners notified
```

1. On startup, the provider loads all dynamic config keys into an in-memory cache.
2. A background thread polls the config source at a configurable interval (default: 30 seconds).
3. When a value changes, registered change listeners are invoked with the old and new values.
4. If the config source is unreachable, the last known values are retained (stale-while-revalidate).

## Interface (implements ConfigProvider sources)

```java
// Java — implements as one source in the ConfigProvider chain
public class DynamicDbConfigSource implements ConfigSource {
    String get(String key);                          // returns current cached value
    void refresh();                                  // force refresh from source
    void addChangeListener(String key, Consumer<ConfigChangeEvent> listener);
}
```

```python
# Python
class DynamicDbConfigSource:
    def get(self, key: str) -> str | None: ...
    def refresh(self) -> None: ...
    def add_change_listener(self, key: str, callback: Callable) -> None: ...
```

## Database Schema (if DB-backed)

```sql
CREATE TABLE dynamic_config (
    config_key   VARCHAR(255) PRIMARY KEY,
    config_value TEXT NOT NULL,
    description  VARCHAR(500),
    updated_by   VARCHAR(100) NOT NULL,
    updated_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    version      INTEGER NOT NULL DEFAULT 1
);
```

- `config_key` namespaced: `<service>.rate-limit.max-requests`, `global.feature.new-checkout`.
- `version` incremented on every update — enables optimistic concurrency and change detection.
- `updated_by` records who changed the value (audit trail).

## Polling vs Push

| Approach | Pros | Cons | When to Use |
|----------|------|------|-------------|
| Polling (default) | Simple, no infrastructure dependency beyond DB | Up to poll-interval delay | Most services |
| Push (webhook/event) | Instant propagation | Requires event infrastructure | Kill switches, emergency toggles |
| Hybrid | Best of both | More complex | High-criticality services |

Default: polling at 30-second intervals. For kill switches that must propagate within seconds, add a push mechanism.

## Error Handling

- **Source unreachable:** continue serving cached values. Log WARNING every poll cycle. Emit `<service>_config_source_errors_total`.
- **Source returns invalid data:** reject the update, keep previous value, log ERROR.
- **Startup with source unreachable:** if static fallback defaults exist for all dynamic keys, start normally. If any dynamic key has no static fallback and is required, fail startup.

## Observability

- Metrics: `<service>_config_refresh_total`, `<service>_config_refresh_duration_seconds`, `<service>_config_source_errors_total`, `<service>_config_change_events_total`.
- Log each detected change at INFO: `Dynamic config changed: key=<key>, old=<old>, new=<new>, changedBy=<who>`.
- Redact values that look sensitive (containing "password", "secret", "key", "token").

## Production vs Local

- **Production:** config service (Spring Cloud Config, Consul, Azure App Configuration) or shared database.
- **Local:** dynamic provider typically disabled. Static defaults used. Developers can override via env vars or local config files for testing.

## Security

- Config database/service must require authentication.
- Write access restricted to authorized operators (not application service accounts).
- All changes logged with `updated_by` for audit.
- Values that look like secrets must be rejected — use `SecretProvider` instead.

## LLM Instructions

- When generating a feature flag or runtime-tunable value, wire it through the dynamic config source via `ConfigProvider`.
- Always provide a static fallback default so the service works without the config source.
- Generate change listeners for values that affect runtime behavior (rate limits, circuit breaker thresholds).

## Review Checklist

- [ ] Poll interval configured (default 30s).
- [ ] Stale-while-revalidate on source failure.
- [ ] Every dynamic key has a static fallback default.
- [ ] Change listeners registered for operationally important keys.
- [ ] Changes logged with old/new values (sensitive values redacted).
- [ ] Write access to config source restricted to operators.
