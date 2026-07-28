# Run with Local Adapters

## Purpose

Run a service locally without every production dependency while keeping adapter selection explicit and preventing accidental production use.

Local adapters are not production failover mechanisms.

## Standard Selectors

| Variable | Local value | Behavior |
|---|---|---|
| `MESSAGING_ADAPTER` | `db` | Database-backed queue/outbox; persistent and inspectable |
| `MESSAGING_ADAPTER` | `inmemory` | Process-local queue; no restart durability |
| `CACHE_ADAPTER` | `jsonfile` | Inspectable file-backed cache |
| `CACHE_ADAPTER` | `inmemory` | Process-local cache |
| `STORAGE_ADAPTER` | `local` | Local filesystem |
| `SECRET_ADAPTER` | `env` | Environment-variable secret provider |

A service may support fewer values. Check its integration documentation.

## Java Spring Boot

```bash
MESSAGING_ADAPTER=db \
CACHE_ADAPTER=jsonfile \
STORAGE_ADAPTER=local \
SECRET_ADAPTER=env \
SPRING_PROFILES_ACTIVE=local \
./mvnw spring-boot:run
```

Configuration binds to:

```yaml
adapters:
  messaging: db
  cache: jsonfile
  storage: local
  secrets: env
```

Use `@ConfigurationProperties` and `@ConditionalOnProperty(name = "adapters.messaging", havingValue = "db")` or equivalent typed configuration. Do not rely on an unrelated profile or silent environment detection.

## Python FastAPI

```bash
MESSAGING_ADAPTER=db \
CACHE_ADAPTER=jsonfile \
STORAGE_ADAPTER=local \
SECRET_ADAPTER=env \
ENVIRONMENT=local \
uvicorn app.main:app --reload
```

Provider factories select from typed enum settings such as `settings.messaging_adapter`. Do not reference obsolete fallback fields.

## Example `.env.local`

```env
ENVIRONMENT=local
MESSAGING_ADAPTER=db
CACHE_ADAPTER=jsonfile
STORAGE_ADAPTER=local
SECRET_ADAPTER=env

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/service_db
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
REDIS_URL=redis://localhost:6379/0
LOCAL_STORAGE_PATH=./data/local-storage
```

Use only non-sensitive local credentials. Do not copy local files into production images.

## Reduced Guarantees

| Adapter | Preserved | Not equivalent to production |
|---|---|---|
| Database message queue | persistence, inspection, simple retry | broker partitioning, fan-out, consumer groups, global ordering |
| In-memory message queue | single-process publish/consume | durability and multi-instance coordination |
| JSON-file cache | basic get/put/evict and inspection | distributed atomicity and concurrent writers |
| In-memory cache | basic process-local caching | shared state and restart persistence |
| Local filesystem | basic put/get/delete | managed durability, encryption, lifecycle, multi-instance behavior |
| Environment secrets | key lookup | rotation, central audit, managed authorization |

## Verification

1. Run adapter contract and selector tests.
2. Start locally and confirm an explicit warning/metric identifies local adapters.
3. Verify production configuration rejects all local-only values.
4. Do not use local adapter behavior as proof of production broker/cache/storage semantics.

## References

- [Local Adapter Strategy](../../standards/local-adapter-strategy.md)
- [Production Dependency Failure and Degradation](../../standards/fallback-strategy.md)
- [Start Local Stack](start-local-stack.md)
