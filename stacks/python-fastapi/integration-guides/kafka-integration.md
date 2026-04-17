# Kafka Integration (Python FastAPI)

## Purpose

Step-by-step guide for wiring Apache Kafka into a FastAPI service through the `MessagePublisher` and `MessageSubscriber` capability interfaces using `aiokafka`, including async producer/consumer configuration, serialization, error handling, observability, and fallback setup.

## Dependencies

```txt
# requirements.txt
aiokafka>=0.10.0
pydantic>=2.0
prometheus-client>=0.20.0
opentelemetry-api>=1.24.0
opentelemetry-instrumentation-kafka>=0.45b0
```

## Producer Configuration

```python
# config/kafka.py
from pydantic_settings import BaseSettings

class KafkaSettings(BaseSettings):
    bootstrap_servers: str = "localhost:9092"
    acks: str = "all"
    retries: int = 3
    linger_ms: int = 5
    max_in_flight: int = 5
    idempotent: bool = True

    class Config:
        env_prefix = "KAFKA_"
```

## MessagePublisher Implementation

```python
# infrastructure/messaging/kafka_publisher.py
import json
from aiokafka import AIOKafkaProducer
from opentelemetry import trace
from core.abstractions import MessagePublisher, Message, PublishOptions

tracer = trace.get_tracer(__name__)

class KafkaMessagePublisher(MessagePublisher):
    def __init__(self, settings: KafkaSettings, metrics: MetricsCollector):
        self._producer: AIOKafkaProducer | None = None
        self._settings = settings
        self._metrics = metrics

    async def start(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._settings.bootstrap_servers,
            acks=self._settings.acks,
            enable_idempotence=self._settings.idempotent,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self._producer.start()

    async def stop(self):
        if self._producer:
            await self._producer.stop()

    async def publish(self, topic: str, message: Message, options: PublishOptions | None = None) -> None:
        with tracer.start_as_current_span("kafka-publish", attributes={"topic": topic}):
            headers = [
                ("idempotencyKey", message.idempotency_key.encode()),
                ("correlationId", message.correlation_id.encode()),
            ]
            try:
                await self._producer.send_and_wait(
                    topic,
                    key=options.partition_key.encode() if options and options.partition_key else None,
                    value=message.body,
                    headers=headers,
                )
                self._metrics.increment("publisher_messages_sent_total", tags={"topic": topic})
            except Exception as e:
                self._metrics.increment("publisher_errors_total", tags={"topic": topic})
                raise PublishFailedError(topic, message.idempotency_key) from e
```

## FastAPI Lifespan Integration

```python
# main.py
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    publisher = app.state.publisher
    subscriber = app.state.subscriber
    await publisher.start()
    await subscriber.start()
    yield
    await subscriber.stop()
    await publisher.stop()

app = FastAPI(lifespan=lifespan)
```

## MessageSubscriber Implementation

```python
# infrastructure/messaging/kafka_subscriber.py
import asyncio
from aiokafka import AIOKafkaConsumer
from core.abstractions import MessageSubscriber

class KafkaMessageSubscriber(MessageSubscriber):
    def __init__(self, settings: KafkaSettings, handler_registry: dict, metrics: MetricsCollector):
        self._settings = settings
        self._handlers = handler_registry  # {topic: async callable}
        self._consumer: AIOKafkaConsumer | None = None
        self._metrics = metrics
        self._task: asyncio.Task | None = None

    async def start(self):
        self._consumer = AIOKafkaConsumer(
            *self._handlers.keys(),
            bootstrap_servers=self._settings.bootstrap_servers,
            group_id=self._settings.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
        )
        await self._consumer.start()
        self._task = asyncio.create_task(self._consume_loop())

    async def _consume_loop(self):
        async for msg in self._consumer:
            headers = {k: v.decode() for k, v in msg.headers}
            idempotency_key = headers.get("idempotencyKey", "")

            if await self._dedup_store.exists(idempotency_key):
                await self._consumer.commit()
                continue

            handler = self._handlers.get(msg.topic)
            if handler:
                try:
                    await handler(msg.value, headers)
                    await self._dedup_store.mark(idempotency_key, ttl=86400)
                    await self._consumer.commit()
                    self._metrics.increment("subscriber_messages_processed_total")
                except Exception:
                    self._metrics.increment("subscriber_errors_total")
                    # message not committed — will be redelivered

    async def stop(self):
        if self._task:
            self._task.cancel()
        if self._consumer:
            await self._consumer.stop()
```

## Fallback Wiring

```python
# infrastructure/messaging/inmemory_publisher.py
from collections import defaultdict
from core.abstractions import MessagePublisher

class InMemoryMessagePublisher(MessagePublisher):
    """See core/fallbacks/kafka-fallback.md for full implementation."""
    def __init__(self):
        self._queues: dict[str, list] = defaultdict(list)

    async def publish(self, topic, message, options=None):
        self._queues[topic].append(message)
```

Activate via:
```bash
export FALLBACK_KAFKA=true
```

```python
# dependency injection
def get_publisher(settings: Settings) -> MessagePublisher:
    if settings.fallback_kafka:
        return InMemoryMessagePublisher()
    return KafkaMessagePublisher(settings.kafka, get_metrics())
```

## Observability

| Metric | Description |
|--------|-------------|
| `publisher_messages_sent_total` | Messages published by topic |
| `publisher_errors_total` | Publish failures by topic |
| `subscriber_messages_processed_total` | Messages consumed and handled |
| `subscriber_errors_total` | Consumer processing failures |

## Testing

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_publish_sends_to_kafka(mock_producer):
    publisher = KafkaMessagePublisher(settings, metrics)
    publisher._producer = mock_producer
    await publisher.publish("orders", Message(body={"id": "123"}, idempotency_key="k1"))
    mock_producer.send_and_wait.assert_called_once()
```

For integration tests with a real broker, use `testcontainers-python`:
```python
from testcontainers.kafka import KafkaContainer

@pytest.fixture(scope="module")
def kafka_container():
    with KafkaContainer() as kafka:
        yield kafka
```

## References

- [MessagePublisher.md](../../../core/abstractions/MessagePublisher.md)
- [MessageSubscriber.md](../../../core/abstractions/MessageSubscriber.md)
- [kafka-fallback.md](../../../core/fallbacks/kafka-fallback.md)
- [messaging-abstraction standard](../../../standards/messaging-abstraction.md)
