# Vault Provider

## Purpose

Secret manager provider specification for production secret resolution. Integrates with cloud-managed secret stores (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager) to provide secrets to services through the `SecretProvider` interface.

## Supported Backends

| Backend | Use Case | Secret Types |
|---------|----------|-------------|
| HashiCorp Vault | Self-managed, multi-cloud | All (KV, dynamic DB creds, PKI) |
| AWS Secrets Manager | AWS-native | Static secrets, RDS credentials |
| Azure Key Vault | Azure-native | Secrets, keys, certificates |
| GCP Secret Manager | GCP-native | Static secrets |

The vault provider abstracts these behind `SecretProvider`, so service code never references a specific backend.

## Interface

Implements `SecretProvider`:

```java
public class VaultSecretProvider implements SecretProvider {
    String getSecret(String name);
    String getSecret(String name, String version);
    byte[] getSecretAsBytes(String name);
}
```

## Authentication

The service must authenticate to the secret store. Methods by priority:

| Method | Description | When to Use |
|--------|-------------|-------------|
| Workload identity | Cloud-native identity (IAM role, managed identity, Workload Identity Federation) | Default for cloud deployments |
| Kubernetes service account | K8s-native auth (Vault Kubernetes auth, Azure Workload Identity) | K8s deployments |
| App role / client credentials | Service authenticates with its own credential | On-prem or hybrid |
| Token (static) | Pre-provisioned token | Development/testing only (avoid in prod) |

**Mandatory rule:** workload identity or equivalent zero-credential auth is the default. Static tokens are acceptable only in dev/test.

## Caching Strategy

```
getSecret("db-password")
    │
    ▼
  In-memory cache hit?
    ├── Yes → return cached value (if TTL not expired)
    └── No → fetch from vault
              ├── Success → cache with TTL (default 5 min), return
              └── Failure → cached value exists?
                    ├── Yes → return stale value, log WARNING
                    └── No → throw SecretStoreUnavailableException
```

- **Default TTL:** 5 minutes. Configurable per secret.
- **Stale-while-revalidate:** on vault unavailability, return cached value if available.
- **Cache invalidation:** on secret rotation event (webhook) or manual flush.

## Rotation Support

- Secrets rotate in the vault without service restart.
- On next cache miss (after TTL expiry), the new value is fetched automatically.
- For critical rotations (e.g., DB password), the vault can send a webhook that triggers immediate cache invalidation.
- Services must handle transient auth failures gracefully during the rotation window (retry with backoff).

### Rotation Pattern (Database Credentials)

```
1. Vault creates new DB credential (version N+1)
2. Both version N and N+1 are valid simultaneously (dual-write window)
3. Services fetch N+1 on next cache refresh
4. After all services rotated, vault revokes version N
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Secret not found | Throw `SecretNotFoundException`. This is a configuration error. |
| Vault unreachable, cached value exists | Return cached value. Log WARNING. Emit metric. |
| Vault unreachable, no cached value | Throw `SecretStoreUnavailableException`. Service cannot start/continue. |
| Authentication failure | Retry once. If still failing, throw. Likely misconfigured identity. |
| Rate limited | Backoff and retry. Increase cache TTL if frequent. |

## Observability

- Metrics: `<service>_secrets_vault_requests_total`, `<service>_secrets_vault_latency_seconds`, `<service>_secrets_vault_errors_total{type="not_found|unavailable|auth_failure"}`, `<service>_secrets_cache_hits_total`, `<service>_secrets_rotation_total`.
- **Never log secret values.** Log secret names and access outcomes only.
- Create spans for vault requests (cache misses).

## Java Example

```java
@Component
@ConditionalOnProperty(name = "adapters.secrets", havingValue = "vault", matchIfMissing = true)
public class VaultSecretProvider implements SecretProvider {
    private final VaultClient client;
    private final Cache<String, CachedSecret> cache;

    @Override
    public String getSecret(String name) {
        CachedSecret cached = cache.getIfPresent(name);
        if (cached != null && !cached.isExpired()) {
            return cached.value();
        }
        try {
            String value = client.readSecret(name);
            cache.put(name, new CachedSecret(value, Duration.ofMinutes(5)));
            return value;
        } catch (VaultException e) {
            if (cached != null) {
                log.warn("Vault unavailable, returning stale secret: {}", name);
                return cached.value();
            }
            throw new SecretStoreUnavailableException(name, e);
        }
    }
}
```

## Python Example

```python
class VaultSecretProvider:
    def __init__(self, client: VaultClient, cache_ttl: timedelta = timedelta(minutes=5)):
        self._client = client
        self._cache: dict[str, CachedSecret] = {}
        self._cache_ttl = cache_ttl

    def get_secret(self, name: str) -> str:
        cached = self._cache.get(name)
        if cached and not cached.is_expired():
            return cached.value
        try:
            value = self._client.read_secret(name)
            self._cache[name] = CachedSecret(value, self._cache_ttl)
            return value
        except VaultError:
            if cached:
                logger.warning(f"Vault unavailable, returning stale secret: {name}")
                return cached.value
            raise SecretStoreUnavailableError(name)
```

## Security Requirements

- Vault connection must use TLS.
- Service must have access only to its own secrets (least privilege policy in vault).
- Audit logging enabled on the vault backend (who accessed what, when).
- Static vault tokens must rotate on a schedule and must not be committed to source control.

## LLM Instructions

- When generating secret access code, use `SecretProvider.getSecret()`, never direct vault SDK calls in service code.
- Never generate code that logs or prints a secret value.
- Default to workload identity authentication for cloud deployments.
- Generate the caching pattern with stale-while-revalidate.
- Ask the user which vault backend they use before choosing the implementation.

## Review Checklist

- [ ] Vault connection uses TLS.
- [ ] Authentication uses workload identity (no static tokens in production).
- [ ] Cache TTL configured (default 5 min).
- [ ] Stale-while-revalidate on vault failure.
- [ ] Secret values never logged.
- [ ] Least privilege vault policy (service accesses only its secrets).
- [ ] Rotation supported without restart.
