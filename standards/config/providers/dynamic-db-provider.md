# Dynamic Configuration Source

## Purpose

Reference pattern for runtime-changeable configuration **when requirements justify dynamic configuration**. Typical candidates include kill switches, operational thresholds, or feature controls that must change without deployment.

Dynamic configuration is optional. Do not introduce a database, config service, polling loop, listener framework, or `ConfigProvider` solely because this reference exists.

The canonical policy is [Configuration Management](../../configuration-management.md).

## Design Decisions to Resolve

Before implementation, determine from requirements and platform capabilities:

- which keys are actually dynamic;
- required propagation latency;
- source of truth and ownership;
- polling, push, streaming, or platform-native refresh mechanism;
- startup behavior if the source is unavailable;
- safe behavior for stale or missing values;
- authorization and audit requirements for changes;
- validation/versioning/concurrency behavior.

Do not invent a universal 30-second poll interval or stale-value policy.

## Example Model

If a database is deliberately selected, a versioned record can support optimistic concurrency and change detection:

```sql
CREATE TABLE dynamic_config (
    config_key   VARCHAR(255) PRIMARY KEY,
    config_value TEXT NOT NULL,
    updated_by   VARCHAR(100),
    updated_at   TIMESTAMP NOT NULL,
    version      INTEGER NOT NULL
);
```

This schema is illustrative, not mandatory. Use the project's database conventions, audit model, and data types.

## Failure Behavior

Define behavior per key/capability:

- retain a last-known value only when stale operation is safe;
- use a static fallback only when it is semantically valid;
- fail startup or disable the capability when a required value has no safe fallback;
- reject invalid updates and preserve the last valid state when appropriate.

## Observability

Expose enough evidence to diagnose refresh failures and stale state using the project's existing logging/metrics/tracing conventions. Never log sensitive configuration values. Prefer recording key identifiers, versions, source status, and outcomes.

## Security

- Authenticate and authorize access to the selected source according to platform policy.
- Restrict write access according to operational ownership.
- Treat secret values as secrets; do not move them into a dynamic-config store unless that store is the approved secret mechanism.
- Audit changes when required by project/security/compliance policy.

## LLM Instructions

- Confirm that runtime mutation is required before designing dynamic configuration.
- Derive propagation/fallback behavior from requirements; do not assume polling or a fixed interval.
- Prefer an existing platform/configuration service over inventing infrastructure.
- Do not log old/new values if they may be sensitive.

## Review Checklist

- [ ] Dynamic configuration is justified by an explicit requirement.
- [ ] Propagation mechanism and latency target are documented.
- [ ] Startup/source-failure behavior is defined per affected capability.
- [ ] Invalid updates cannot silently corrupt runtime behavior.
- [ ] Authorization/audit controls match the selected platform and risk.
- [ ] Diagnostics expose source health without leaking values.
