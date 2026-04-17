# Python FastAPI Backend Guidance

Purpose
- Provide production-oriented patterns for FastAPI services emphasizing configuration-first design, capability abstractions, async-safe handlers, and explicit local fallbacks.

Structure
- Layers: `controller` (API routers) -> `service` -> `domain` -> `repository`.
- Recommended folders:
  - `app/api` (routers, DTOs/schemas)
  - `app/services` (business services)
  - `app/domain` (entities, value objects)
  - `app/repository` (data access)
  - `app/adapters` (messaging, storage, cache adapters)
  - `app/config` (settings and `ConfigProvider` wrappers)
  - `tests/` (unit and integration tests)
- Naming: Pydantic models use `PascalCase` classes suffixed `Request`/`Response`; adapters named `...Adapter`.

Abstractions
- Messaging: define `MessagePublisher` and `MessageSubscriber` interfaces (async-friendly). Each message includes `idempotency_key` and `trace_id` in attributes.
- Storage: `ObjectStorageProvider` with async-friendly `put/get/delete/list` and optional `presign`.
- Config: central `ConfigProvider` that composes sources (dynamic DB/service, env, local file) and returns typed Pydantic settings.
- Cache: `CacheProvider` exposing async `get/put/invalidate` with pluggable backends (aioredis vs in-memory LRU).

Fallback handling (local vs production)
- Enable fallbacks explicitly via env (e.g., `FALLBACK_KAFKA=db`, `FALLBACK_CACHE=jsonfile`). Use `FALLBACK_*` conventions across stacks.
- Local fallbacks:
  - Messaging → in-memory asyncio.Queue or file-backed queue (durability tradeoffs documented).
  - Cache → in-process TTL cache (e.g., cachetools TTLCache) with clear non-distributed semantics.
  - Storage → local filesystem under `./local-storage` with configurable root.
  - Secrets → env-only provider when `FALLBACK_SECRETS=env` and log a security warning.
- Telemetry: record a metric `fallback.active` and emit a structured log when a fallback is in use.

FastAPI patterns
- Validation: use Pydantic models for request and response schemas; enforce type-safe parsing at the edge.
- Dependency injection: use `fastapi.Depends` to provide `ConfigProvider`, `MessagePublisher`, `CacheProvider` to handlers.
- Async handling: prefer `async def` for IO-bound endpoints and background tasks via `BackgroundTasks` or external messaging for expensive work.

Testing
- Unit tests: use `pytest` and `pytest-mock`; mock adapters implementing capability interfaces.
- Integration: prefer Testcontainers (Python testcontainers library) for DB/broker in CI; otherwise rely on local fallback adapters for deterministic CI.

Anti-patterns
- Mixing blocking IO inside `async def` handlers without offloading (e.g., synchronous DB drivers without async wrappers).
- Placing business logic inside router functions or returning domain objects directly as response models.

LLM instructions
- When generating a FastAPI service scaffold, produce:
  - Pydantic settings classes wired to a `ConfigProvider` adapter implementing env→dynamic→file precedence
  - Async capability interfaces and both production + fallback adapters
  - Dependency providers for adapters wired into `Depends`
  - Health endpoints, metrics exposition (Prometheus), and OpenTelemetry tracing setup
- Ask the user only when: they require strict ordering guarantees for messaging, PHI/PII handling, or synchronous-only processing semantics.

Review checklist
- [ ] Pydantic DTOs separate from domain objects and used at the API edge.
- [ ] Dependency injection via `Depends` used for adapters.
- [ ] Async endpoints use non-blocking IO and are tested under load if possible.
- [ ] Fallback toggles explicit and documented.
