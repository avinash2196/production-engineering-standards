# SecretProvider

## Purpose

Define controlled secret access without spreading Vault, Secret Manager, or direct environment-variable reads through business code.

## Selection

Secret providers are selected explicitly:

| Selection | Environment | Behavior |
|---|---|---|
| `vault` / `secretmanager` | production/staging as approved | managed access policy, audit, and rotation capabilities |
| `env` | local development/tests | no managed rotation, centralized policy, or provider audit trail |

Do not dynamically choose the "most secure available" source. Explicit selection avoids silent security degradation. Production startup rejects `env`.

## Contract Decisions

- secret name and expected format;
- current versus versioned access;
- bootstrap timing;
- cache TTL, if any;
- rotation behavior;
- unavailable-provider behavior;
- audit and least-privilege requirements.

Security-sensitive secret resolution normally fails closed. Returning stale cached credentials is allowed only when the approved security design defines validity and revocation behavior.

## Rules

- Never log, return, or include secret values in metrics/errors.
- Keep direct environment reads inside the local `EnvSecretProvider` or typed bootstrap configuration.
- Do not add mandatory caching or rotation behavior unless the provider and requirement support it.
- Use workload identity/service identity rather than embedded provider credentials.

## Composition

```java
@Bean
@ConditionalOnProperty(name = "adapters.secrets", havingValue = "env")
SecretProvider envSecretProvider() {
    return new EnvSecretProvider(System.getenv());
}
```

```python
if settings.secret_adapter is SecretAdapter.ENV:
    return EnvSecretProvider()
```

## Test-First Requirements

- name mapping and missing-secret behavior;
- no secret value in logs/errors;
- selection and production rejection;
- managed-provider error translation;
- rotation/cache behavior only when part of approved scope.

## Review Checklist

- [ ] Provider selection is explicit
- [ ] `env` is rejected in production
- [ ] Secret values cannot leak through logs/errors
- [ ] Access/rotation requirements are grounded in the plan
- [ ] Local and managed provider tests cover selected behavior
