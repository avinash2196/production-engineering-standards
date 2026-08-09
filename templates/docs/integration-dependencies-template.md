# Integration Dependencies Template
<!--
  HOW TO USE:
  Copy to docs/integration-dependencies.md (or <service>/docs/dependencies.md).
  Fill in one row per external dependency.
  Keep local-development behavior separate from production failure behavior.
  See: playbooks/create-doc.md for the documentation workflow.
-->

# Integration Dependencies: [SERVICE NAME]

**Owner:** [Team]  
**Last updated:** YYYY-MM-DD

## Runtime Dependencies

| Dependency | Purpose | Required version | Protocol | Local adapter/emulator | Production failure behavior |
|---|---|---|---|---|---|
| PostgreSQL | Primary data store | [Version] | TCP | Testcontainers/local DB if approved | [fail fast / startup required / operation-specific] |
| Kafka / Pub/Sub | Domain events | [Version/service] | Broker protocol | `db`/`inmemory` only if approved | [fail / bounded retry / durable queue per contract] |
| Redis | Cache | [Version] | TCP | `jsonfile`/`inmemory` only if approved | [bypass / stale / fail according to correctness and load] |
| S3 / Cloud Storage | Object storage | [Service] | HTTPS | local filesystem only if approved | [retry / fail / queue according to operation semantics] |
| Vault / Secret Manager | Secrets | [Service] | HTTPS | environment provider for local use only | fail closed for required production secrets |
| [Downstream service] | [Purpose] | [Version] | HTTP/gRPC | [mock/emulator/none] | [approved behavior] |

A local adapter is a development/CI choice. It is not the automatic production response to dependency failure.

## Startup and Runtime Validation

| Dependency | Startup-validated? | Required for readiness? | Runtime failure behavior |
|---|---|---|---|
| [Dependency] | [Yes/No] | [Yes/No] | [Explicit approved behavior] |

Document only checks the service actually performs. Do not mark a dependency as required for readiness merely because it exists; base readiness on whether the service can safely serve its intended traffic.

## Configuration Keys

| Key | Dependency | Source/provider | Notes |
|---|---|---|---|
| `[KEY]` | [Dependency] | [Env/Vault/Secret Manager/etc.] | [Purpose and restrictions] |

## Local Development Setup

```bash
# Start selected real/local dependencies when needed.
docker compose -f templates/infra/docker-compose.dev.yaml up -d

# Or start with explicitly selected local adapters when the service implements them.
MESSAGING_ADAPTER=db CACHE_ADAPTER=jsonfile STORAGE_ADAPTER=local SECRET_ADAPTER=env \
  ./mvnw spring-boot:run
```

List only adapter values implemented and tested by the target service.

## References

- [Local Adapter Strategy](../../standards/local-adapter-strategy.md)
- [Production Dependency Failure and Degradation](../../standards/fallback-strategy.md)
- [Run with Local Adapters](../../playbooks/local-dev/run-with-local-adapters.md)
