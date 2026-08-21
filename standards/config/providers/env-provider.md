# Environment Configuration Source

## Purpose

Reference pattern for reading configuration from environment variables **when the project's deployment model uses environment variables**. This document is not a repository-wide requirement to introduce a `ConfigProvider` abstraction or to place every deployment value in environment variables.

The canonical policy is [Configuration Management](../../configuration-management.md).

## When to Use

Environment variables are useful for simple deployment-specific values supplied by the runtime or orchestrator, for example:

- service endpoints;
- ports;
- feature/configuration selectors that are static for the process lifetime;
- adapter selectors used by an approved local/deployment strategy.

Use the platform/framework's native configuration mechanism unless the project has an explicit reason for a custom abstraction.

## Naming

Follow the runtime/framework convention. `UPPER_SNAKE_CASE` is a common portable convention when direct environment-variable names are owned by the application.

Example mappings, **only if the application owns this mapping**:

| Application key | Environment variable |
|---|---|
| `database.url` | `DATABASE_URL` |
| `server.port` | `SERVER_PORT` |
| `feature.new-checkout.enabled` | `FEATURE_NEW_CHECKOUT_ENABLED` |

Do not invent a second naming layer when Spring Boot, a deployment platform, or another framework already defines a supported binding convention.

## Precedence

If several configuration sources are used, document and test their precedence. Do not assume this repository's historical provider-chain order. Prefer framework/platform-native precedence unless requirements justify overriding it.

## Secrets

Do not treat environment variables as the default production secret-management mechanism. Use the organization's approved secret mechanism for the target environment. If a project deliberately injects secrets through environment variables, that decision must come from the approved platform/security model rather than from this reference document.

`SECRET_ADAPTER=env` in the repository examples is a **local-development adapter selector**, not a production recommendation.

## Validation

Validate required configuration early enough to fail clearly and safely. Validation should report the missing/invalid key without logging sensitive values.

## Example

```java
String endpoint = System.getenv("PAYMENTS_ENDPOINT");
if (endpoint == null || endpoint.isBlank()) {
    throw new IllegalStateException("Required configuration missing: PAYMENTS_ENDPOINT");
}
```

This direct read is sufficient for a small application. Introduce a `ConfigProvider` or typed configuration boundary only when it improves the design or is already part of the project architecture.

## LLM Instructions

- First inspect the target stack and deployment model.
- Prefer existing framework/platform configuration support.
- Do not create a custom `ConfigProvider` solely because this repository contains provider examples.
- Do not invent environment-variable precedence.
- Never log secret/configuration values merely to prove they were loaded.

## Review Checklist

- [ ] Environment variables are actually supported by the target runtime/deployment model.
- [ ] Naming follows the existing stack/platform convention.
- [ ] Required values are validated with safe error messages.
- [ ] Precedence is documented when multiple sources exist.
- [ ] Secret handling follows the approved security/platform mechanism.
