# Transport Encryption

## Purpose

Enforce TLS for all network communication. Defines minimum protocol versions, cipher suites, certificate management, and mTLS requirements for service-to-service traffic.

## Mandatory Rules

### TLS Minimum Version

| Protocol | Allowed | Notes |
|----------|---------|-------|
| TLS 1.3 | Preferred | Best performance and security |
| TLS 1.2 | Allowed | Required for legacy client compatibility |
| TLS 1.1, 1.0 | **Prohibited** | Known vulnerabilities |
| SSL 3.0, 2.0 | **Prohibited** | Broken — never use |

### Where TLS Is Required

| Connection Type | TLS Required | mTLS Required |
|----------------|-------------|---------------|
| External API (client → service) | Yes | No (JWT/OAuth on top of TLS) |
| Service-to-service (internal) | Yes | Recommended |
| Service-to-database | Yes | Recommended for PHI services |
| Service-to-cache (Redis) | Yes | No (network-level isolation acceptable) |
| Service-to-message broker (Kafka) | Yes | Recommended |
| Service-to-secret store (Vault) | Yes | Yes |
| Health/readiness probes (internal) | Optional | No |

### Cipher Suites

Allow only strong cipher suites. Reject weak ones at the server level.

**Recommended (TLS 1.3):**
- `TLS_AES_256_GCM_SHA384`
- `TLS_AES_128_GCM_SHA256`
- `TLS_CHACHA20_POLY1305_SHA256`

**Recommended (TLS 1.2):**
- `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`
- `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256`
- `TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384`

**Prohibited:**
- Any cipher with `RC4`, `DES`, `3DES`, `MD5`, `SHA1`, `NULL`, `EXPORT`

## Certificate Management

### Certificate Lifecycle

| Stage | Responsibility | Automation |
|-------|---------------|------------|
| Issuance | Internal CA or public CA (Let's Encrypt, ACM) | Automated via cert-manager, ACME |
| Storage | `SecretProvider` (vault or managed cert store) | Never on filesystem in production |
| Rotation | Auto-rotate before expiry (30 days lead time) | cert-manager, Vault PKI, ACM auto-renewal |
| Revocation | CRL or OCSP | Monitored |
| Monitoring | Alert on certs expiring within 30 days | Prometheus alert or Azure Monitor |

### Self-Signed Certificates

| Environment | Allowed |
|-------------|---------|
| Local dev | Yes (via mkcert or similar) |
| Staging | No (use internal CA) |
| Production | **Never** |

## mTLS (Mutual TLS)

For service-to-service communication where both sides authenticate via certificates.

### When to Use mTLS

- Service mesh (Istio, Linkerd) handles mTLS transparently → preferred approach.
- Services handling PHI or Restricted data.
- Cross-network-boundary calls (between VPCs, clusters, or data centers).

### mTLS Without Service Mesh

```java
// Java — Spring Boot mTLS client config
@Bean
public RestTemplate mtlsRestTemplate() throws Exception {
    SSLContext sslContext = SSLContextBuilder.create()
        .loadKeyMaterial(clientKeyStore, keyPassword)     // client cert
        .loadTrustMaterial(trustStore, null)               // CA certs
        .build();
    HttpClient httpClient = HttpClients.custom()
        .setSSLContext(sslContext)
        .build();
    return new RestTemplateBuilder()
        .requestFactory(() -> new HttpComponentsClientHttpRequestFactory(httpClient))
        .build();
}
```

```python
# Python — httpx with mTLS
import httpx

client = httpx.Client(
    cert=("/path/to/client.crt", "/path/to/client.key"),
    verify="/path/to/ca-bundle.crt",
)
```

## Java (Spring Boot) TLS Configuration

```yaml
# application-production.yml
server:
  ssl:
    enabled: true
    protocol: TLS
    enabled-protocols: TLSv1.3,TLSv1.2
    ciphers:
      - TLS_AES_256_GCM_SHA384
      - TLS_AES_128_GCM_SHA256
      - TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
    key-store: ${SSL_KEYSTORE_PATH}
    key-store-password: ${SSL_KEYSTORE_PASSWORD}  # via SecretProvider
    key-store-type: PKCS12
```

## Python (FastAPI/Uvicorn) TLS Configuration

```python
# main.py
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8443,
        ssl_keyfile="/path/to/server.key",
        ssl_certfile="/path/to/server.crt",
        ssl_version=ssl.PROTOCOL_TLS_SERVER,
    )
```

## Database Connection TLS

```yaml
# Java — Spring datasource with TLS
spring:
  datasource:
    url: jdbc:postgresql://db-host:5432/mydb?sslmode=verify-full&sslrootcert=/path/to/ca.crt
```

```python
# Python — SQLAlchemy with TLS
DATABASE_URL = "postgresql://user:pass@db-host:5432/mydb?sslmode=verify-full&sslrootcert=/path/to/ca.crt"
```

- `sslmode=verify-full` validates both the certificate and the hostname.
- `sslmode=require` encrypts but does not validate — use only when `verify-full` is not possible.

## Anti-Patterns

- **TLS termination at gateway only:** encrypt all the way to the service, not just gateway → service.
- **Self-signed certs in production:** use a proper CA.
- **Disabling certificate validation in code:** never `verify=False` or `InsecureTrustManager` in production.
- **Hardcoded cert passwords:** use `SecretProvider`.
- **Ignoring cert expiry:** automate rotation and alert on approaching expiry.

## LLM Instructions

- When generating HTTP clients, always use HTTPS URLs in production config.
- When generating database connections, include `sslmode=verify-full`.
- Never generate code that disables certificate verification.
- When asked to configure TLS, use TLS 1.2+ only and the recommended cipher suites above.
- For mTLS, check if a service mesh handles it before generating application-level mTLS.

## Review Checklist

- [ ] TLS 1.2+ enforced on all external and internal connections.
- [ ] TLS 1.0, 1.1, SSL prohibited.
- [ ] Strong cipher suites only (no RC4, DES, MD5).
- [ ] Certificates managed via automated process (cert-manager, ACME).
- [ ] Certificate rotation automated with 30-day lead time.
- [ ] mTLS for service-to-service where required (PHI, cross-boundary).
- [ ] Database connections use TLS with certificate verification.
- [ ] No certificate verification disabled in code.
- [ ] Certificate expiry monitoring and alerting configured.
