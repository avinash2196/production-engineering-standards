# SecretProvider

## Purpose

Define the capability interface for resolving secrets (API keys, database credentials, encryption keys, tokens) with explicit rotation, caching, and access-control contracts. Services depend on this abstraction, never directly on Vault, AWS Secrets Manager, Azure Key Vault, or environment variables.

## Interface Contract

- `getSecret(name)` → returns the current value of the named secret. Throws `SecretNotFoundException` if not found.
- `getSecret(name, version)` → returns a specific version of the secret (for rotation scenarios).
- `getSecretAsBytes(name)` → returns binary secret (encryption keys, certificates).
- Secrets are string-typed by default. The caller is responsible for parsing (e.g., JSON connection strings).

## Required Semantics

- **Resolution order:** the provider resolves secrets from the most secure source available. In production, this is always a managed secret store (Vault, Key Vault, Secrets Manager). In local development with `FALLBACK_SECRETS=env`, environment variables are used as a last resort.
- **Caching:** secrets should be cached in memory with a short TTL (default: 5 minutes) to avoid excessive calls to the secret store. The cache must be invalidatable.
- **Rotation support:** the provider must support secret rotation without service restart. On next access after cache expiry, the new value is fetched transparently.
- **Access auditing:** in production, the secret store should log which service accessed which secret and when. This is typically handled by the store itself (Vault audit log, Key Vault diagnostics).
- **Lazy loading:** secrets are resolved on first access, not at startup. This avoids blocking startup on secret store availability (except for critical bootstrap secrets like DB credentials).

## Error Handling

- `SecretNotFoundException` → secret name not found in the store. Fail fast; this is a configuration error.
- Secret store unavailable → if a cached value exists, return it (stale-while-revalidate). If no cached value, throw `SecretStoreUnavailableException`.
- Log all errors at ERROR level with the secret name (never the value) and `traceId`.
- Emit `<service>_secrets_errors_total{type="not_found|unavailable"}`.

## Observability

- Metrics: `<service>_secrets_access_total`, `<service>_secrets_cache_hits_total`, `<service>_secrets_cache_misses_total`, `<service>_secrets_errors_total`, `<service>_secrets_rotation_total`.
- **Never log or emit a secret value.** Log only the secret name and access outcome.
- Create spans for secret resolution on cache miss (calls to the secret store).

## Production vs Local Differences

- **Production:** HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager. Encrypted storage, access policies, audit logging, rotation automation.
- **Local / fallback (`FALLBACK_SECRETS=env`):** secrets read from environment variables. No rotation, no caching, no audit trail. Acceptable for development only.
- Fallback must never be active in production. Enforce via startup validation.

## Java Example

```java
public interface SecretProvider {
    String getSecret(String name);
    String getSecret(String name, String version);
    byte[] getSecretAsBytes(String name);
}

@Component
@Profile("!fallback-secrets")
public class VaultSecretProvider implements SecretProvider {
    // HashiCorp Vault implementation with caching, rotation, audit
}

@Component
@Profile("fallback-secrets")
public class EnvSecretProvider implements SecretProvider {
    @Override
    public String getSecret(String name) {
        return System.getenv(name);
    }
    // no caching, no rotation, no versioning
}
```

## Python Example

```python
class SecretProvider(Protocol):
    def get_secret(self, name: str) -> str: ...
    def get_secret_version(self, name: str, version: str) -> str: ...
    def get_secret_as_bytes(self, name: str) -> bytes: ...
```

## Anti-Patterns

- **Secrets in source code or config files:** all secrets must come from `SecretProvider`.
- **Logging secret values:** never log, print, or include secret values in error messages or metrics.
- **No rotation plan:** every secret must have a documented rotation schedule.
- **Startup dependency on all secrets:** use lazy loading except for critical bootstrap secrets.
- **Disabling fallback check in production:** `FALLBACK_SECRETS=env` in production is a critical security violation.

## LLM Instructions

- When a service needs a secret, inject `SecretProvider` and call `getSecret(name)`. Never read environment variables directly in production code.
- Never generate code that logs or exposes a secret value.
- Ask the user which secret store is used before choosing the production implementation.
- Wire fallback via Spring profile or Python dependency injection.

## Review Checklist

- [ ] All secrets resolved via `SecretProvider`, not direct env/file access in production code.
- [ ] Secret values never logged, printed, or included in error responses.
- [ ] Caching with short TTL implemented (default 5 min).
- [ ] Rotation supported without service restart.
- [ ] Metrics emitted for access, cache hits/misses, and errors.
- [ ] Fallback implementation exists for local development.
- [ ] Fallback cannot activate in production.
