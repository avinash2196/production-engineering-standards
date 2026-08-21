# SecretProvider

## Purpose

Optional capability boundary for projects that benefit from isolating secret retrieval from business/application logic—for example to contain vendor SDKs, support test doubles/local adapters, or enforce a stable policy boundary.

A project may instead use its framework/platform's native secret injection/binding when that is simpler and meets the security requirements. See [Secrets Handling](../standards/security/secrets-handling.md).

## Contract Decisions

If this boundary is adopted, define only the behavior the project needs:

- secret identifier/name mapping;
- value type/format;
- current versus versioned access where relevant;
- bootstrap timing;
- caching, if allowed;
- rotation/refresh behavior supported by the selected backend;
- unavailable/not-found/authentication behavior;
- audit and least-privilege requirements.

Do not invent cache TTLs, stale-value fallback, rotation intervals, or backend behavior.

## Local Adapter

The repository includes an environment-backed local reference adapter selected with `SECRET_ADAPTER=env`. Use it only when the adopting project explicitly chooses that local strategy and documents its reduced guarantees. It is not an automatic fallback when a production secret service fails.

Production startup should reject a local-only selector **when that selector exists in the project and the production model prohibits it**.

## Rules

- Never log, trace, return in errors, or emit secret values in metrics.
- Keep provider/backend details out of business logic when this boundary is used.
- Use the authentication mechanism approved by the selected platform/security architecture; prefer short-lived/workload identity where that is the platform standard.
- Fail closed for security-sensitive resolution unless an explicitly approved design defines another safe behavior.

## Example

```java
public interface SecretProvider {
    String getSecret(String name);
}
```

The interface is illustrative. Do not add version/caching APIs that current requirements do not need.

## Test-First Concerns

When applicable, test:

- identifier mapping and missing-secret behavior;
- absence of secret values from logs/errors;
- provider/local-adapter selection rules actually adopted by the project;
- production rejection of local-only selection when required;
- backend error translation;
- cache/rotation behavior only when in approved scope.

## Review Checklist

- [ ] The boundary is justified or already adopted.
- [ ] Secret values cannot leak through diagnostics.
- [ ] Backend/authentication choice comes from the deployment/security model.
- [ ] Local-only behavior cannot become an unapproved production fallback.
- [ ] Cache/rotation/failure behavior is grounded in provider semantics and requirements.
