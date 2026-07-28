# MessagePublisher

## Purpose

Define the application-owned contract for publishing messages without coupling business code to Kafka, Pub/Sub, or a local implementation.

## Contract

A publisher should support the semantics selected by the approved plan, commonly:

```text
publish(topic, payload, key?, headers?)
```

Document:

- schema and compatibility policy;
- message key and ordering scope;
- idempotency/correlation identifiers;
- acknowledgement/durability expectation;
- timeout and retryable failures;
- behavior after retry exhaustion;
- transaction/outbox relationship.

Do not promise atomic batch publication unless the selected platform and implementation provide it.

## Failure Rules

- Never silently report success after a confirmed publish failure.
- Bound retries and use them only when the operation is safe to repeat.
- Translate vendor exceptions into stable application/infrastructure errors.
- When data loss is unacceptable, use an approved durable outbox/queue or fail the business operation according to its contract.

## Production and Local Implementations

| Selection | Use | Important guarantees |
|---|---|---|
| `kafka` / `pubsub` | production broker | platform-specific durability, partitioning, consumer behavior |
| `db` | local database outbox/table queue | restart persistence and SQL inspectability; no broker groups/rebalancing |
| `inmemory` | isolated tests | process-local and lost on restart |

Local-only selections are rejected in production.

## Composition Examples

```java
@Bean
@ConditionalOnProperty(name = "adapters.messaging", havingValue = "db")
MessagePublisher databasePublisher(OutboxRepository repository) {
    return new DatabaseOutboxMessagePublisher(repository);
}
```

```python
if settings.messaging_adapter is MessagingAdapter.DB:
    return DatabaseOutboxMessagePublisher(
        SqlAlchemyOutboxStore(settings.database_url)
    )
```

## Test-First Requirements

Before implementation, add tests for selected behavior such as:

- serialization and headers;
- provider selection and production guards;
- timeout/error translation;
- outbox persistence and rollback boundaries;
- duplicate/idempotency behavior;
- broker integration for the selected production adapter.

## Observability

Record useful publish success, failure, retry, and duration metrics. Propagate trace/correlation context without logging sensitive payloads. Emit a clear warning when a local adapter activates.

## Review Checklist

- [ ] Contract semantics match the approved plan
- [ ] Business code does not import the broker SDK
- [ ] Timeout and exhausted-failure behavior are explicit
- [ ] Idempotency and ordering requirements are documented
- [ ] Local adapter limitations and production guards are tested
- [ ] Relevant publish/outbox tests were written before code

## References

- [MessageSubscriber](MessageSubscriber.md)
- [Messaging abstraction](../standards/messaging-abstraction.md)
- [Messaging local adapters](../standards/fallbacks/kafka-fallback.md)
