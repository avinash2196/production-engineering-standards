# Java Spring Boot Stack

Guidance, a minimal configuration/build skeleton, and integration notes for Java 21 and Spring Boot 3.x services.

## Delivery Workflow

Use the template only after approving a Plan that defines scope, risks, success criteria, and the required PDD phase milestones. For behavior-changing work, RED and GREEN are separate milestones. REFACTOR is also separate when justified.

Execute one approved milestone at a time:

1. **RED milestone** — approve a RED-specific Implementation Plan, add only the approved tests/test support, confirm the expected RED, record evidence, and stop.
2. **GREEN milestone** — after the predecessor RED evidence is approved, approve a GREEN-specific Implementation Plan, add only the minimum production changes required for GREEN, record evidence, and stop.
3. **REFACTOR milestone (optional)** — after GREEN, create and approve a separate REFACTOR Implementation Plan only when structural cleanup is justified; preserve behavior and keep tests GREEN.

Do not authorize RED, GREEN, and REFACTOR from one Implementation Plan, and do not advance into the next phase without its own reviewed plan.

## Base Template Status

`project-template/` contains only the minimum Spring Boot build/configuration foundation. It is not a complete runnable service. Application source plus database, messaging, cache, storage, security, observability, vendor, and local-adapter dependencies must be added only when selected by the approved current phase-specific Implementation Plan.

For an event-only service, do not add the web stack merely because it appears in another example. For a simple REST service, do not add Kafka, Redis, object storage, or managed-secret SDKs unless the service actually uses them.

## Suggested Structure

```text
src/main/java/<base-package>/
  api/                 controllers, DTO binding, response mapping
  application/         use-case orchestration and transaction ownership
  domain/              business rules and value objects where justified
  ports/               meaningful persistence/capability contracts
  infrastructure/
    messaging/          selected Kafka/Pub/Sub or local adapter
    cache/              selected Redis or local adapter
    storage/            selected S3/GCS or local adapter
    secrets/            selected managed/local secret provider
  config/               composition, typed properties, production guards
```

A straightforward CRUD service may use fewer packages when dependency direction remains controlled.

## Adapter Configuration

Define selectors only for capabilities the service actually uses. For example, a service that publishes messages may define:

```yaml
adapters:
  messaging: ${MESSAGING_ADAPTER:kafka}
```

A local profile may deliberately select a local implementation for that same capability:

```yaml
adapters:
  messaging: db
```

Add cache, storage, or secret selectors only when those capabilities are part of the approved design. Local-only selections must emit activation telemetry, document reduced guarantees, and fail startup in production. A database-backed queue/outbox and inspectable file cache are preferred over in-memory substitutes when restart behavior matters.

## Guides

| Guide | Focus |
|---|---|
| [Kafka Integration](integration-guides/kafka-integration.md) | publisher/consumer boundaries and messaging configuration |
| [Redis Integration](integration-guides/redis-integration.md) | cache policy and Redis integration |
| [Storage Integration](integration-guides/storage-integration.md) | object-storage behavior and local filesystem adapter |
| [Observability](observability.md) | Micrometer, tracing, logging, and health |

## References

- [Java/Spring guidance](java-spring.md)
- [Prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md)
- [Capability boundary pattern](../../contracts/CapabilityPattern.md)
- [Local adapter strategy](../../standards/local-adapter-strategy.md)
- [Production dependency failure strategy](../../standards/fallback-strategy.md)
