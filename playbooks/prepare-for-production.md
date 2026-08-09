# Workflow: Prepare for Production

## Purpose

Step-by-step procedure for validating a service is production-ready, covering configuration, observability, resilience, security, testing, deployment, and compliance.

## Prerequisites

- Service is functionally complete (all required endpoints implemented)
- Service has a repeatable local/test execution path
- Basic test suite exists

## Steps

### 1. Run Production Readiness Review

Invoke **production-readiness-reviewer** agent. This produces a checklist assessment across all areas. Address all CRITICAL findings before proceeding.

### 2. Configuration Hardening

- [ ] All environment-specific values externalized (no hardcoded hosts, ports, credentials)
- [ ] Secrets resolved via `SecretProvider` (not env vars in production)
- [ ] `*_ADAPTER` selectors use approved production values, and startup validation rejects all local-only values
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
- [ ] Retry policies, where used, are bounded and safe for duplicate effects; deterministic failures and overload signals are excluded/handled appropriately
- [ ] Deterministic/non-retryable failures are excluded from retry according to dependency semantics
- [ ] Circuit breaking, bulkheads, concurrency limits, durable queueing, or fail-fast behavior is applied where justified by the dependency/failure model
- [ ] Graceful shutdown: drain in-flight requests, flush metrics, close connections
- [ ] Failed-message handling is explicit for message flows where retry/loss semantics require it

**Validate:** simulate representative dependency failures and confirm the approved timeout, retry/degradation, observability, and recovery behavior.

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
- [ ] Test execution time fits the project's CI/developer feedback budget; slower suites are intentionally separated where needed
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
- [ ] Approved at-rest safeguards for PHI/ePHI are implemented according to the applicable risk/security decision
- [ ] PHI/ePHI transmission uses the organization-approved secure transport configuration
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
