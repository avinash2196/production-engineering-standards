# Engineering Principles

Non-negotiable engineering principles that govern all design and implementation decisions in this repository. Mandatory for any team scaffolding services from the `enterprise-ai-engineering` templates.

## Principles

### 1. Abstraction over Implementation

All infrastructure access (messaging, caching, storage, secrets, config) flows through capability interfaces (`MessagePublisher`, `CacheProvider`, `ObjectStorageProvider`, `SecretProvider`, `ConfigProvider`). No service directly instantiates an SDK client.

**Why:** Enables local development without infrastructure, zero-downtime provider swaps, and deterministic testing.

**Test:** Can you run `./mvnw test` or `pytest` with no Docker containers, network access, or cloud credentials? If not, you violated this principle.

### 2. Fail Open with Degradation

When a non-critical dependency is unavailable, the service continues operating at reduced fidelity using fallback implementations. Only the primary data store is a hard dependency. Fallbacks are enabled explicitly by environment variables (e.g., `FALLBACK_KAFKA=db`, `FALLBACK_CACHE=jsonfile`) and must never be implicitly used in production.

**Why:** Partial service is better than total outage. Kafka down should not prevent HTTP requests from being served.

**Test:** Set `FALLBACK_KAFKA=db` and verify the service still starts, accepts requests, and persists events to the `outbox_message` table.

### 3. Observable by Default

Every service ships with structured logging, metrics (latency, error rate, throughput), distributed tracing, and health checks — without manual opt-in.

**Why:** You cannot fix what you cannot see. Production incidents correlate directly with observability gaps.

**Test:** Can you trace a single request across all services it touches using only the correlation ID?

### 4. Security as a Constraint, Not a Feature

Security controls (TLS, authentication, input validation, secrets management, least-privilege) are architectural constraints applied everywhere, not features added later. No hardcoded secrets. Implement audit logging for operations involving sensitive data.

**Why:** Retrofitting security is exponentially more expensive and error-prone than building it in.

**Test:** Can any service read secrets from environment variables in production? (Answer must be no — secrets come from `SecretProvider`.)

### 5. Convention over Configuration

Standard project structures, naming conventions, config resolution orders, and metric names reduce cognitive load and enable automation. Configuration sources follow the precedence defined in `rule-precedence.md`.

**Why:** Every bespoke choice is a decision that slows onboarding and breaks tooling.

**Test:** Can a new developer scaffold a service and have it compile, test, and deploy within one hour using the templates?

### 6. Test at the Right Level

Unit tests for business logic (fast, isolated). Integration tests for infrastructure wiring (Testcontainers). Contract tests for API boundaries. E2E tests for critical paths only. Design for batching, caching, and efficient DB access.

**Why:** Over-testing at the wrong level creates slow, brittle suites that teams stop trusting.

**Test:** Does the test suite complete in under 5 minutes locally? Are flaky tests quarantined?

### 7. Immutable Deployments

Artifacts are built once and promoted through environments unchanged. Configuration varies per environment; code does not.

**Why:** "Works on my machine" must be eliminated. Environment parity prevents deployment surprises.

**Test:** Is the same container image SHA deployed to staging and production?

### 8. Least Knowledge

Each layer knows only what it needs. Enforce controller → service → domain → repository layering. Controllers only orchestrate request validation and mapping to service calls.

**Why:** Coupling spreads change impact. A database migration should not require controller changes.

**Test:** Can you swap PostgreSQL for a different data store by changing only the repository layer?

### 9. Distributed-Ready by Default

Implement retries, timeouts, idempotency keys, and clear async/sync boundaries. Cloud integrations must have local-safe fallbacks so the service runs in development without cloud accounts.

**Why:** Services run in distributed environments. Single-node assumptions cause production failures.

**Test:** Does every outbound call have a configured timeout and retry policy?

### 10. Agent Interaction

Agents must ask targeted questions only when the repository's defined defaults cannot safely resolve design choices.

**Why:** Unnecessary questions slow down development and undermine the value of the templates.

**See:** `questioning-policy.md` for rules.

## Quick Reference

| When you're tempted to... | Apply this principle |
|---|---|
| Call an S3 SDK directly from a service | #1 Abstraction over Implementation |
| Throw a 500 when Redis is down | #2 Fail Open with Degradation |
| Skip metrics "just for this service" | #3 Observable by Default |
| Store an API key in `application.yml` | #4 Security as a Constraint |
| Invent a new project layout | #5 Convention over Configuration |
| Write an E2E test for a utility function | #6 Test at the Right Level |
| Patch production config in-place | #7 Immutable Deployments |
| Import a controller class in a domain model | #8 Least Knowledge |
| Make a synchronous call with no timeout | #9 Distributed-Ready by Default |
| Ask the user which database to use when a default exists | #10 Agent Interaction |

## LLM Instructions

- When generating code, verify each principle is satisfied before presenting the result.
- If a user asks for something that violates a principle (e.g., hardcoded secrets), explain the violation and offer the compliant alternative.
- When reviewing code, check principle adherence before style or performance.

## References

- [architecture.md](architecture.md) — layered architecture standard
- [fallback-strategy.md](fallback-strategy.md) — fallback rules and toggles
- [standards/security/](security/) — security standards
- [standards/observability.md](observability.md) — observability standard
- [contracts/](../contracts/) — capability interface specifications
