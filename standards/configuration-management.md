# Configuration Management Standard

## Purpose

Define how production services manage configuration safely and predictably without forcing every service to use dynamic configuration, a `ConfigProvider`, or the same configuration sources.

## Core Principle

Configuration management is mandatory. The configuration mechanism is architecture-dependent.

A service must make required runtime configuration explicit, typed or otherwise validated, deterministic, secure, and reviewable. Introduce additional abstraction only when the service actually has multiple providers, dynamic configuration, portability requirements, or a policy boundary that justifies it.

Do not invent configuration sources, dynamic configuration infrastructure, secret products, or precedence rules for sources that the service does not use.

## Required Invariants

### Typed and Validated Configuration

Configuration that can affect correctness, security, dependency behavior, or startup safety must be validated before it is used.

Prefer typed configuration models where the language/framework supports them.

Validation should cover applicable concerns such as:

- required values;
- allowed enumerations;
- ranges and timeouts;
- endpoint/URI shape;
- environment compatibility;
- mutually exclusive settings;
- local-only adapter rejection in production;
- required combinations of settings.

Fail startup when a required configuration value is missing or unsafe. Do not silently choose a production behavior that the approved configuration did not select.

### Configuration Ownership

Centralize configuration access enough to avoid scattered raw environment reads, duplicated defaults, and inconsistent parsing.

This does **not** require a `ConfigProvider` interface in every service.

A simple service may use a framework-native typed settings object as its configuration boundary. Introduce `ConfigProvider` or another abstraction when it creates a real boundary, for example:

- multiple configuration backends;
- runtime refresh/dynamic configuration;
- portability across hosting platforms;
- policy-controlled configuration retrieval;
- testing needs that cannot be handled cleanly through the existing settings boundary.

### Deterministic Precedence

When more than one configuration source is used, precedence must be explicit and deterministic.

Example sources may include:

- command-line/operator overrides;
- platform configuration;
- environment variables;
- configuration files;
- remote/dynamic configuration;
- safe code defaults.

There is no universal required precedence ordering. Document and test the order actually selected by the service/platform.

Defaults are allowed only for values whose behavior is safe and intentionally defined. Required business/security decisions must not be created through hidden defaults.

### Environment Separation

Values that legitimately differ between environments must be externalized from source code.

Do not create separate code paths for environments when configuration or composition is sufficient.

Local/test settings must not weaken production behavior silently. Local-only adapter selections must fail in production where the local-adapter standard requires a production guard.

## Secrets

Secrets are not ordinary configuration.

Production secrets must be obtained through an approved secure mechanism appropriate to the platform. Examples may include managed secret stores, workload identity, injected secret files, environment-based secret injection, or another approved mechanism.

The standard does not mandate Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, or any other product unless the project selects it.

Never:

- commit secrets to source control;
- include real secrets in example configuration;
- log secret values;
- expose secrets through diagnostics or configuration endpoints;
- use a local environment-secret adapter as an automatic production fallback.

## Dynamic Configuration

Dynamic/runtime configuration is optional and must be introduced only when an approved requirement justifies changing configuration without redeployment/restart.

When dynamic configuration is used, define:

- authoritative source;
- refresh/propagation semantics;
- validation before activation;
- behavior when the source is unavailable;
- rollback/reversion strategy where needed;
- auditability for material changes;
- consistency expectations across instances.

Do not introduce a dynamic configuration service simply because the application is enterprise-scale.

## Configuration Changes

Material configuration changes should be treated as deployable/operational changes with appropriate review and rollback evidence.

Where a change can affect correctness, security, data handling, capacity, or dependency behavior, define verification proportionate to the risk.

## Local Development

Local development should use the smallest configuration mechanism that preserves the intended boundary.

Examples:

- `.env`/environment variables for non-sensitive local values;
- local files for explicitly supported local adapters;
- test settings/fixtures for isolated tests.

Never store real production secrets in local example files.

## PDD Integration

Configuration decisions must trace to explicit requirements, repository-confirmed architecture, or an approved Plan decision.

The agent must not infer:

- a secret provider;
- a dynamic configuration product;
- a configuration refresh model;
- precedence between sources that do not yet exist;
- a default value that changes business/security behavior.

If missing configuration behavior materially affects the current milestone, ask the user and stop before planning that behavior.

RED/GREEN/REFACTOR milestones remain separate. A RED configuration milestone may add validation/startup-guard tests only. The corresponding GREEN milestone adds the minimum configuration behavior required to satisfy the approved tests.

## Review Checklist

- Required configuration is explicit.
- Risk-bearing values are typed/validated.
- Configuration access is not scattered or inconsistently parsed.
- Source precedence is documented when multiple sources exist.
- Unsafe required values fail fast.
- Local-only selections cannot reach production accidentally.
- Secrets are handled separately from ordinary configuration.
- Dynamic configuration exists only when justified.
- No framework/product default has been converted into an unstated requirement.

## Anti-Patterns

- Creating `ConfigProvider` in every service regardless of need.
- Mandatory remote configuration for a service that only needs static deployment configuration.
- Hidden production defaults for authentication, data retention, dependency endpoints, or business behavior.
- Different teams inventing conflicting precedence rules without documentation.
- Reading environment variables throughout application/domain code.
- Logging complete settings objects that may contain secrets.
- Treating local `.env` behavior as the production secret-management design.
