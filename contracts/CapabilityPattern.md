# Capability Boundary Pattern

## Purpose

Define when and how a service should isolate an external capability—messaging, cache, object storage, secrets, or dynamic configuration—behind an application-owned contract.

An interface is valuable when it protects a meaningful business, testing, portability, or policy boundary. It is not required merely to add another layer around a single SDK call.

## Pattern

```text
Application or domain decision
          |
          v
   Capability contract
      /           \
production adapter  explicit local adapter
```

Production and local implementations share the capability semantics that application code relies on, but they do not necessarily provide the same operational guarantees.

## Why Use It

- Unit tests can exercise business behavior without a live vendor dependency.
- Vendor-specific retries, serialization, connection handling, and telemetry remain in adapters.
- Local development can use an explicit substitute when an emulator or Testcontainer is not the better boundary.
- Policy such as secret handling, durability, or production guards has one composition point.

## Shared Contracts

| Capability | Contract | Production examples | Local examples |
|---|---|---|---|
| Messaging | `MessagePublisher`, `MessageSubscriber` | Kafka, Pub/Sub | database outbox/table queue, in-memory queue |
| Cache | `CacheProvider` | Redis | JSON-file cache, in-memory cache |
| Object storage | `ObjectStorageProvider` | S3, GCS | local filesystem |
| Secrets | `SecretProvider` | Vault, Secret Manager | environment variables |
| Configuration | `ConfigProvider` | managed configuration service | typed environment/file settings |

## Design Rules

1. Express the behavior the application needs, not the vendor API. Prefer `publish(message)` to exposing producer records throughout business code.
2. Document semantics: idempotency, ordering, TTL, not-found behavior, retries, timeouts, and error types.
3. Keep vendor SDK imports in infrastructure/composition code.
4. Add only implementations selected by the approved plan and implementation plan.
5. Treat local adapters as explicit development/testing choices, not automatic production failover.
6. Document differences in durability, consistency, concurrency, security, and observability.
7. Reject local-only values during production startup.
8. Test selection, contract behavior, and production guards before implementing the adapter.

## Java Composition Example

```java
@Configuration
class MessagingConfiguration {

    @Bean
    @ConditionalOnProperty(name = "adapters.messaging", havingValue = "db")
    MessagePublisher databaseOutboxPublisher(OutboxRepository outboxRepository) {
        return new DatabaseOutboxMessagePublisher(outboxRepository);
    }

    @Bean
    @ConditionalOnProperty(name = "adapters.messaging", havingValue = "kafka")
    MessagePublisher kafkaPublisher(KafkaTemplate<String, byte[]> kafkaTemplate) {
        return new KafkaMessagePublisher(kafkaTemplate);
    }
}
```

## Python Composition Example

```python
from app.config.settings import MessagingAdapter, Settings


def get_message_publisher(settings: Settings) -> MessagePublisher:
    if settings.messaging_adapter is MessagingAdapter.DB:
        return DatabaseOutboxMessagePublisher(
            SqlAlchemyOutboxStore(settings.database_url)
        )
    if settings.messaging_adapter is MessagingAdapter.IN_MEMORY:
        return InMemoryMessagePublisher()
    return KafkaMessagePublisher(settings.kafka_bootstrap_servers)
```

## Typed Selection

| Capability | Production values | Local-only values |
|---|---|---|
| `MESSAGING_ADAPTER` | `kafka`, `pubsub` | `db`, `inmemory` |
| `CACHE_ADAPTER` | `redis` | `jsonfile`, `inmemory` |
| `STORAGE_ADAPTER` | `s3`, `gcs` | `local` |
| `SECRET_ADAPTER` | `vault`, `secretmanager` | `env` |

Production validation rejects only the local-only values. It does not reject explicit production adapter values.

## Delivery Sequence

1. Plan the capability and required guarantees.
2. Create a repository-aware implementation plan listing contracts, adapters, configuration, and tests.
3. Write contract/selection/production-guard tests and confirm the expected failure.
4. Implement the minimum contract and selected adapters.
5. Run focused and integration tests.
6. Refactor composition and duplicate code only after green.

## Review Checklist

- [ ] The abstraction protects a concrete boundary rather than adding ceremony.
- [ ] Contract semantics and error behavior are documented.
- [ ] Only approved production/local implementations are present.
- [ ] Business code does not import vendor SDKs.
- [ ] Local adapters document lost guarantees and emit activation telemetry.
- [ ] Production startup rejects local-only selections.
- [ ] Tests prove selection and important contract behavior.
