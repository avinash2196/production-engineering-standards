# Workflow: Prepare for Production

## Purpose

Step-by-step procedure for validating a service is production-ready, covering configuration, observability, resilience, security, testing, deployment, and compliance.

## Prerequisites

- Service is functionally complete (all required endpoints implemented)
- Service runs locally with fallback mode
- Basic test suite exists

## Steps

### 1. Run Production Readiness Review

Invoke **production-readiness-reviewer** agent. This produces a checklist assessment across all areas. Address all CRITICAL findings before proceeding.

### 2. Configuration Hardening

- [ ] All environment-specific values externalized (no hardcoded hosts, ports, credentials)
- [ ] Secrets resolved via `SecretProvider` (not env vars in production)
- [ ] `*_ADAPTER` toggles confirmed OFF in production config/image
- [ ] Config precedence verified: operator overrides → dynamic config → env → build defaults
- [ ] Sensitive config keys cannot be overridden by low-privilege config sources

Reference: `standards/configuration-management.md`

### 3. Observability Validation

- [ ] Structured JSON logging confirmed in production log output
- [ ] Correlation ID present in all request-scoped logs
- [ ] Four golden signal metrics exposed on `/metrics` endpoint
- [ ] Metric names follow `<service>_<subsystem>_<signal>_<unit>` convention
- [ ] Distributed tracing active with W3C context propagation
- [ ] Health endpoint reports adapter connectivity status
- [ ] Readiness and liveness probes configured for orchestrator

**Validate:** send a test request and confirm log line includes `traceId`, `spanId`, `correlationId`. Confirm metrics increment.

Reference: `standards/observability.md`, `standards/observability/*.md`

### 4. Resilience Hardening

- [ ] Timeouts configured on all outbound calls (HTTP, DB, cache, messaging)
- [ ] Retry policies with exponential backoff and max attempts for transient failures
- [ ] Non-retryable errors excluded from retry (4xx, validation failures)
- [ ] Circuit breaker or bulkhead on critical downstream dependencies
- [ ] Graceful shutdown: drain in-flight requests, flush metrics, close connections
- [ ] Dead-letter routing for failed message processing

**Validate:** simulate a dependency timeout and confirm retry + circuit breaker behavior.

Reference: `standards/resiliency.md`

### 5. Security Hardening

- [ ] No secrets in source code, config files, Docker images, or logs
- [ ] TLS on all external endpoints
- [ ] Input validation at controller boundary (reject malformed requests early)
- [ ] Authentication and authorization enforced on all non-health endpoints
- [ ] Dependencies scanned for known CVEs (`OWASP dependency-check`, `pip-audit`, `npm audit`)
- [ ] Response headers include security headers (no sensitive info leakage)

Reference: `standards/security-basics.md`, `standards/security/*.md`

### 6. Testing Validation

- [ ] Unit tests pass — all service and domain logic covered
- [ ] Integration tests pass — adapter contracts validated
- [ ] No tests depend on external shared services
- [ ] Test execution time reasonable (<5 min for full suite)
- [ ] Edge cases and failure paths tested

Reference: `standards/testing/*.md`

### 7. Deployment Artifact Validation

- [ ] Dockerfile uses multi-stage build (no build tools in runtime image)
- [ ] Container runs as non-root user
- [ ] Resource limits defined (CPU, memory)
- [ ] Container image scanned for vulnerabilities
- [ ] `.env.example` documents all required environment variables
- [ ] Rollback strategy documented and tested

### 8. Compliance Validation (if HIPAA-aware)

Invoke **hipaa-reviewer** agent. Verify:

- [ ] PHI inventory complete and documented
- [ ] Encryption at rest for all PHI fields
- [ ] TLS 1.2+ for all PHI transmission
- [ ] Audit logging on all PHI access operations
- [ ] Minimum necessary principle in API responses
- [ ] No PHI in standard logs or error messages

Reference: `standards/compliance/hipaa-controls.md`

### 9. Load Test (if applicable)

- Baseline performance under expected load
- Verify no resource leaks (memory, connections, threads)
- Confirm metrics/alerting detect degradation

### 10. Go/No-Go Checklist

| Area | Status | Blocking? |
|------|--------|-----------|
| Configuration | ✅/❌ | Yes |
| Observability | ✅/❌ | Yes |
| Resilience | ✅/❌ | Yes |
| Security | ✅/❌ | Yes |
| Testing | ✅/❌ | Yes |
| Deployment | ✅/❌ | Yes |
| Compliance | ✅/❌/N/A | Yes (if HIPAA) |
| Load test | ✅/❌/N/A | No (but recommended) |

**Verdict:** READY / NOT READY (list blocking items)
