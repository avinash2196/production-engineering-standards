# Configuration Model

> Parent standard: [Configuration Management](../configuration-management.md)

## Purpose

Provide a decision model for configuration without requiring every service to use the same sources, provider abstraction, precedence chain, or dynamic-configuration infrastructure.

## Configuration Categories

A service may have one or more of these categories:

| Category | Description | Typical examples |
|---|---|---|
| Static/deployment configuration | Values selected for a deployment and normally changed through restart/redeploy | endpoints, ports, pool bounds, feature settings |
| Dynamic/runtime configuration | Values intentionally changeable without restart because an approved use case requires it | kill switches, selected runtime tuning, feature flags |
| Secrets/credentials | Sensitive values or credentials requiring protected delivery/access | passwords, API credentials, private keys, tokens |

The categories help reason about validation and ownership; they do not require a `ConfigProvider` or `SecretProvider` interface in every adopting service.

## Source Selection

Use only sources the approved project/runtime actually needs. Examples include:

- framework configuration;
- environment variables or platform-injected values;
- command-line/operator overrides;
- configuration files;
- remote/dynamic configuration;
- managed secret injection/access;
- safe code defaults.

When multiple sources exist, document and test the actual precedence. There is no repository-wide mandatory precedence order.

## Typed Validation

Validate configuration that can affect correctness, security, dependency behavior, or startup safety before it is used.

Applicable checks may include required values, enums, ranges, URI shape, mutually exclusive settings, required combinations, and environment guards for local-only adapters.

Do not hide a required business/security choice behind an undocumented default.

## Optional Capability Boundaries

The repository provides [ConfigProvider](../../contracts/ConfigProvider.md) and [SecretProvider](../../contracts/SecretProvider.md) as reference capability boundaries.

Adopt them when they create a real boundary, such as multiple backends, portability, runtime refresh, policy-controlled retrieval, or testing needs. A simple service may instead use a framework-native typed configuration object and an approved runtime secret mechanism.

## Dynamic Configuration

Dynamic configuration is optional. Introduce it only when an approved requirement justifies runtime changes without redeploy/restart.

When used, define:

- authoritative source;
- validation before activation;
- propagation/consistency semantics;
- unavailable-source behavior;
- rollback/reversion behavior where required;
- auditability for material changes.

A polling interval, storage technology, or push mechanism is an implementation decision, not a repository-wide default.

## Secrets

Secrets are not ordinary configuration. Production credentials must use the project's approved secure delivery/access mechanism and must never be committed, logged, or exposed through diagnostics.

If a project adopts this repository's `SecretProvider` capability, use that boundary consistently. The `SECRET_ADAPTER=env` local reference is local-only and must not silently activate in production.

## Local Development

Use the smallest local configuration mechanism that preserves the intended boundary. Stack-specific examples may include `.env.local`, Spring `application-local.yml`, container configuration, or explicit local-adapter selectors.

Do not copy production credentials or sensitive production data into local configuration.

## Anti-Patterns

- Introducing a dynamic configuration service without a requirement.
- Requiring `ConfigProvider` only for architectural symmetry.
- Scattering duplicate parsing/default logic across the codebase.
- Undocumented precedence between multiple sources.
- Treating secrets as ordinary committed configuration.
- Letting local-only selectors become production fallbacks.

## LLM Instructions

- Determine which configuration categories and sources the service actually uses before proposing a mechanism.
- Do not invent dynamic configuration, provider chains, refresh intervals, or precedence rules.
- Prefer typed validation for risk-bearing values.
- Use `ConfigProvider`/`SecretProvider` only when the project has adopted those capability boundaries or the current design justifies them.

## Review Checklist

- [ ] Only required configuration sources are present.
- [ ] Risk-bearing values are validated before use.
- [ ] Multi-source precedence is explicit and deterministic where applicable.
- [ ] Dynamic configuration exists only for an approved need.
- [ ] Secret handling uses the approved secure mechanism.
- [ ] Local-only configuration cannot silently weaken production behavior.
