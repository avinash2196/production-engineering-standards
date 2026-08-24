---
applyTo: "**/*.java"
description: "Apply Java and Spring Boot engineering guidance with controlled dependencies, constructor injection, test-first changes, and explicit production failure behavior."
---

Follow the applicable guidance in [Java and Spring standards](../../stacks/java-springboot/java-spring.md), [coding standards](../../standards/coding-standards.md), and the [prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md).

## Delivery Sequence

For non-trivial behavior changes:

1. work from an approved Plan containing separate RED and GREEN milestones; add a separate REFACTOR milestone only when justified;
2. create and obtain approval for the current phase-specific Implementation Plan;
3. during RED, change approved tests/checks only, verify valid RED, record evidence, and stop;
4. create and obtain approval for the separate GREEN Implementation Plan;
5. during GREEN, require predecessor RED evidence, implement the minimum approved Java/Spring behavior, run focused and relevant regression tests, and stop;
6. refactor only through a separately approved REFACTOR milestone from a verified GREEN baseline.

Do not expand scope, pull later dependencies forward, or mix unrelated cleanup into a behavior milestone. Do not advance to the next phase without its own reviewed Implementation Plan.

## Architecture Defaults

- **Controller/API**: Spring MVC or WebFlux transport handling, DTO binding, validation, authentication context, and response mapping.
- **Application service**: use-case orchestration and transaction ownership.
- **Domain**: business rules and value objects when complexity justifies them; avoid coupling business decisions to Spring or vendor SDKs.
- **Ports/contracts**: repository and external-capability abstractions where they protect a meaningful boundary.
- **Infrastructure adapters**: JPA/SQL, Kafka/Pub/Sub, Redis, object storage, and managed-secret implementations.

Use a simpler layered structure for straightforward CRUD when documented and testable. Do not create interfaces or folders solely to satisfy a diagram.

## Java Practices

- Prefer constructor injection. Do not use field injection.
- Use records for immutable request/response DTOs when they fit the API contract; classes are acceptable when framework or evolution needs justify them.
- Apply Bean Validation at the transport boundary and keep business-rule validation in application/domain code.
- Throw specific domain/application exceptions and map them through centralized exception handling.
- Use transactions around a coherent unit of work; do not hold database transactions open across slow remote calls without a documented reason.
- Treat method length, class size, nesting, and constructor size as review signals, not automatic failures. Refactor when responsibilities or testability demonstrate the need.
- Do not access Kafka, Redis, storage, or secret SDKs directly from controllers or domain logic.

## Adapter Selection

Select adapters in configuration/composition code using the adopting project's typed configuration model. The adapter names shown in this repository's local-adapter examples (`kafka`, `pubsub`, `db`, `inmemory`, `redis`, `jsonfile`, `s3`, `gcs`, `local`, `env`) are illustrative and must not create dependencies or configuration keys that the approved design does not require.

Local-only adapters must be explicit, document reduced guarantees, and be rejected by production startup or deployment validation. Add logging/metrics for activation when those signals are part of the project's operating model.

## Security and Observability

- Retrieve credentials through approved configuration/secret abstractions; never hardcode them.
- Use SLF4J with structured key-value or MDC context where it supports diagnosis.
- Add Micrometer metrics and tracing to critical service and external boundaries based on SLO/support needs.
- Avoid logging tokens, credentials, PII, PHI, or full sensitive payloads.
- Configure timeouts and explicit failure behavior for every remote dependency.

## Testing

- Unit-test application/domain decisions with JUnit 5 and Mockito/fakes without starting Spring unless framework behavior is under test.
- Use focused MVC/WebFlux tests for transport behavior.
- Use Testcontainers or an equivalent realistic environment for persistence and integration boundaries when needed.
- Prove local-adapter production guards and important retry, idempotency, rollback, and error behavior.
- Keep tests deterministic and assert behavior rather than internal call sequences unless the sequence is itself the contract.
