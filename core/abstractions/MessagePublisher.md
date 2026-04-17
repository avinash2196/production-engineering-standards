# MessagePublisher

## Purpose

Define the capability interface for publishing messages to topics/queues with explicit delivery semantics, idempotency, retry, and observability.

## Interface Contract

- `publish(topic, message, options)` — publishes a message to the specified topic.
- `publishBatch(topic, messages, options)` — publishes multiple messages atomically where supported by the underlying broker.
- Message structure: `{ body, attributes, idempotencyKey, traceId, correlationId, timestamp }`.
- `options` may include: `partitionKey`, `delaySeconds`, `headers`, `timeout`.

## Required Semantics

- **Delivery guarantee:** at-least-once. The publisher must retry on transient failures until the broker confirms receipt or max retries is exhausted.
- **Idempotency key:** every published message must carry an `idempotencyKey` (UUID or deterministic hash). The broker or consumer uses this for deduplication.
- **Ordering:** if ordering is required, the caller must provide a stable `partitionKey`. Document per-topic whether ordering matters.
- **Retry policy:** exponential backoff with jitter. Default: 3 retries, initial delay 200ms, max delay 5s. Configurable via `ConfigProvider`.
- **Timeout:** publish calls must have a timeout (default 10s). Exceeded timeout counts as a failure.

## Error Handling

- Transient errors (network, throttle) → retry according to policy.
- Permanent errors (serialization, topic not found) → fail immediately, log as ERROR with `traceId` and `correlationId`, emit metric.
- After max retries exhausted → throw a typed exception (e.g., `PublishFailedException`) and emit `<service>_publisher_errors_total{type="exhausted"}`.
- Never silently drop a message. The caller must know the publish failed.

## Observability

- Emit metrics: `<service>_publisher_messages_sent_total`, `<service>_publisher_send_duration_seconds`, `<service>_publisher_errors_total`, `<service>_publisher_retries_total`.
- Create a span for each publish call. Inject trace context into message headers so the subscriber can continue the trace.
- Include `correlationId` in all log lines during publish.

## Production vs Local Differences

- **Production:** Kafka, RabbitMQ, Azure Service Bus, SNS/SQS, etc. Full broker durability, partitioning, consumer groups.
- **Local / fallback (`FALLBACK_KAFKA=true`):** in-memory event bus or local file-based queue. No partitioning or durability. Messages lost on process restart. Acceptable for development only.
- Fallback mode must never be active in production. Enforce via startup validation.

## Java Example

```java
public interface MessagePublisher {
    void publish(String topic, Message message, PublishOptions options);
    void publishBatch(String topic, List<Message> messages, PublishOptions options);
}

@Component
@Profile("!fallback-kafka")
public class KafkaMessagePublisher implements MessagePublisher {
    // production Kafka implementation with retry, idempotency, tracing
}

@Component
@Profile("fallback-kafka")
public class InMemoryMessagePublisher implements MessagePublisher {
    // local-only in-memory implementation
}
```

## Python Example

```python
class MessagePublisher(Protocol):
    def publish(self, topic: str, message: Message, options: PublishOptions | None = None) -> None: ...
    def publish_batch(self, topic: str, messages: list[Message], options: PublishOptions | None = None) -> None: ...
```

## Relationship to MessageSubscriber

- `MessagePublisher` and `MessageSubscriber` share the same message contract (topic, body, attributes, `idempotencyKey`, `traceId`).
- See [MessageSubscriber.md](MessageSubscriber.md) for the consume side.
- See [standards/messaging-abstraction.md](../../standards/messaging-abstraction.md) for combined abstraction rules.

## LLM Instructions

- When scaffolding a publisher, always include an `idempotencyKey` on every message.
- Generate retry logic with exponential backoff and jitter.
- Inject trace context into message headers.
- Ask the user which broker is used before choosing the production implementation.
- Wire fallback via Spring profile or Python dependency injection.

## Review Checklist

- [ ] Every published message includes `idempotencyKey`.
- [ ] Retry policy configured with backoff and jitter.
- [ ] Timeout set on publish calls.
- [ ] Trace context injected into message headers.
- [ ] Metrics emitted for sent, errors, and retries.
- [ ] Fallback implementation exists for local development.
- [ ] Fallback cannot activate in production.
