# Java Spring Boot Stack

Opinionated starter templates and integration guides for Java 21 + Spring Boot 3.x services.

## Stack Requirements

| Component | Version |
|-----------|---------|
| Java | 21 LTS |
| Spring Boot | 3.2+ |
| Build tool | Maven (Gradle acceptable) |
| Container base | Eclipse Temurin 21-jre-alpine |

## Project Structure

```
src/main/java/com/myorg/{service}/
├── controller/          # REST endpoints — thin, delegates to service
├── service/             # Business logic — orchestrates domain + infra
├── domain/              # Value objects, entities, domain events
├── repository/          # Data access (JPA, JDBC)
├── infrastructure/      # Capability interface implementations
│   ├── messaging/       # KafkaMessagePublisher, KafkaMessageSubscriber
│   ├── cache/           # RedisCacheProvider
│   ├── storage/         # S3ObjectStorageProvider
│   ├── config/          # Config provider wiring
│   └── fallback/        # In-memory / local fallback beans
└── config/              # Spring @Configuration classes
```

See [java-spring.md](java-spring.md) for full architecture, abstractions, and coding conventions.

## Guides

| Guide | Description |
|-------|-------------|
| [Kafka Integration](integration-guides/kafka-integration.md) | Producer/consumer with `MessagePublisher` / `MessageSubscriber` |
| [Redis Integration](integration-guides/redis-integration.md) | Caching with `CacheProvider` |
| [Storage Integration](integration-guides/storage-integration.md) | Object storage with `ObjectStorageProvider` |
| [Observability](observability.md) | Micrometer, OpenTelemetry, logging, health checks |

## Quick Start

```bash
# Clone the template
cp -r project-templates/java-springboot my-new-service
cd my-new-service

# Build
./mvnw clean verify

# Run locally with fallbacks (no infra needed)
FALLBACK_KAFKA=db FALLBACK_CACHE=jsonfile FALLBACK_STORAGE=local \
  ./mvnw spring-boot:run -Dspring-boot.run.profiles=local
```

## Capability Interface Mapping

| Abstraction | Production Bean | Fallback Bean |
|-------------|-----------------|---------------|
| `MessagePublisher` | `KafkaMessagePublisher` | `InMemoryMessagePublisher` |
| `MessageSubscriber` | `KafkaMessageSubscriber` | `InMemoryMessageSubscriber` |
| `CacheProvider` | `RedisCacheProvider` | `InMemoryCacheProvider` |
| `ObjectStorageProvider` | `S3ObjectStorageProvider` | `LocalFileStorageProvider` |
| `SecretProvider` | `VaultSecretProvider` | `EnvSecretProvider` |
| `ConfigProvider` | `CompositeConfigProvider` | same (env + file fallback) |

Fallback activation is controlled via environment variables and Spring `@Profile` annotations.

## References

- [java-spring.md](java-spring.md) — Full stack conventions
- [Contracts](../../contracts/)
- [Fallback strategy](../../standards/fallback-strategy.md)
- [Observability standard](../../standards/observability.md)
