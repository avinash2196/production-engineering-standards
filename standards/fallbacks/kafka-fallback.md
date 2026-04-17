# Kafka Fallback

## Purpose

Database-table-backed message queue replacement for local development when Kafka is unavailable. Activated by `FALLBACK_KAFKA=db`. Implements `MessagePublisher` and `MessageSubscriber` interfaces using the service's existing database so messages survive restarts and can be inspected with SQL.

An in-memory fallback (`FALLBACK_KAFKA=inmemory`) is also available for ultra-minimal setups with no DB, but is not recommended — it loses messages on restart and cannot be inspected.

## Activation

| Environment | Toggle | Fallback used |
|-------------|--------|---------------|
| Local dev (recommended) | `FALLBACK_KAFKA=db` | DB table queue — persistent, inspectable |
| Local dev (no DB) | `FALLBACK_KAFKA=inmemory` | In-memory queue — ephemeral |
| Staging | Must be unset | No fallback |
| Production | Must be unset | **Never** |

**Startup validation:** if `FALLBACK_KAFKA` is set to any value and the environment is production, fail startup with a clear error message.

## Behavior

### DB Table Implementation (Recommended — `FALLBACK_KAFKA=db`)

Uses two tables in the service's existing local database (`outbox_message` and `outbox_consumer_offset`) so messages survive restarts and are readable via SQL.

```
Publisher.publish(topic, message)
    → INSERT INTO outbox_message (id, topic, payload, idempotency_key, trace_id, created_at, status)
       VALUES (..., 'PENDING')

Subscriber poll (every 200ms)
    → SELECT * FROM outbox_message
        WHERE topic = ? AND status = 'PENDING'
        ORDER BY created_at ASC
        LIMIT 50
    → invoke handler per row
    → UPDATE outbox_message SET status = 'PROCESSED' WHERE id = ?
    → on nack: UPDATE outbox_message SET status = 'FAILED', retry_count = retry_count + 1 WHERE id = ?
```

**Schema (auto-created on startup when fallback is active):**

```sql
CREATE TABLE IF NOT EXISTS outbox_message (
    id              UUID PRIMARY KEY,
    topic           VARCHAR(255) NOT NULL,
    payload         TEXT NOT NULL,          -- JSON serialised message
    idempotency_key VARCHAR(255),
    trace_id        VARCHAR(64),
    correlation_id  VARCHAR(64),
    status          VARCHAR(16) DEFAULT 'PENDING',  -- PENDING | PROCESSED | FAILED
    retry_count     INT DEFAULT 0,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    processed_at    TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_outbox_topic_status ON outbox_message (topic, status, created_at);
```

- Survives process restart — messages are in the DB.
- Inspectable with SQL: `SELECT * FROM outbox_message WHERE status = 'PENDING';`
- Works with multi-instance local setups (shared DB).
- Failed messages accumulate with `status = 'FAILED'` — no silent dropping.
- Ordering: FIFO per topic.

### In-Memory Implementation (Fallback of last resort — `FALLBACK_KAFKA=inmemory`)

Use only when no database is available at all.

```
Publisher.publish(topic, message)
    → stores message in ConcurrentLinkedQueue per topic (JVM heap)

Subscriber.subscribe(topic, handler)
    → background thread polls the queue every 100ms, invokes handler
```

- Messages lost on restart.
- Single JVM process only.
- No dead-letter routing — nacked messages are logged and dropped.
- Use only for smoke tests or truly no-infra CI.

## Java Example

### DB table publisher (`FALLBACK_KAFKA=db`)

```java
@Component
@ConditionalOnProperty(name = "fallback.kafka", havingValue = "db")
public class DbTableMessagePublisher implements MessagePublisher {
    private final JdbcTemplate jdbc;

    @Override
    public void publish(String topic, Message message, PublishOptions options) {
        jdbc.update(
            "INSERT INTO outbox_message (id, topic, payload, idempotency_key, trace_id, correlation_id, status, created_at) "
          + "VALUES (?, ?, ?::jsonb, ?, ?, ?, 'PENDING', NOW())",
            UUID.randomUUID(), topic, toJson(message),
            message.getIdempotencyKey(), message.getTraceId(), message.getCorrelationId());
        log.debug("[kafka-fallback:db] published topic={} key={}", topic, message.getIdempotencyKey());
        fallbackActiveGauge.labels("kafka").set(1);
    }
}

@Component
@ConditionalOnProperty(name = "fallback.kafka", havingValue = "db")
public class DbTableMessageSubscriber implements MessageSubscriber {
    @Scheduled(fixedDelay = 200)
    public void poll() {
        List<OutboxRow> rows = jdbc.query(
            "SELECT * FROM outbox_message WHERE topic = ? AND status = 'PENDING' "
          + "ORDER BY created_at ASC LIMIT 50",
            rowMapper, topic);
        for (OutboxRow row : rows) {
            try {
                handler.handle(row.toMessage());
                jdbc.update("UPDATE outbox_message SET status='PROCESSED', processed_at=NOW() WHERE id=?", row.id());
            } catch (Exception e) {
                jdbc.update("UPDATE outbox_message SET status='FAILED', retry_count=retry_count+1 WHERE id=?", row.id());
                log.warn("[kafka-fallback:db] handler failed for id={}", row.id(), e);
            }
        }
    }
}
```

### In-memory publisher (`FALLBACK_KAFKA=inmemory`)

```java
@Component
@ConditionalOnProperty(name = "fallback.kafka", havingValue = "inmemory")
public class InMemoryMessagePublisher implements MessagePublisher {
    private final Map<String, Queue<Message>> topics = new ConcurrentHashMap<>();

    @Override
    public void publish(String topic, Message message, PublishOptions options) {
        topics.computeIfAbsent(topic, k -> new ConcurrentLinkedQueue<>()).add(message);
        log.debug("[kafka-fallback:inmemory] published topic={} key={}", topic, message.getIdempotencyKey());
    }
}
```

## Python Example

### DB table publisher (`FALLBACK_KAFKA=db`)

```python
class DbTableMessagePublisher:
    def __init__(self, db: AsyncSession, metrics: MetricsProvider):
        self._db = db
        self._metrics = metrics

    async def publish(self, topic: str, message: Message, options=None) -> None:
        await self._db.execute(
            text("""
                INSERT INTO outbox_message
                    (id, topic, payload, idempotency_key, trace_id, correlation_id, status, created_at)
                VALUES (:id, :topic, :payload, :idem_key, :trace_id, :corr_id, 'PENDING', NOW())
            """),
            {
                "id": str(uuid4()), "topic": topic,
                "payload": message.model_dump_json(),
                "idem_key": message.idempotency_key,
                "trace_id": message.trace_id, "corr_id": message.correlation_id,
            }
        )
        await self._db.commit()
        logger.warning("fallback.active", fallback="kafka", mode="db", topic=topic)


class DbTableMessageSubscriber:
    async def poll(self) -> None:
        rows = await self._db.execute(
            text("SELECT * FROM outbox_message WHERE topic=:topic AND status='PENDING' "
                 "ORDER BY created_at ASC LIMIT 50"),
            {"topic": self._topic}
        )
        for row in rows:
            try:
                await self._handler(Message.from_row(row))
                await self._db.execute(
                    text("UPDATE outbox_message SET status='PROCESSED', processed_at=NOW() WHERE id=:id"),
                    {"id": row.id})
            except Exception as e:
                await self._db.execute(
                    text("UPDATE outbox_message SET status='FAILED', retry_count=retry_count+1 WHERE id=:id"),
                    {"id": row.id})
                logger.warning("kafka_fallback_handler_failed", id=row.id, error=str(e))
            await self._db.commit()
```

### In-memory publisher (`FALLBACK_KAFKA=inmemory`)

```python
class InMemoryMessagePublisher:
    def __init__(self):
        self._topics: dict[str, list[Message]] = defaultdict(list)

    async def publish(self, topic: str, message: Message, options=None) -> None:
        self._topics[topic].append(message)
        logger.debug("[kafka-fallback:inmemory] published", topic=topic, key=message.idempotency_key)
```

## Limitations

| Feature | Production Kafka | DB table fallback | In-memory fallback |
|---------|-----------------|-------------------|--------------------|
| Durability | Replicated, persistent | Yes — in DB rows | None — lost on restart |
| Inspectable | Kafka UI / consumer lag | Yes — `SELECT * FROM outbox_message` | No |
| Partitioning | Yes | No | No |
| Consumer groups | Yes | No (single poller) | No |
| Ordering guarantees | Per-partition | FIFO per topic | FIFO per topic |
| Dead-letter routing | Yes | Failed rows with `status='FAILED'` | No (log and drop) |
| Multi-instance | Yes | Yes (shared DB) | No |
| Backpressure | Yes | Partial (poll limit) | No |
| Observability | Full metrics | Row counts + logging | Basic logging only |

## What Works in Fallback

- Publish/subscribe flow: messages published by one component are delivered to subscribers.
- Idempotency keys present on messages (consumers can test dedup logic).
- Handler invocation with message context (traceId, correlationId).
- Basic functional testing of message-driven workflows.

## What Does NOT Work in Fallback

- Multi-instance parallelism and partition assignment.
- Consumer group rebalancing.
- Dead-letter queue routing.
- Message replay from offsets.
- Backpressure and flow control.
- Production-grade observability metrics.

## LLM Instructions

- When scaffolding a fallback for messaging, generate the **DB table implementation** (`FALLBACK_KAFKA=db`) as the primary option.
- Also generate the in-memory implementation as a secondary option for no-infra CI.
- Auto-create the `outbox_message` table on startup when `FALLBACK_KAFKA=db` is active (use Flyway migration or `CREATE TABLE IF NOT EXISTS` on bean init).
- Wire via `@ConditionalOnProperty(name="fallback.kafka", havingValue="db")` (Spring) or `settings.fallback_kafka == "db"` (Python).
- Always add startup validation that fails if `FALLBACK_KAFKA` is set in production.
- Emit `fallbackActiveGauge.labels("kafka").set(1)` and a structured `logger.warning` on every publish when fallback is active.
- Remind the user that neither fallback tests consumer group rebalancing or partition assignment.

## Review Checklist

- [ ] `FALLBACK_KAFKA=db` is the default local fallback (not in-memory).
- [ ] `outbox_message` table is auto-created when `FALLBACK_KAFKA=db` is active.
- [ ] Startup fails if `FALLBACK_KAFKA` is set in production.
- [ ] Implements `MessagePublisher` and `MessageSubscriber` interfaces.
- [ ] Messages include `idempotencyKey`, `traceId`, `correlationId`.
- [ ] Failed messages set `status='FAILED'` — not silently dropped.
- [ ] Fallback active metric and structured warning emitted on every publish in fallback mode.
- [ ] Limitations documented and understood by team.
