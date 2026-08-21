# Configuration Source Precedence

## Purpose

Define how to reason about precedence **when a project has multiple configuration sources**. This document no longer defines a universal repository-wide provider chain.

Canonical guidance: [Configuration Management](configuration-management.md).

## Rules

- Prefer the target framework/platform's documented configuration model.
- If a project intentionally combines multiple sources, document the actual order, ownership, mutability, and failure behavior.
- Security-sensitive values must not become weaker merely because a lower-trust source has higher technical precedence.
- Local-only selectors or reduced-guarantee adapters must not activate silently in production.
- Emergency/operator overrides, if supported, need authorization and auditability appropriate to their risk.
- Dynamic configuration, if supported, needs explicit version/concurrency/rollback semantics and safe source-failure behavior.
- Secret values use the project's approved secret mechanism. A `SecretProvider` boundary is optional and should be used only when the project adopts it.

## Example Only

A platform **might** combine deployment/operator overrides, environment variables, profile files, and build defaults. Another platform may use a completely different order. Do not copy an example order into an implementation without confirming the stack's actual behavior.

## Review Checklist

- [ ] All active sources are identified from the real project/deployment model.
- [ ] Their precedence is documented or inherited from a cited platform convention.
- [ ] Mutable sources have defined validation/concurrency/failure behavior where applicable.
- [ ] Security-sensitive values cannot be downgraded through an unintended override.
- [ ] Local-only values are blocked or unavailable in production as designed.
