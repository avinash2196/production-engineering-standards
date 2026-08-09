# Messaging Integration — Java Spring Boot

## Purpose

Implement Kafka or Pub/Sub behind `MessagePublisher`/`MessageSubscriber`, with an explicit database-backed or in-memory local adapter only when approved.

A database outbox/table queue is useful locally because it survives process restarts and is inspectable with SQL. It does not reproduce broker partitions, consumer groups, rebalancing, replay, or production throughput.

## Delivery Sequence

1. Plan topic/schema, key, ordering, idempotency, acknowledgement, retry, and transaction ownership.
2. Approve exact files, migrations, tests, and rollout behavior in the Implementation Plan.
3. Add failing tests for selection, serialization, headers, outbox behavior, and production guards.
4. Implement the minimum contract and selected adapter.
5. Run unit and Testcontainers/broker integration tests.
6. Refactor after green.

## Configuration

```yaml
adapters:
  messaging: ${MESSAGING_ADAPTER:kafka}
```

Use `kafka` or `pubsub` for production. `db` and `inmemory` are local-only and must fail startup in production.

## Composition

```java
@Configuration
@EnableConfigurationProperties(AdapterProperties.class)
class MessagingConfiguration {

    @Bean
    @ConditionalOnProperty(name = "adapters.messaging", havingValue = "kafka")
    MessagePublisher kafkaPublisher(KafkaTemplate<String, byte[]> template) {
        return new KafkaMessagePublisher(template);
    }

    @Bean
    @ConditionalOnProperty(name = "adapters.messaging", havingValue = "db")
    MessagePublisher databasePublisher(OutboxRepository repository) {
        return new DatabaseOutboxMessagePublisher(repository);
    }
}
```

Prefer `@ConfigurationProperties`/validated enums over unrelated Spring profiles. Validate local-only values against the environment during startup.

## Publisher Requirements

- broker acknowledgements and delivery timeout;
- bounded retries safe for idempotency;
- stable key/ordering scope;
- correlation and idempotency metadata;
- typed exhausted-failure behavior;
- outbox when business data and event durability must be atomic.

## Subscriber Requirements

- acknowledge only after the required transaction succeeds;
- idempotent processing/deduplication;
- bounded retry and terminal/dead-letter behavior;
- explicit ordering and concurrency;
- graceful shutdown/rebalance handling;
- lag, duplicate, retry, failure, and duration signals.

## Verification

- JUnit tests for contract behavior and error translation;
- configuration-selection and production-guard tests;
- repository integration tests for the DB outbox;
- Testcontainers Kafka tests for the selected production adapter;
- duplicate-delivery and failed-transaction tests;
- lifecycle start/stop tests.

## References

- [MessagePublisher](../../../contracts/MessagePublisher.md)
- [MessageSubscriber](../../../contracts/MessageSubscriber.md)
- [Messaging local adapters](../../../standards/local-adapters/messaging-local-adapter.md)
- [Production dependency failure strategy](../../../standards/fallback-strategy.md)
