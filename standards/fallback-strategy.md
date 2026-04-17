# Fallback Strategy

Purpose
- Define explicit, auditable fallback behaviors for external dependencies so services run locally without silently weakening production guarantees.

Mandatory Rules
- Every external integration must document at least one fallback implementation (e.g., Kafka → file-queue/no-op, Redis → in-memory cache, cloud storage → local disk).
- Fallbacks must be enabled explicitly with environment toggles (e.g., `FALLBACK_KAFKA=db`, `FALLBACK_CACHE=jsonfile`) and must not be the default in production images.
- Services must emit telemetry and audit logs when a fallback is in use.

Defaults
- Default fallback toggles are disabled. Developer instructions in `playbooks/local-dev/run-with-fallbacks.md` show how to enable them for local testing.

Anti-patterns
- Implicitly using fallback implementations in production or silently degrading guarantees without logging and alerts.

Fallback Patterns (clear definitions)
- Messaging fallback: Primary — DB table outbox (`FALLBACK_KAFKA=db`). The service's existing database stores messages in an `outbox_message` table; a scheduled poller delivers them to handlers. Survives restarts and is inspectable via SQL. Secondary — in-memory queue (`FALLBACK_KAFKA=inmemory`) for CI with no DB. Include behavior differences (durability, ordering, blocking semantics) in docs.
- Cache fallback: Primary — JSON file (`FALLBACK_CACHE=jsonfile`). Entries persisted to `./data/fallback-cache/cache.json` with TTL timestamps; survives restarts and is inspectable with `jq`. Secondary — in-memory dict/map (`FALLBACK_CACHE=inmemory`) for CI with no filesystem. Mark as non-distributed and document consistency implications.
- Storage fallback: Local filesystem adapter with configurable root and explicit sync/flush semantics; document eventual differences (latency, durability).
- Secret fallback: Environment-variable-only provider that is explicitly allowed only when `FALLBACK_SECRETS=env` and must log a security warning.

LLM instructions
- When scaffolding adapters, generate both the production adapter stub and a reference fallback implementation in the template. Add telemetry hooks and a clear env toggle.
- Default Kafka fallback is DB tables (`FALLBACK_KAFKA=db`). Default cache fallback is JSON file (`FALLBACK_CACHE=jsonfile`). Only use in-memory variants when the user confirms no DB or filesystem is available.
- Agents must ask if the team requires persistence guarantees (durable vs ephemeral) before choosing a fallback implementation.

Review checklist
- [ ] All external dependencies list a fallback in their integration guide.
- [ ] Fallbacks are enabled only via explicit environment toggles.
- [ ] Telemetry and audit logs emitted when fallbacks are active.
