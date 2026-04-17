# Core Principles

Non-negotiable engineering principles that govern all design and implementation decisions.

## Purpose

Establish a shared mental model across teams so that every service, library, and automation follows the same foundational values — regardless of stack, team, or domain.

## Principles

### 1. Abstraction over Implementation

All infrastructure access (messaging, caching, storage, secrets, config) flows through capability interfaces. No service directly instantiates an SDK client.

**Why:** Enables local development without infrastructure, zero-downtime provider swaps, and deterministic testing.

**Test:** Can you run `./mvnw test` or `pytest` with no Docker containers, network access, or cloud credentials? If not, you violated this principle.

### 2. Fail Open with Degradation

When a non-critical dependency is unavailable, the service continues operating at reduced fidelity using fallback implementations. Only the primary data store is a hard dependency.

**Why:** Partial service is better than total outage. Kafka down should not prevent HTTP requests from being served.

**Test:** Set `FALLBACK_KAFKA=true` and verify the service still starts, accepts requests, and queues events locally.

### 3. Observable by Default

Every service ships with structured logging, metrics (latency, error rate, throughput), distributed tracing, and health checks — without manual opt-in.

**Why:** You cannot fix what you cannot see. Production incidents correlate directly with observability gaps.

**Test:** Can you trace a single request across all services it touches using only the correlation ID?

### 4. Security as a Constraint, Not a Feature

Security controls (TLS, authentication, input validation, secrets management, least-privilege) are architectural constraints applied everywhere, not features added later.

**Why:** Retrofitting security is exponentially more expensive and error-prone than building it in.

**Test:** Can any service read secrets from environment variables in production? (Answer must be no — secrets come from `SecretProvider`.)

### 5. Convention over Configuration

Standard project structures, naming conventions, config resolution orders, and metric names reduce cognitive load and enable automation.

**Why:** Every bespoke choice is a decision that slows onboarding and breaks tooling.

**Test:** Can a new developer scaffold a service and have it compile, test, and deploy within one hour using the templates?

### 6. Test at the Right Level

Unit tests for business logic (fast, isolated). Integration tests for infrastructure wiring (Testcontainers). Contract tests for API boundaries. E2E tests for critical paths only.

**Why:** Over-testing at the wrong level creates slow, brittle suites that teams stop trusting.

**Test:** Does the test suite complete in under 5 minutes locally? Are flaky tests quarantined?

### 7. Immutable Deployments

Artifacts are built once and promoted through environments unchanged. Configuration varies per environment; code does not.

**Why:** "Works on my machine" must be eliminated. Environment parity prevents deployment surprises.

**Test:** Is the same container image SHA deployed to staging and production?

### 8. Least Knowledge

Each layer knows only what it needs. Controllers don't know about databases. Services don't know about HTTP status codes. Domain objects don't know about frameworks.

**Why:** Coupling spreads change impact. A database migration should not require controller changes.

**Test:** Can you swap PostgreSQL for a different data store by changing only the repository layer?

## Applying Principles

| When you're tempted to... | Apply this principle |
|---------------------------|---------------------|
| Call an S3 SDK directly from a service | #1 Abstraction over Implementation |
| Throw a 500 when Redis is down | #2 Fail Open with Degradation |
| Skip metrics "just for this service" | #3 Observable by Default |
| Store an API key in `application.yml` | #4 Security as a Constraint |
| Invent a new project layout | #5 Convention over Configuration |
| Write an E2E test for a utility function | #6 Test at the Right Level |
| Patch production config in-place | #7 Immutable Deployments |
| Import a controller class in a domain model | #8 Least Knowledge |

## LLM Instructions

- When generating code, verify each principle is satisfied before presenting the result.
- If a user asks for something that violates a principle (e.g., hardcoded secrets), explain the violation and offer the compliant alternative.
- When reviewing code, check principle adherence before style or performance.

## References

- [architecture.md](architecture.md)
- [Fallback strategy](../standards/fallback-strategy.md)
- [Security standards](../standards/security/security-standards.md)
- [Observability standard](../standards/observability.md)
