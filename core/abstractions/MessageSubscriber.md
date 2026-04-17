# MessageSubscriber

Purpose
- Define the capability interface for consuming messages from topics/queues with explicit delivery semantics, deduplication, and observability.

Interface Contract
- `subscribe(topic, handler, options)` — registers a handler for messages on a topic.
- Handler signature: `handler(message, context)` where context includes `traceId`, `correlationId`, `attempt`, `idempotencyKey`, and `timestamp`.
- `ack(message)` / `nack(message, reason)` — explicit acknowledgment required; no auto-ack by default.

Required Semantics
- **Delivery guarantee:** at-least-once by default; subscribers must be idempotent.
- **Deduplication:** subscribers must check `idempotencyKey` against a local or shared dedup store before processing. Duplicate messages must be acked silently.
- **Ordering:** document per-topic whether ordering is required. If ordering is required, bind to a single partition key.
- **Retry:** failed messages (nack) must be retried with exponential backoff up to a configurable max attempts, then routed to a dead-letter topic/queue.

Error Handling
- Handler exceptions must be caught, logged with `traceId` and `correlationId`, recorded as a span error, and the message must be nacked.
- After max retries, publish the message to a dead-letter topic and emit a metric (`<service>_subscriber_deadletter_total`).

Observability
- Emit metrics: `<service>_subscriber_messages_received_total`, `<service>_subscriber_processing_duration_seconds`, `<service>_subscriber_errors_total`.
- Extract trace context from message headers and create a child span for processing.
- Include `correlationId` in all log lines during message handling.

Production vs Local Differences
- **Production:** durable consumer groups with offset/checkpoint management, multi-instance parallelism, dead-letter routing.
- **Local/fallback:** in-memory or file-backed queue consumer. No consumer groups; single-instance only. Dead-letter writes to a local file.

Relationship to MessagePublisher
- `MessagePublisher` and `MessageSubscriber` share the same message contract (topic, message body, attributes including `idempotencyKey` and `traceId`).
- See [MessagePublisher.md](MessagePublisher.md) for the publish side.
- See [standards/messaging-abstraction.md](../../standards/messaging-abstraction.md) for the combined abstraction rules.

LLM instructions
- When scaffolding a subscriber, generate an idempotent handler with dedup check, ack/nack, dead-letter routing, and trace context extraction.
- Ask the user if ordering or consumer-group semantics are required before choosing implementation.

Review checklist
- [ ] Handler includes `idempotencyKey` deduplication.
- [ ] Explicit ack/nack with dead-letter routing on max retries.
- [ ] Trace context extracted from message headers.
- [ ] Metrics emitted for received, processed, and errored messages.
