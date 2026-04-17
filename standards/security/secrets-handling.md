# Secrets Handling

## Purpose

Standards for storing, accessing, rotating, and disposing of secrets across all services. Secrets include database credentials, API keys, encryption keys, JWT signing keys, TLS certificates/keys, and service account tokens.

## Mandatory Rules

### 1. No Secrets in Source Code

| Forbidden Location | Why | What to Do Instead |
|-------------------|-----|-------------------|
| Source files (hardcoded strings) | Committed to VCS, visible to all developers | Use `SecretProvider` |
| Config files (`application.yml`, `.env`) | Committed to VCS | Use `SecretProvider` for secrets, `ConfigProvider` for non-secret config |
| Docker images / Dockerfiles | Visible via `docker inspect`, layer history | Inject at runtime via env or vault |
| CI/CD pipeline definitions | Visible in pipeline config | Use CI/CD secret variables or vault integration |
| Log files | Accessible to operators and log aggregation | Never log secret values |
| Error messages / stack traces | Returned to clients, stored in error tracking | Redact or omit |
| URL query parameters | Logged by proxies, browsers, CDNs | Use headers or request body |

**Detection:** run `gitleaks`, `trufflehog`, or equivalent scanner in CI. Block merges when secrets detected.

### 2. Use SecretProvider Exclusively

All production secret access must go through `SecretProvider`:

```java
// Correct
String dbPassword = secretProvider.getSecret("db-password");

// WRONG — never do this in production code
String dbPassword = System.getenv("DB_PASSWORD");         // bypasses SecretProvider
String dbPassword = config.get("database.password");      // wrong provider (ConfigProvider)
String dbPassword = "hardcoded-password-123";             // hardcoded
```

See: [SecretProvider.md](../../core/abstractions/SecretProvider.md)

### 3. Rotation

Every secret must have a rotation plan:

| Secret Type | Rotation Frequency | Method |
|-------------|-------------------|--------|
| Database credentials | 90 days | Vault dynamic credentials or automated rotation |
| API keys (external) | Per vendor policy or 180 days | Manual with notification or automated |
| Encryption keys | 365 days | Key rotation with envelope encryption (no re-encryption needed) |
| JWT signing keys | 180 days | Dual-key period: old key still verifies, new key signs |
| TLS certificates | Before expiry (30-day lead) | cert-manager auto-renewal |
| Service account tokens | 90 days | Vault auto-rotation or managed identity (no rotation needed) |

**Rotation rules:**
- Rotation must not require service restart (secret is fetched fresh from vault on next cache miss).
- During rotation, both old and new values must be valid simultaneously (dual-write window).
- After all consumers have rotated, revoke the old secret.
- Emit `<service>_secrets_rotation_total` metric when a new version is detected.

### 4. Caching

- Secrets cached in memory with TTL (default 5 minutes).
- Cache is invalidated on explicit rotation event or TTL expiry.
- Stale-while-revalidate: if vault is unreachable, return cached value rather than failing.
- **Never cache secrets to disk, database, or external cache (Redis).**

### 5. Access Control

| Principle | Implementation |
|-----------|----------------|
| Least privilege | Each service accesses only its own secrets in the vault |
| Audit trail | Vault logs every secret access (who, what, when) |
| No shared secrets | Each service gets its own credential, not a shared one |
| Emergency access | Break-glass procedure with full audit and notification |

### 6. Secret Types and Handling

| Type | Storage | Rotation | Special Handling |
|------|---------|----------|-----------------|
| Database password | Vault KV or dynamic | 90 days / on-demand | Dynamic credentials preferred (Vault generates per-connection) |
| API key | Vault KV | Per policy | Store with metadata (vendor, purpose, expiry) |
| Encryption key | Vault Transit or KMS | 365 days | Envelope encryption — rotate wrapping key, not data key |
| JWT signing key | Vault KV or managed | 180 days | JWKS endpoint serves multiple keys during rotation |
| TLS key/cert | Vault PKI or cert-manager | Before expiry | Auto-rotation mandatory |
| OAuth client secret | Vault KV | 180 days | Rotate in identity provider and vault simultaneously |

## Local Development

In local development, `FALLBACK_SECRETS=env` allows reading secrets from environment variables:

```bash
# .env.local (NEVER committed to VCS)
DB_PASSWORD=local-dev-password
API_KEY=test-key-12345
```

- `.env.local` must be in `.gitignore`.
- Pre-commit hook should reject commits containing `.env.local` or patterns matching secrets.

See: [secret-fallback.md](../../core/fallbacks/secret-fallback.md)

## CI/CD Pipeline Secrets

| Platform | Secret Mechanism |
|----------|-----------------|
| GitHub Actions | Repository/environment secrets |
| Azure DevOps | Variable groups with vault integration |
| GitLab CI | CI/CD variables (masked, protected) |
| Jenkins | Credentials plugin with vault integration |

**Rules:**
- Pipeline secrets masked in logs.
- Secrets scoped to the minimum required environment (not globally accessible).
- Rotate pipeline secrets on the same schedule as application secrets.

## Incident Response

If a secret is compromised:

1. **Immediately rotate** the compromised secret in the vault.
2. **Revoke** the old secret value.
3. **Audit** vault access logs to determine exposure scope.
4. **Scan** for the compromised value in logs, error tracking, and monitoring systems.
5. **Notify** security team and affected downstream consumers.
6. **Review** how the compromise occurred and close the vulnerability.

## Anti-Patterns

- **Secrets in ConfigProvider:** use `SecretProvider` for all secrets.
- **Logging secret values:** never, under any circumstance, log a secret value.
- **Shared credentials:** each service and each environment gets its own credentials.
- **No rotation plan:** every secret must have a documented rotation schedule.
- **Secrets in Docker build args:** use runtime injection, not build-time.
- **Disabling vault in production:** `FALLBACK_SECRETS=env` must never be active in production.

## LLM Instructions

- When generating code that needs a secret, use `SecretProvider.getSecret()`.
- Never generate hardcoded secrets, even as placeholders. Use `<REPLACE_WITH_SECRET>` markers.
- Never generate code that logs or prints a secret value.
- When generating CI/CD pipelines, use the platform's secret mechanism.
- When asked about secret rotation, generate the dual-key rotation pattern.
- Ask the user which vault backend they use before generating vault-specific code.

## Review Checklist

- [ ] No secrets in source code, config files, Docker images, or logs.
- [ ] All secrets accessed via `SecretProvider` in production.
- [ ] Rotation plan documented for every secret type.
- [ ] Rotation does not require service restart.
- [ ] `.env.local` in `.gitignore`.
- [ ] Secret scanner running in CI (`gitleaks`, `trufflehog`, etc.).
- [ ] Vault access policies follow least privilege.
- [ ] Fallback mode (`FALLBACK_SECRETS=env`) cannot activate in production.
