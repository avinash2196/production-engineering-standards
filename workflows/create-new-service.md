# Workflow: Create New Service

## Purpose

Step-by-step procedure for scaffolding a new backend service from scratch, ensuring it meets all enterprise-ai-engineering standards from day one.

## Prerequisites

- Stack decision made (Java Spring Boot or Python FastAPI)
- Service name and domain scope defined
- External dependencies identified (Kafka, Redis, S3, database, etc.)
- Compliance tier known (standard or HIPAA-aware)

## Steps

### 1. Gather Inputs

Collect the following before generation:

| Input | Example |
|-------|---------|
| Service name | `order-service` |
| Stack | `java-springboot` |
| Domain entities | `Order`, `OrderItem`, `OrderStatus` |
| External dependencies | Kafka (events), Redis (cache), PostgreSQL (persistence) |
| Compliance tier | standard |

### 2. Scaffold Project Structure

Invoke **backend-service-builder** agent with gathered inputs. The agent generates:

- Layered package structure (controller → service → domain → repository)
- Capability abstraction interfaces wired for each external dependency
- Production adapters + fallback adapters with env toggles
- Configuration classes using `ConfigProvider`
- Health endpoint
- Dockerfile + docker-compose.dev.yaml
- `.env.example` with all required environment variables

### 3. Add Observability

Verify the scaffold includes (or add if missing):

- Structured JSON logging with `correlationId`, `traceId`, `spanId`
- Metrics registry with golden signal metrics (`_duration_seconds`, `_errors_total`, `_requests_total`)
- OpenTelemetry tracing configuration
- Correlation ID middleware/filter

Reference: `standards/observability.md` and `standards/observability/*.md`

### 4. Generate Initial Tests

Invoke **test-engineer** agent:

- Unit tests for service layer with mocked abstractions
- Integration test stubs for each adapter
- Verify tests run green with `FALLBACK_*` toggles enabled

### 5. Review Architecture

Invoke **architecture-reviewer** agent. Verify:

- [ ] Layered architecture correct
- [ ] No business logic in controllers
- [ ] Abstraction boundaries clean
- [ ] Domain model meaningful (not anemic)

### 6. Review Production Readiness (baseline)

Invoke **production-readiness-reviewer** agent. At scaffold stage, expect:

- Config externalization: ✅
- Observability: ✅
- Tests: ✅ (basic)
- Security: ⚠️ (auth not yet configured — expected)
- Resilience: ⚠️ (retries/timeouts may need tuning — expected)

### 7. Compliance Check (if HIPAA-aware)

Invoke **hipaa-reviewer** agent if the service handles PHI. Verify:

- PHI inventory documented
- Encryption controls in place
- Audit logging on PHI access
- Minimum necessary principle in API responses

### 8. Local Verification

```bash
# Start local stack with fallbacks
docker-compose -f docker-compose.dev.yaml up -d

# Set fallback toggles
export FALLBACK_KAFKA=true
export FALLBACK_CACHE=inmemory
export FALLBACK_STORAGE=local
export FALLBACK_SECRETS=env

# Run the service
./gradlew bootRun  # Java
# or
uvicorn main:app   # Python

# Run tests
./gradlew test     # Java
# or
pytest             # Python
```

### 9. Commit and Document

- Write `README.md` with service purpose, setup instructions, and architecture overview
- Create initial ADR (Architecture Decision Record) for key design choices
- Commit with conventional commit message: `feat: scaffold order-service`

## Completion Criteria

- [ ] Project structure follows layered architecture
- [ ] All external dependencies wrapped in capability abstractions
- [ ] Fallback adapters present with explicit env toggles
- [ ] Observability configured (logging, metrics, tracing)
- [ ] Unit and integration test stubs pass
- [ ] Service runs locally with fallback mode
- [ ] README and initial ADR committed
