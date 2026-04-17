# Messaging Abstraction

Purpose
- Define the `MessagePublisher` and `MessageSubscriber` capabilities and their expected semantics (ordering, durability, delivery guarantees).

Mandatory Rules
- Explicitly document delivery semantics: at-most-once, at-least-once, or exactly-once if supported.
- Message interfaces must include optional `idempotencyKey` and `traceId` fields to enable deduplication and correlation.
- Provide a local fallback adapter (file-backed or in-memory) for development and testing.

Defaults
- Default publish semantics: at-least-once with idempotency support in subscribers.
- Use topic/partition keys documented per event type for partitioned ordering.

Anti-patterns
- Tightly coupling event schemas to transport SDKs or embedding business logic in message handlers without transactional guarantees.

Abstraction Patterns
- Define a small contract: `publish(topic, message, attributes)` and `subscribe(topic, handler, options)` with ack/nack semantics.
- Handler contract must receive context including `traceId`, `attempt`, and `idempotencyKey`.

Production vs Local Differences
- Production: durable, multi-node brokers (Kafka, managed pub/sub) with retention and partitioning. Local: file-backed or ephemeral in-memory queues with no replication and weaker ordering guarantees.

LLM instructions
- When scaffolding message flows, generate a publisher adapter and a subscriber harness that enforces idempotency via `idempotencyKey` and durable checkpoints where possible.
- Ask the user if message ordering and cross-topic consistency are required before selecting a fallback strategy.

Review checklist
- [ ] Message contract includes `idempotencyKey` and `traceId`.
- [ ] Production and local adapters included and documented.
- [ ] Subscriber includes deduplication/ack semantics.
