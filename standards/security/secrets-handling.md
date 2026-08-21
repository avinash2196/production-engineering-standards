# Secrets Handling

> Parent standard: [Security Engineering](security-standards.md)

## Purpose

Define safe outcomes for storing, delivering, accessing, rotating, and disposing of credentials and other secrets without mandating one vendor, injection method, rotation interval, or abstraction for every service.

## Mandatory Outcomes

### No Secrets in Source or Artifacts

Do not place real secrets in:

- source code;
- committed configuration/examples;
- container image layers or build arguments;
- logs, metrics, traces, error responses, or URLs;
- documentation/screenshots/test fixtures that are shared broadly.

CI/CD definitions should reference the platform's protected secret mechanism rather than contain values directly.

### Approved Production Delivery/Access

Production credentials must come from an approved secure mechanism appropriate to the platform and threat model. Examples include managed secret stores, workload identity, injected secret files, protected environment injection, certificate/key services, or another approved mechanism.

This repository provides `SecretProvider` as an optional capability boundary. Use it when the adopting project has selected that abstraction or needs multiple secret backends/testability/portability. Do not wrap a platform-native mechanism solely to satisfy repository symmetry.

The repository's `SECRET_ADAPTER=env` local adapter is explicitly local-only and must not become an automatic production fallback.

### Least Privilege and Scope

- Give each workload only the credentials/permissions it needs.
- Avoid shared privileged credentials when separate identities are practical.
- Scope secrets by environment and purpose according to the platform model.
- Protect emergency access through the organization's approved break-glass process when one exists.

### Rotation and Revocation

Rotation requirements come from credential lifetime, platform capability, vendor constraints, incident risk, and organization policy. Do not invent universal 5-minute cache TTLs or 90/180/365-day schedules.

For a rotatable secret, define as applicable:

- source of truth;
- refresh/reload behavior;
- overlap/dual-key strategy when consumers require it;
- revocation timing;
- failure behavior when refresh fails;
- operational evidence that rotation works.

Prefer short-lived identity/credentials where the approved platform supports them and doing so meaningfully reduces risk.

### Caching

Cache secrets in process only when the selected secret mechanism/client requires or benefits from it. Keep cache lifetime bounded according to provider semantics, rotation requirements, availability needs, and exposure risk. Never cache secrets in an external general-purpose cache merely for convenience.

## Local Development

Use synthetic/local credentials only. `.env.local` or similar files may be used when explicitly supported by the project; such files must be excluded from version control and must never contain production credentials.

## Incident Response

When a credential may be compromised, follow the organization's security incident process. Typical technical actions include revocation/rotation, exposure-scope investigation, removal from logs/artifacts, and validation of the affected trust boundary. Do not invent notification roles or timelines not established by policy.

## Anti-Patterns

- Hardcoded or committed credentials.
- Logging/printing secret values.
- Using the local environment-secret adapter as production degradation.
- Universal rotation schedules copied without policy/platform evidence.
- Requiring runtime-refresh architecture for credentials that are intentionally deployment-scoped.
- Claiming a secret is safe merely because it is in an environment variable; evaluate how the production platform protects and exposes that environment.

## LLM Instructions

- Identify the project's approved secret-delivery/access mechanism before generating product-specific code.
- Use `SecretProvider` only when the project has adopted that capability boundary or the design justifies it.
- Never generate real credentials or examples that look usable.
- Do not invent rotation intervals, cache TTLs, vault products, or CI scanners.

## Review Checklist

- [ ] No real secrets are committed or exposed through telemetry/artifacts.
- [ ] Production credentials use an approved secure mechanism.
- [ ] Workload access follows least privilege.
- [ ] Rotation/revocation behavior is defined where required.
- [ ] Local-only credential mechanisms cannot silently activate in production.
- [ ] Secret values are not leaked through logs/errors/diagnostics.
