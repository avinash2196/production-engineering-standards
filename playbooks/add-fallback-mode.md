# Workflow: Add Fallback Mode

## Purpose

Step-by-step procedure for adding a fallback adapter to an existing external dependency, enabling local development without the full infrastructure.

## Prerequisites

- Existing production adapter for the dependency (e.g., KafkaMessagePublisher, RedisCacheProvider)
- Capability abstraction interface already defined (or will be introduced as part of this workflow)

## Steps

### 1. Identify the Dependency

| Aspect | Value |
|--------|-------|
| Dependency | e.g., Kafka, Redis, S3, Vault |
| Existing adapter | e.g., `KafkaMessagePublisher` |
| Abstraction interface | e.g., `MessagePublisher` |
| Fallback toggle | e.g., `FALLBACK_KAFKA=db` |

If no abstraction interface exists yet, create one first (see `playbooks/refactor-module.md` step 5).

### 2. Define Fallback Behavior

Document how the fallback differs from production:

| Aspect | Production | Fallback |
|--------|-----------|----------|
| **Kafka** | Durable, multi-broker, partitioned | In-memory queue or file-backed FIFO. No replication. No consumer groups. |
| **Redis** | Distributed, multi-node, persistent | In-process LRU map with configurable TTL. Non-distributed. |
| **S3/Cloud Storage** | Cloud-managed, durable, encrypted | Local filesystem with configurable root. Sync flush. |
| **Vault/Secret Manager** | Managed secret store with rotation | Environment variables only. Security warning logged. |

Reference: `standards/fallback-strategy.md`

### 3. Implement Fallback Adapter

Create the fallback adapter implementing the same capability interface:

**Rules:**
- Implement every method of the abstraction interface
- Document behavior differences in javadoc/docstring (durability, ordering, consistency)
- Log a `WARN` on initialization: `"Fallback adapter active for <dependency> — not for production use"`
- Emit a metric: `<service>_fallback_active{dependency="<name>"}` gauge set to 1

**Java example structure:**
```java
@ConditionalOnProperty(name = "fallback.kafka", havingValue = "db")
public class DbTableMessagePublisher implements MessagePublisher {
    private final BlockingQueue<Message> queue = new LinkedBlockingQueue<>();
    // ...
}
```

**Python example structure:**
```python
class InMemoryMessagePublisher(MessagePublisher):
    def __init__(self):
        logger.warning("Fallback adapter active for Kafka — not for production use")
        self._queue: list[Message] = []
    # ...
```

### 4. Wire the Toggle

Configure the adapter selection based on the environment toggle:

- Toggle name: `FALLBACK_<DEPENDENCY>` (e.g., `FALLBACK_KAFKA=db`, `FALLBACK_CACHE=jsonfile`)
- Default: **disabled** (production adapter is the default)
- Toggle must be explicit — never auto-detect environment and silently switch
- Java: use `@ConditionalOnProperty` or `@Profile`
- Python: use factory function in dependency injection that reads the toggle

### 5. Add Telemetry

When fallback is active:

- [ ] `WARN` log on adapter initialization
- [ ] Gauge metric indicating fallback is active
- [ ] All operations still emit standard metrics (latency, errors) — fallback operations must be observable

### 6. Write Tests

- **Unit test** for fallback adapter: verify it implements the full interface contract
- **Integration test** for adapter selection: verify correct adapter is wired based on toggle value
- **Negative test**: verify fallback is NOT active when toggle is absent or false

### 7. Update Local Dev Docs

Update `playbooks/local-dev/run-with-fallbacks.md` and `.env.example`:

```bash
# .env.example
FALLBACK_KAFKA=db          # Use DB outbox table instead of Kafka (or inmemory for ephemeral)
FALLBACK_CACHE=jsonfile    # Use JSON file cache instead of Redis (or inmemory for ephemeral)
FALLBACK_STORAGE=local     # Use local filesystem instead of S3
FALLBACK_SECRETS=env       # Use environment variables instead of Vault
```

### 8. Verify Locally

```bash
# Enable fallback
export FALLBACK_KAFKA=db

# Start service
./gradlew bootRun  # or uvicorn main:app

# Verify WARN log appears: "Fallback adapter active for Kafka"
# Verify service operates normally with fallback
# Run tests
./gradlew test  # or pytest
```

## Completion Criteria

- [ ] Fallback adapter implements full capability interface
- [ ] Toggle-controlled with explicit env variable
- [ ] Default is production adapter (fallback OFF)
- [ ] WARN log and gauge metric on fallback activation
- [ ] Unit + integration tests for fallback adapter
- [ ] .env.example and local dev docs updated
- [ ] Fallback never silently weakens production guarantees
