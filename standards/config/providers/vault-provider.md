# Managed Secret Store Adapter

## Purpose

Reference pattern for integrating an application with an **approved managed secret store**. The word "vault" here is historical/generic; this document does not require HashiCorp Vault or any particular cloud vendor.

Use this adapter pattern only when the project benefits from isolating secret-store SDK details behind a boundary such as `SecretProvider`. If the framework/platform already provides safe native secret injection or binding, use that instead.

The canonical policy is [Secrets Handling](../../security/secrets-handling.md).

## Possible Backends

Examples include HashiCorp Vault and cloud-managed secret/key services. Select the actual backend from the deployment architecture, organization standards, and project requirements. Do not choose a vendor from this repository alone.

## Authentication

Use the platform/organization-approved workload or service identity mechanism where available. Avoid long-lived embedded credentials. Exact authentication, token lifetime, rotation, and bootstrap behavior are platform-specific decisions.

## Optional Application Boundary

```java
public interface SecretProvider {
    String getSecret(String name);
}
```

A boundary is useful when it improves testability, keeps vendor SDK calls out of business logic, or supports an intentional adapter strategy. It is not mandatory when native framework integration is simpler and equally safe.

## Caching and Availability

Do not assume a universal five-minute cache or stale-secret fallback. Determine whether caching is allowed and safe for each secret type and backend.

Resolve explicitly:

- whether the platform already caches;
- acceptable retrieval latency;
- rotation semantics;
- whether stale values remain valid after rotation/revocation;
- startup/runtime behavior when the store is unavailable;
- rate limits and retry/backoff behavior.

Returning stale credentials after revocation can be incorrect or unsafe; use it only when the backend semantics and requirements justify it.

## Rotation

Support the rotation model of the selected backend and credential type. Some systems inject a new value on restart/redeploy; others support runtime refresh or dynamic credentials. Do not invent a webhook, dual-validity window, or refresh schedule unless the platform provides it.

## Observability

- Never log, trace, or emit secret values.
- Record safe access outcomes/errors using existing observability conventions.
- Avoid secret names in telemetry if names themselves reveal sensitive information.

## Security Requirements

- Use approved protected transport to the secret service.
- Apply least-privilege access to the required secret paths/resources.
- Keep bootstrap credentials out of source control.
- Follow the backend's audit/rotation controls and organization security policy.

## LLM Instructions

- Ask/inspect which secret mechanism the target environment already uses.
- Do not choose HashiCorp Vault, AWS, Azure, or GCP automatically.
- Do not introduce `SecretProvider` if native platform integration is already the intended design.
- Do not invent cache TTLs, stale fallback, rotation intervals, or authentication methods.
- Never generate logging of secret values.

## Review Checklist

- [ ] Backend and authentication come from the actual deployment/security model.
- [ ] Secret access follows least privilege.
- [ ] Secret values cannot enter logs/traces/metrics.
- [ ] Caching/failure behavior is explicitly justified.
- [ ] Rotation behavior matches the selected backend and credential semantics.
- [ ] No long-lived secret/bootstrap credential is committed to source control.
