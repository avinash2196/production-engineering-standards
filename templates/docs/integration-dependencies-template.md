# Integration Dependencies Template
<!--
  HOW TO USE:
  Copy to docs/integration-dependencies.md (or <service>/docs/dependencies.md).
  Fill in one row per external dependency. Keep the fallback column current.
  See: playbooks/create-doc.md for full process.
-->

# Integration Dependencies: [SERVICE NAME]

**Owner:** [Team]  
**Last updated:** YYYY-MM-DD

## Runtime Dependencies

| Dependency | Purpose | Required version | Protocol | Fallback |
|------------|---------|-----------------|----------|----------|
| PostgreSQL | Primary data store | 15.x | TCP/5432 | None — hard dependency |
| Kafka | Domain event publishing | 3.x | TCP/9092 | `FALLBACK_KAFKA=db` — DB outbox table |
| Redis | Response cache | 7.x | TCP/6379 | `FALLBACK_CACHE=jsonfile` — local JSON file |
| S3 / Cloud Storage | Document storage | AWS S3 API | HTTPS | `FALLBACK_STORAGE=local` — local filesystem |
| Vault | Secrets | 1.14+ | HTTPS/8200 | `FALLBACK_SECRETS=env` — env variables |
| [Downstream service] | [Purpose] | [Version] | HTTP/gRPC | [no fallback / degrade gracefully] |

## Startup Validation

<!--
  Services must fail fast at startup if hard dependencies are unavailable.
  Document which dependencies are validated at startup vs deferred.
-->

| Dependency | Startup-validated? | Failure behaviour |
|------------|-------------------|-------------------|
| PostgreSQL | Yes | Crash — hard dependency |
| Kafka | No | Continue — fallback activates |
| Redis | No | Continue — fallback activates |
| Vault | Yes (prod only) | Crash in prod; warn in dev |

## Config Keys

<!--
  List all config keys used to connect to each dependency.
  Document the config provider that supplies the value.
-->

| Key | Dependency | Provider | Notes |
|-----|-----------|----------|-------|
| `spring.datasource.url` / `DATABASE_URL` | PostgreSQL | Env / Vault | JDBC URL with connection pool params |
| `spring.kafka.bootstrap-servers` / `KAFKA_BOOTSTRAP_SERVERS` | Kafka | Env | Comma-separated host:port |
| `spring.redis.url` / `REDIS_URL` | Redis | Env / Vault | `redis://host:port` |
| `aws.s3.bucket` / `S3_BUCKET` | S3 | Env | Bucket name per environment |
| `vault.uri` / `VAULT_ADDR` | Vault | Env | `https://vault.internal:8200` |

## Local Development Setup

```bash
# Start all dependencies
docker compose -f templates/infra/docker-compose.dev.yaml up -d

# Start with fallbacks only (zero Docker needed)
FALLBACK_KAFKA=db FALLBACK_CACHE=jsonfile FALLBACK_STORAGE=local FALLBACK_SECRETS=env \
  ./mvnw spring-boot:run   # or: uvicorn src.service.main:app --reload
```

## References

- [standards/fallback-strategy.md](../../standards/fallback-strategy.md)
- [playbooks/local-dev/run-with-fallbacks.md](../../playbooks/local-dev/run-with-fallbacks.md)
- [templates/infra/docker-compose.dev.yaml](../infra/docker-compose.dev.yaml)

