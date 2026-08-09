# Secret Local Adapter

## Purpose

Environment-variable-based secret resolution for local development when a secret manager (Vault, Key Vault) is unavailable. Activated by `SECRET_ADAPTER=env`. Implements `SecretProvider` interface by reading secrets from OS environment variables.

## Activation

| Environment | Toggle | Active |
|-------------|--------|--------|
| Local dev | `SECRET_ADAPTER=env` | Yes |
| Staging | `vault` or `secretmanager` | Production provider |
| Production | `vault` or `secretmanager` | Local value rejected |

**Startup validation:** if `SECRET_ADAPTER=env` and the environment is production, fail startup immediately. This is a critical security violation.

## Behavior

```
getSecret("db-password")
    → reads System.getenv("DB_PASSWORD") / os.environ.get("DB_PASSWORD")
    → returns value or throws SecretNotFoundException

getSecret("db-password", "v2")
    → version parameter ignored (env vars don't have versions)
    → logs WARNING about version being ignored in local-adapter mode
```

- Key mapping: secret name is uppercased, hyphens/dots replaced with underscores.
  - `db-password` → `DB_PASSWORD`
  - `api.external.key` → `API_EXTERNAL_KEY`
- No caching (env vars don't change at runtime).
- No rotation support.
- No audit logging.

## Java Example

```java
@Component
@ConditionalOnProperty(name = "adapters.secrets", havingValue = "env")
public class EnvSecretProvider implements SecretProvider {

    @Override
    public String getSecret(String name) {
        String envKey = name.replace("-", "_").replace(".", "_").toUpperCase();
        String value = System.getenv(envKey);
        if (value == null) {
            throw new SecretNotFoundException(name,
                "Secret not found in env var: " + envKey + " (local-adapter mode)");
        }
        return value;
    }

    @Override
    public String getSecret(String name, String version) {
        log.warn("Version parameter ignored in local secret provider: {}@{}", name, version);
        return getSecret(name);
    }

    @Override
    public byte[] getSecretAsBytes(String name) {
        return Base64.getDecoder().decode(getSecret(name));
    }
}
```

## Python Example

```python
import os, base64

class EnvSecretProvider:
    def get_secret(self, name: str) -> str:
        env_key = name.replace("-", "_").replace(".", "_").upper()
        value = os.environ.get(env_key)
        if value is None:
            raise SecretNotFoundError(f"Secret not found in env var: {env_key} (local-adapter mode)")
        return value

    def get_secret_version(self, name: str, version: str) -> str:
        logger.warning(f"Version parameter ignored by local adapter: {name}@{version}")
        return self.get_secret(name)

    def get_secret_as_bytes(self, name: str) -> bytes:
        return base64.b64decode(self.get_secret(name))
```

## Local Development Setup

Developers set secrets in a `.env.local` file (gitignored):

```bash
# .env.local (NEVER commit this file)
DB_PASSWORD=local-dev-password
API_EXTERNAL_KEY=test-key-12345
JWT_SIGNING_KEY=dGVzdC1rZXk=
```

Load via:
- **Java:** Spring dotenv plugin or `source .env.local && mvn spring-boot:run`
- **Python:** `python-dotenv` in development, or `export $(cat .env.local | xargs)`

## Security Risks of Local-Adapter Mode

| Risk | Mitigation |
|------|------------|
| Env vars visible in `ps`, `/proc`, container inspect | Acceptable in local dev only |
| No encryption at rest | Acceptable in local dev only |
| No rotation | Acceptable in local dev only |
| No audit trail | Acceptable in local dev only |
| `.env.local` accidentally committed | Add to `.gitignore`; pre-commit hook to check |

## Limitations

| Feature | Production Vault | Local adapter |
|---------|-----------------|----------|
| Encryption at rest | Yes | No |
| Access audit | Yes | No |
| Rotation | Yes (automatic) | No |
| Versioning | Yes | No |
| Caching/TTL | Provider/configuration dependent | No (direct env read) |
| Least privilege | Policy-based | N/A |

## LLM Instructions

- When scaffolding a secret local adapter, use the env-var pattern above.
- Wire via `@ConditionalOnProperty(name = "adapters.secrets", havingValue = "env")` or Python conditional injection.
- Always add `.env.local` to `.gitignore` in generated projects.
- Always generate startup validation that rejects the local adapter in production.
- Warn the user that local-adapter mode provides no security guarantees.

## Review Checklist

- [ ] Local adapter activated only by `SECRET_ADAPTER=env`.
- [ ] Startup fails if local adapter active in production.
- [ ] Implements full `SecretProvider` interface.
- [ ] `.env.local` in `.gitignore`.
- [ ] Key mapping convention documented (uppercase, underscores).
- [ ] Risks acknowledged and accepted for local dev only.
