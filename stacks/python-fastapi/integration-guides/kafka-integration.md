# Messaging Integration — Python FastAPI

## Purpose

Wire Kafka or Pub/Sub behind the `MessagePublisher`/`MessageSubscriber` contracts while preserving an explicit database-backed or in-memory local adapter for approved development and test scenarios.

A database outbox is preferred locally when restart durability and SQL inspectability matter. It does not reproduce Kafka partitions, consumer groups, rebalancing, replay, or equivalent throughput.

## Required Workflow

1. Plan message semantics: topic, schema, key, ordering, idempotency, retry, and ownership.
2. Approve an implementation plan with exact files, migrations, tests, and rollout behavior.
3. Add failing tests for publisher selection, serialization, idempotency metadata, and production guards.
4. Implement the contract and selected adapter.
5. Run unit and broker/outbox integration tests.
6. Refactor only after green.

## Typed Configuration

```python
from enum import StrEnum


class MessagingAdapter(StrEnum):
    KAFKA = "kafka"
    PUBSUB = "pubsub"
    DB = "db"
    IN_MEMORY = "inmemory"
```

Production startup must reject `DB` and `IN_MEMORY`; it must allow `KAFKA` or `PUBSUB`.

## Contract

```python
from typing import Any, Protocol


class MessagePublisher(Protocol):
    async def publish(
        self,
        topic: str,
        message: Any,
        key: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None: ...
```

## Kafka Adapter

Keep `aiokafka` types in `infrastructure/messaging/`. Configure acknowledgements, bounded retries, idempotence, delivery timeout, and lifecycle start/stop. Include correlation and idempotency metadata without logging sensitive payloads.

```python
class KafkaMessagePublisher:
    def __init__(self, producer: AIOKafkaProducer) -> None:
        self._producer = producer

    async def publish(self, topic, message, key=None, headers=None) -> None:
        await self._producer.send_and_wait(
            topic,
            key=key.encode() if key else None,
            value=serialize(message),
            headers=encode_headers(headers or {}),
        )
```

## Database Outbox Local Adapter

The local implementation stores a record in an inspectable table:

```text
outbox_message(
  message_id, topic, message_key, payload_json,
  headers_json, status, created_at
)
```

Use the same database transaction as the business update when the outbox is part of a real durability design. For a local-only publisher test, at minimum verify that messages survive publisher recreation and remain queryable.

```python
if settings.messaging_adapter is MessagingAdapter.DB:
    return DatabaseOutboxMessagePublisher(
        SqlAlchemyOutboxStore(
            settings.database_url,
            table_name=settings.outbox_table_name,
        )
    )
```

`MESSAGING_ADAPTER=inmemory` is acceptable only for isolated tests that do not need restart durability or multi-process behavior.

## Consumer Requirements

Document and test:

- idempotency/deduplication key;
- commit/acknowledgement point;
- retry and dead-letter behavior;
- ordering scope;
- poison-message handling;
- shutdown and rebalance behavior;
- telemetry for lag, success, retry, and failure.

Do not mark a message processed before its required business transaction succeeds.

## Verification

- unit tests for serialization, metadata, and error translation;
- selection tests for `kafka`, `pubsub`, `db`, and `inmemory` as applicable;
- production guard tests for local-only values;
- Testcontainers/emulator test for the selected production broker;
- database integration test for outbox schema and persistence;
- duplicate delivery/idempotency test;
- startup/shutdown lifecycle test.

## References

- [MessagePublisher](../../../contracts/MessagePublisher.md)
- [MessageSubscriber](../../../contracts/MessageSubscriber.md)
- [Messaging local adapter detail](../../../standards/local-adapters/messaging-local-adapter.md)
- [Production dependency failure strategy](../../../standards/fallback-strategy.md)
