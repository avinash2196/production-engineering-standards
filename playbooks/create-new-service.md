# Workflow: Create New Service

## Purpose

Step-by-step procedure for scaffolding a new backend service from scratch, ensuring it meets all enterprise-ai-engineering standards from day one.

## Prerequisites

- Stack decision made (Java Spring Boot or Python FastAPI)
- Service name and domain scope defined
- External dependencies identified (Kafka, Redis, S3, database, etc.)
- Compliance tier known (standard or HIPAA-aware)

## Steps

### 1. Scaffold the service — `/scaffold-service`

Type `/scaffold-service` in GitHub Copilot Chat. The agent will ask 10 questions in a single message:

| Question | Example answer |
|----------|---------------|
| Service name | `order-service` |
| Runtime target | `a) Local / on-prem` or `b) GCP` |
| Stack | `a) Java 21 + Spring Boot` or `b) Python 3.12 + FastAPI` |
| Messaging | `b) Kafka` (local) or `c) Pub/Sub` (GCP) or `a) none` |
| Cache | `b) Redis` (local) or `c) Memorystore` (GCP) or `a) none` |
| Object storage | `b) S3/MinIO` (local) or `c) GCS` (GCP) or `a) none` |
| Secrets | `a) Vault` (local) or `b) Secret Manager` (GCP) |
| Database | `a) PostgreSQL` or `b) Cloud SQL` or `c) none` |
| API style | `a) REST` or `b) event-driven` or `c) both` |
| Data classification | `a) public` / `b) internal` / `c) PII` / `d) PHI` |

After you answer, the agent prints a numbered plan (up to 24 files) and waits for your confirmation before writing anything. It then creates every file one by one, marking each step complete as it goes.

**What the scaffold produces automatically:**
- Layered package structure (controller → service → domain → repository)
- Capability abstraction interfaces wired for each selected dependency
- Production adapters + fallback adapters with env toggles
- Configuration classes using `ConfigProvider`
- Health, liveness, and readiness endpoints
- Dockerfile (multi-stage, non-root) + docker-compose.dev.yaml (local) or cloudbuild.yaml (GCP)
- `.env.local` with all `FALLBACK_*` toggles pre-set
- CI workflow: lint → test → build image → scan (Trivy)
- `docs/project-context.md` and `docs/integration-dependencies.md` pre-filled

### 2. Add or verify observability

The scaffold includes observability, but verify:

- Structured JSON logging with `correlationId`, `traceId`, `spanId`
- Prometheus metrics endpoint (`/actuator/prometheus` or `/metrics`)
- OpenTelemetry tracing configured via `OTEL_EXPORTER_OTLP_ENDPOINT`
- Correlation ID middleware/filter present

If anything is missing, run `/refactor-code` on the affected file.  
Reference: [standards/observability.md](../standards/observability.md)

### 3. Generate or review tests — `/generate-tests`

The scaffold includes test stubs. To generate or fill out a full test suite:

```
/generate-tests
```

Paste the service class file when prompted. The agent produces:
- Unit tests for the service layer with mocked capability abstractions
- Integration test stubs using Testcontainers (or fallback adapters for CI)
- Verifies tests pass with all `FALLBACK_*` toggles enabled

### 4. Review architecture — `/review-architecture`

```
/review-architecture
```

Paste key source files or the service folder. The agent verifies:

- [ ] Layered architecture correct (no cross-layer imports)
- [ ] No business logic in controllers
- [ ] Abstraction boundaries clean
- [ ] Domain model meaningful (not anemic)

### 5. Review production readiness (baseline) — `/review-production-readiness`

```
/review-production-readiness
```

At scaffold stage, expected results:

- Config externalization: ✅
- Observability: ✅
- Tests: ✅ (basic)
- Security: ⚠️ (auth not yet configured — expected at this stage)
- Resilience: ⚠️ (retries/timeouts may need tuning — expected at this stage)

### 6. Compliance check (if PHI/PII) — `/review-hipaa` or `/compliance-review`

If the service handles PHI, run:

```
/review-hipaa
```

If it handles PII or has internal compliance requirements:

```
/compliance-review
```

The agent verifies:
- Encryption controls in place
- Audit logging on PHI access
- Minimum necessary principle in API responses

### 7. Local verification

```bash
# Start local stack with fallbacks
docker-compose -f docker-compose.dev.yaml up -d

# Set fallback toggles
export FALLBACK_KAFKA=db
export FALLBACK_CACHE=jsonfile
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

### 8. Commit and document

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
