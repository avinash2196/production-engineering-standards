# Local Adapters vs Production Degradation

These solve different problems.

## Local adapters
Allow development/CI without managed dependencies.

Examples:
- Kafka/PubSub → local in-memory or database-backed adapter
- Redis → local in-memory/file cache
- S3/GCS → local filesystem
- Vault/Secret Manager → environment-variable provider

Local adapters must be explicit and blocked from accidental production use.

## Production degradation
Defines what the real service does when a real dependency fails.

Never silently treat a local adapter as a production fallback. Document reduced durability, consistency, ordering, concurrency, and security guarantees.
