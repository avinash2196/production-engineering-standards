# Messaging Local Adapters

## Purpose

Database-table-backed message queue replacement for local development when Kafka is unavailable. Activated by `MESSAGING_ADAPTER=db`. Implements `MessagePublisher` and `MessageSubscriber` interfaces using the service's existing database so messages survive restarts and can be inspected with SQL.

An in-memory local adapter (`MESSAGING_ADAPTER=inmemory`) is also available for ultra-minimal setups with no DB, but is not recommended — it loses messages on restart and cannot be inspected.

## Activation

| Environment | Toggle | Adapter selected |
|-------------|--------|---------------|
| Local dev (recommended) | `MESSAGING_ADAPTER=db` | DB table queue — persistent, inspectable |
| Local dev (no DB) | `MESSAGING_ADAPTER=inmemory` | In-memory queue — ephemeral |
| Staging | `kafka` or `pubsub` | Production adapter |
| Production | `kafka` or `pubsub` | Local values rejected |

**Startup validation:** if `MESSAGING_ADAPTER` is `db` or `inmemory` and the environment is production, fail startup with a clear error message. Production values such as `kafka` or `pubsub` remain valid.

## Behavior

### DB Table Implementation (Recommended — `MESSAGING_ADAPTER=db`)

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

**Schema (auto-created on startup when local adapter is active):**

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

### In-Memory Implementation (Local adapter of last resort — `MESSAGING_ADAPTER=inmemory`)

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

### DB table publisher (`MESSAGING_ADAPTER=db`)

```java
@Component
@ConditionalOnProperty(name = "adapters.messaging", havingValue = "db")
public class DbTableMessagePublisher implements MessagePublisher {
    private final JdbcTemplate jdbc;

    @Override
    public void publish(String topic, Message message, PublishOptions options) {
        jdbc.update(
            "INSERT INTO outbox_message (id, topic, payload, idempotency_key, trace_id, correlation_id, status, created_at) "
          + "VALUES (?, ?, ?::jsonb, ?, ?, ?, 'PENDING', NOW())",
            UUID.randomUUID(), topic, toJson(message),
            message.getIdempotencyKey(), message.getTraceId(), message.getCorrelationId());
        log.debug("[messaging-local-adapter:db] published topic={} key={}", topic, message.getIdempotencyKey());
        localAdapterActiveGauge.labels("kafka").set(1);
    }
}

@Component
@ConditionalOnProperty(name = "adapters.messaging", havingValue = "db")
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
                log.warn("[messaging-local-adapter:db] handler failed for id={}", row.id(), e);
            }
        }
    }
}
```

### In-memory publisher (`MESSAGING_ADAPTER=inmemory`)

```java
@Component
@ConditionalOnProperty(name = "adapters.messaging", havingValue = "inmemory")
public class InMemoryMessagePublisher implements MessagePublisher {
    private final Map<String, Queue<Message>> topics = new ConcurrentHashMap<>();

    @Override
    public void publish(String topic, Message message, PublishOptions options) {
        topics.computeIfAbsent(topic, k -> new ConcurrentLinkedQueue<>()).add(message);
        log.debug("[messaging-local-adapter:inmemory] published topic={} key={}", topic, message.getIdempotencyKey());
    }
}
```

## Python Example

### DB table publisher (`MESSAGING_ADAPTER=db`)

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
        logger.warning("local_adapter.active", adapter="messaging", mode="db", topic=topic)


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
                logger.warning("messaging_local_adapter_handler_failed", id=row.id, error=str(e))
            await self._db.commit()
```

### In-memory publisher (`MESSAGING_ADAPTER=inmemory`)

```python
class InMemoryMessagePublisher:
    def __init__(self):
        self._topics: dict[str, list[Message]] = defaultdict(list)

    async def publish(self, topic: str, message: Message, options=None) -> None:
        self._topics[topic].append(message)
        logger.debug("[messaging-local-adapter:inmemory] published", topic=topic, key=message.idempotency_key)
```

## Limitations

| Feature | Production Kafka | DB table local adapter | In-memory local adapter |
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

## What the Local Adapter Supports

- Publish/subscribe flow: messages published by one component are delivered to subscribers.
- Idempotency keys present on messages (consumers can test dedup logic).
- Handler invocation with message context (traceId, correlationId).
- Basic functional testing of message-driven workflows.

## What the Local Adapter Does Not Reproduce

- Multi-instance parallelism and partition assignment.
- Consumer group rebalancing.
- Dead-letter queue routing.
- Message replay from offsets.
- Backpressure and flow control.
- Production-grade observability metrics.

## LLM Instructions

- When an approved implementation plan includes a messaging local adapter, generate the **DB table implementation** (`MESSAGING_ADAPTER=db`) as the primary option.
- Add the in-memory implementation only when the approved plan explicitly needs a no-database local/CI path.
- Auto-create the `outbox_message` table on startup when `MESSAGING_ADAPTER=db` is active (use Flyway migration or `CREATE TABLE IF NOT EXISTS` on bean init).
- Wire via `@ConditionalOnProperty(name="adapters.messaging", havingValue="db")` (Spring) or `settings.messaging_adapter is MessagingAdapter.DB` (Python).
- Always add startup validation that fails if a local-only messaging value is selected in production.
- Emit a structured warning once at startup when the local adapter is active. When the project exposes application metrics, expose an adapter-active gauge/counter as well; do not emit activation warnings on every publish.
- Remind the user that neither local adapter reproduces consumer-group rebalancing or partition assignment.

## Review Checklist

- [ ] `MESSAGING_ADAPTER=db` is the preferred local adapter (not in-memory).
- [ ] `outbox_message` table is auto-created when `MESSAGING_ADAPTER=db` is active.
- [ ] Startup fails if a local-only messaging value is selected in production.
- [ ] Implements `MessagePublisher` and `MessageSubscriber` interfaces.
- [ ] Messages include `idempotencyKey`, `traceId`, `correlationId`.
- [ ] Failed messages set `status='FAILED'` — not silently dropped.
- [ ] Structured activation warning is emitted at startup; an adapter-active metric is exposed when the project has application metrics.
- [ ] Limitations documented and understood by team.
