# Workflow: Review Existing Repository

## Purpose

Comprehensive assessment of an existing repository against enterprise-ai-engineering standards, producing a prioritized remediation roadmap.

## Prerequisites

- Access to the full repository codebase
- Knowledge of the service's purpose and external dependencies

## Steps

### 1. Initial Scan

Identify:

- Stack (Java Spring Boot / Python FastAPI / other)
- Project structure (packages/modules, entry points, config files)
- External dependencies (from build files: `pom.xml`, `build.gradle`, `requirements.txt`, `pyproject.toml`)
- Deployment artifacts (Dockerfile, docker-compose, CI config)
- Existing tests (location, framework, coverage)

### 2. Architecture Review

Invoke **architecture-reviewer** agent:

- Is layered architecture followed? (controller → service → domain → repository)
- Are dependency directions correct?
- Is the domain model meaningful or anemic?
- Are DTOs separated from domain entities?

### 3. Abstraction & Fallback Review

Check each external dependency:

| Dependency | Abstracted? | Fallback? | Toggle? |
|-----------|-------------|-----------|---------|
| Kafka | ✅/❌ | ✅/❌ | ✅/❌ |
| Redis | ✅/❌ | ✅/❌ | ✅/❌ |
| S3 | ✅/❌ | ✅/❌ | ✅/❌ |
| Vault | ✅/❌ | ✅/❌ | ✅/❌ |

Reference: `standards/fallback-strategy.md`, `contracts/`

### 4. Configuration Review

- Are all env-specific values externalized?
- Is config precedence followed? (operator → dynamic → env → files → defaults)
- Are secrets separate from config? (SecretProvider, not mixed into config files)
- Are `*_ADAPTER` toggles present and disabled by default?

Reference: `standards/configuration-management.md`

### 5. Observability Review

- Structured JSON logging with correlation ID?
- Four golden signal metrics?
- Distributed tracing with context propagation?
- Health endpoint with adapter checks?

Reference: `standards/observability.md`, `standards/observability/*.md`

### 6. Security Review

- No hardcoded secrets in source, config, or Docker images?
- Input validation at controller layer?
- Auth/authz on endpoints?
- Dependencies scanned for vulnerabilities?

Reference: `standards/security-basics.md`, `standards/security/*.md`

### 7. Testing Review

- Unit tests exercise business logic with mocked abstractions?
- Integration tests validate adapter contracts?
- Tests are deterministic (no shared external services)?
- Test naming and structure follow conventions?

Reference: `standards/testing/*.md`

### 8. Distributed Systems Review

Invoke **distributed-systems-reviewer** agent:

- Timeouts on all outbound calls?
- Retry policies with exponential backoff?
- Idempotency in message consumers?
- Failure modes documented for each dependency?

### 9. Compliance Review (if applicable)

Invoke **compliance-reviewer** or **hipaa-reviewer** agent:

- Data classification documented?
- Encryption at rest and in transit?
- Audit logging on sensitive data access?
- Access control enforced?

### 10. Produce Remediation Roadmap

Compile findings into a prioritized roadmap:

```markdown
## Remediation Roadmap: <repo-name>

### Phase 1: Critical (block production deploy)
1. [CRITICAL] Remove hardcoded DB password → SecretProvider
2. [CRITICAL] Add TLS for patient data endpoint

### Phase 2: High (next sprint)
3. [HIGH] Extract business logic from OrderController → OrderService
4. [HIGH] Add fallback adapter for Redis with env toggle

### Phase 3: Medium (next quarter)
5. [MEDIUM] Add distributed tracing
6. [MEDIUM] Improve integration test coverage

### Phase 4: Low (backlog)
7. [LOW] Rename generic methods to domain terms
```

## Completion Criteria

- [ ] All 8 review areas assessed
- [ ] Findings prioritized by severity
- [ ] Each finding references a specific standard
- [ ] Each finding includes a remediation action with effort estimate
- [ ] Roadmap organized in implementation phases
