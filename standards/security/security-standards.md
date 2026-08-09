# Security Standards

## Purpose

High-level security standards that apply to every service. Covers authentication, authorization, input validation, dependency management, and least-privilege principles. These are mandatory engineering requirements, not optional best practices.

## Mandatory Rules

### 1. Authentication

Every service endpoint that serves non-public data requires authentication.

| Rule | Detail |
|------|--------|
| Default: all endpoints authenticated | Use an allow-list for public endpoints, not a deny-list |
| Token format | JWT (RS256 or ES256) with expiration, issuer, and audience claims |
| Service-to-service | mTLS or signed JWT with service identity |
| No basic auth in production | Basic auth, if allowed at all, is limited to explicitly approved local/test use and is not a production fallback |
| Session management | Stateless JWT preferred; if stateful, server-side session store with short TTL |

```java
// Java — Spring Security default: secure everything, allow-list public paths
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(auth -> auth
            .requestMatchers("/health", "/ready", "/metrics").permitAll()
            .anyRequest().authenticated()
        );
        return http.build();
    }
}
```

```python
# Python — FastAPI dependency
async def require_auth(token: str = Depends(oauth2_scheme)) -> AuthContext:
    claims = verify_jwt(token)  # validates signature, expiry, issuer, audience
    return AuthContext.from_claims(claims)
```

### 2. Authorization

Authentication proves identity; authorization determines what the identity can do.

| Rule | Detail |
|------|--------|
| Enforce at service layer | Not just at gateway or controller |
| RBAC or ABAC | Role-based minimum; attribute-based for fine-grained PHI access |
| No implicit admin | Admin capabilities require explicit role assignment |
| Resource-level checks | User can only access resources they own or are assigned to |

```java
// Service layer authorization check
public OrderDto getOrder(String orderId, AuthContext auth) {
    Order order = orderRepository.findById(orderId);
    if (!auth.hasRole("admin") && !order.getOwnerId().equals(auth.getUserId())) {
        throw new AccessDeniedException("Not authorized to access order: " + orderId);
    }
    return OrderDto.from(order);
}
```

### 3. Input Validation

All external input is untrusted. Validate at the system boundary.

| Rule | Detail |
|------|--------|
| Validate at controller/handler | Before data reaches service or domain layer |
| Allowlist validation | Define what's valid, reject everything else |
| Type coercion | Use typed DTOs, not raw string maps |
| Size limits | Max string lengths, max collection sizes, max request body |
| No SQL/command injection | Use parameterized queries exclusively. Never concatenate user input into queries |
| No XSS | HTML-encode output. Use framework-provided template engines |
| Path traversal | Validate file paths. Never pass user input directly to file operations |

```java
// Java — validation annotations on DTOs
public record CreateOrderRequest(
    @NotNull @Size(min = 1, max = 100) String customerId,
    @NotNull @Size(min = 1, max = 50) List<@Valid OrderItem> items,
    @Size(max = 500) String notes
) {}
```

```python
# Python — Pydantic validation
class CreateOrderRequest(BaseModel):
    customer_id: str = Field(min_length=1, max_length=100)
    items: list[OrderItem] = Field(min_length=1, max_length=50)
    notes: str | None = Field(default=None, max_length=500)
```

### 4. Dependency Security

| Rule | Detail |
|------|--------|
| Automated CVE scanning | Run `dependabot`, `snyk`, or `trivy` on every build |
| No known critical CVEs | CI fails on CRITICAL or HIGH severity vulnerabilities |
| Minimal dependencies | Don't add libraries for trivial functionality |
| Pinned versions | Use exact versions, not ranges, for reproducible builds |
| License compliance | Verify license compatibility before adding a dependency |

### 5. Least Privilege

| Rule | Detail |
|------|--------|
| Service accounts | Minimum required permissions. No wildcard policies |
| Database accounts | Service uses a restricted DB user (SELECT/INSERT/UPDATE on its own tables only) |
| Secret access | Each service accesses only its own secrets in the vault |
| Network | Services exposed only to their consumers (no public exposure unless required) |
| File system | Read-only container filesystem where possible |

### 6. Error Handling & Information Disclosure

| Rule | Detail |
|------|--------|
| Generic error responses | Return `500 Internal Server Error` without stack traces or internals |
| No PII/PHI in errors | Error messages must not contain user data |
| No infrastructure details | Don't expose database names, internal IPs, or library versions |
| Structured error format | `{ "error": "ORDER_NOT_FOUND", "message": "The requested order does not exist" }` |

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handle(Exception e) {
        log.error("Unhandled exception", e); // full details in server log
        return ResponseEntity.status(500)
            .body(new ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred"));
    }
}
```

### 7. CORS and Headers

| Header | Value | Purpose |
|--------|-------|---------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Force HTTPS |
| `X-Content-Type-Options` | `nosniff` | Prevent MIME type sniffing |
| `X-Frame-Options` | `DENY` | Prevent clickjacking |
| `Content-Security-Policy` | Appropriate for the application | Prevent XSS |
| CORS | Explicit origin allowlist | No wildcard `*` in production |

## Anti-Patterns

- **Security by obscurity:** never rely on hidden endpoints or secret URL paths.
- **Client-side-only validation:** always validate on the server. Client validation is UX, not security.
- **Shared credentials across services:** each service gets its own identity and secrets.
- **Catch-all CORS policy (`*`):** use explicit origin allowlist in production.
- **Logging sensitive data for debugging:** use correlation IDs instead.

## LLM Instructions

- When generating any endpoint, add authentication by default. Ask the user if it should be public.
- Generate input validation on all DTOs/request models.
- Use parameterized queries exclusively. Never generate string concatenation for SQL.
- Add security headers to HTTP response configuration.
- Generate Global exception handler that returns generic errors.

## Review Checklist

- [ ] All endpoints authenticated (public endpoints explicitly allow-listed).
- [ ] Authorization enforced at service layer.
- [ ] Input validation on all external inputs with size limits.
- [ ] Parameterized queries only (no SQL concatenation).
- [ ] Generic error responses (no stack traces, no internal details).
- [ ] Security headers configured.
- [ ] Dependency CVE scanning in CI.
- [ ] Least privilege for service accounts, DB users, and secret access.
