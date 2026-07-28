# Java Spring Boot Stack

Guidance, a configuration/build skeleton, and integration notes for Java 21 and Spring Boot 3.x services.

## Delivery Workflow

Use the template only after approving:

1. a Plan defining scope, milestones, risks, and success criteria;
2. an Implementation Plan defining exact files, tests, code approach, and exclusions.

Then add the first failing test, implement the minimum code for green, and refactor separately.

## Base Template Status

`project-template/` contains a Maven descriptor and configuration examples. It is **not a complete runnable service** because application source and selected adapters must come from the approved implementation plan.

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

```yaml
adapters:
  messaging: ${MESSAGING_ADAPTER:kafka}
  cache: ${CACHE_ADAPTER:redis}
  storage: ${STORAGE_ADAPTER:s3}
  secrets: ${SECRET_ADAPTER:vault}
```

A local profile may deliberately select:

```yaml
adapters:
  messaging: db
  cache: jsonfile
  storage: local
  secrets: env
```

Local-only selections must emit activation telemetry, document reduced guarantees, and fail startup in production. A database-backed queue/outbox and inspectable file cache are preferred over in-memory substitutes when restart behavior matters.

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
