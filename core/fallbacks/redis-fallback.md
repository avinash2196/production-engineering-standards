# Redis Fallback

## Purpose

JSON-file-backed cache fallback for local development when Redis is unavailable. Activated by `FALLBACK_CACHE=jsonfile`. Implements `CacheProvider` using a local JSON file (`./data/fallback-cache/cache.json`) so cache entries survive restarts and can be inspected with any text editor.

An in-memory fallback (`FALLBACK_CACHE=inmemory`) is also available for CI or truly zero-infra setups, but entries are lost on restart and cannot be inspected.

## Activation

| Environment | Toggle | Fallback used |
|-------------|--------|---------------|
| Local dev (recommended) | `FALLBACK_CACHE=jsonfile` | JSON file — persistent, inspectable |
| Local dev (no disk) | `FALLBACK_CACHE=inmemory` | In-memory dict/map — ephemeral |
| Staging | Must be unset | No fallback |
| Production | Must be unset | **Never** |

**Startup validation:** if `FALLBACK_CACHE` is set to any value and the environment is production, fail startup.

## Behavior

### JSON File Implementation (Recommended — `FALLBACK_CACHE=jsonfile`)

Stores all cache entries in `./data/fallback-cache/cache.json` as a JSON object keyed by cache key. Each entry includes value, `expiresAt`, and metadata.

```
put(key, value, ttl)
    → read cache.json (or start with {})
    → write { key: { value, expiresAt: now+ttl, cachedAt: now } }
    → flush to disk (atomic write via temp file + rename)

get(key)
    → read cache.json
    → return value if present and expiresAt > now
    → remove expired entry and re-flush if expired
    → return null/None if missing or expired

evict(key)
    → remove key from JSON, flush

evictByPrefix(prefix)
    → remove all keys starting with prefix, flush
```

**File format (`./data/fallback-cache/cache.json`):**

```json
{
  "user:42:profile": {
    "value": { "id": 42, "name": "Alice" },
    "cachedAt": "2026-04-16T10:00:00Z",
    "expiresAt": "2026-04-16T10:05:00Z"
  }
}
```

- Survives restart — unexpired entries are reloaded.
- Inspectable with any text editor or `cat ./data/fallback-cache/cache.json | jq`.
- Atomic writes: write to `.cache.json.tmp` then rename — no corrupt reads.
- Single-process only (no file locking across multiple JVMs/processes).

### In-Memory Implementation (Fallback of last resort — `FALLBACK_CACHE=inmemory`)

Use only when no filesystem is available (e.g., some CI environments).

```
put(key, value, ttl)
    → stores in ConcurrentHashMap / dict with expiration timestamp

get(key)
    → returns value if present and not expired (lazy eviction)
    → returns null/None otherwise
```

- No persistence — all entries lost on restart.
- No max memory limit — unbounded heap usage.
- Single instance only.

## Java Example

### JSON file provider (`FALLBACK_CACHE=jsonfile`)

```java
@Component
@ConditionalOnProperty(name = "fallback.cache", havingValue = "jsonfile")
public class JsonFileCacheProvider implements CacheProvider {
    private static final Path CACHE_FILE = Path.of("./data/fallback-cache/cache.json");
    private static final Path TMP_FILE   = Path.of("./data/fallback-cache/cache.json.tmp");
    private final ObjectMapper mapper;

    @PostConstruct
    void init() throws IOException {
        Files.createDirectories(CACHE_FILE.getParent());
        if (!Files.exists(CACHE_FILE)) Files.writeString(CACHE_FILE, "{}");
        log.warn("[cache-fallback:jsonfile] active — cache stored at {}", CACHE_FILE.toAbsolutePath());
    }

    @Override
    public <T> Optional<T> get(String key, Class<T> type) throws IOException {
        Map<String, CacheEntry> store = readStore();
        CacheEntry entry = store.get(key);
        if (entry == null || Instant.now().isAfter(entry.expiresAt())) {
            if (entry != null) { store.remove(key); writeStore(store); }
            return Optional.empty();
        }
        return Optional.of(mapper.convertValue(entry.value(), type));
    }

    @Override
    public void put(String key, Object value, Duration ttl) throws IOException {
        Map<String, CacheEntry> store = readStore();
        store.put(key, new CacheEntry(value, Instant.now(), Instant.now().plus(ttl)));
        writeStore(store);
    }

    @Override
    public void evict(String key) throws IOException {
        Map<String, CacheEntry> store = readStore();
        store.remove(key);
        writeStore(store);
    }

    @Override
    public void evictByPrefix(String prefix) throws IOException {
        Map<String, CacheEntry> store = readStore();
        store.keySet().removeIf(k -> k.startsWith(prefix));
        writeStore(store);
    }

    private Map<String, CacheEntry> readStore() throws IOException {
        return mapper.readValue(CACHE_FILE.toFile(),
            new TypeReference<Map<String, CacheEntry>>() {});
    }

    private void writeStore(Map<String, CacheEntry> store) throws IOException {
        mapper.writeValue(TMP_FILE.toFile(), store);          // write to temp
        Files.move(TMP_FILE, CACHE_FILE, REPLACE_EXISTING, ATOMIC_MOVE); // atomic rename
    }

    private record CacheEntry(Object value, Instant cachedAt, Instant expiresAt) {}
}
```

### In-memory provider (`FALLBACK_CACHE=inmemory`)

```java
@Component
@ConditionalOnProperty(name = "fallback.cache", havingValue = "inmemory")
public class InMemoryCacheProvider implements CacheProvider {
    private final ConcurrentHashMap<String, CacheEntry> store = new ConcurrentHashMap<>();

    @Override
    public <T> Optional<T> get(String key, Class<T> type) {
        CacheEntry entry = store.get(key);
        if (entry == null || entry.isExpired()) { store.remove(key); return Optional.empty(); }
        return Optional.of(type.cast(entry.value()));
    }

    @Override
    public void put(String key, Object value, Duration ttl) {
        store.put(key, new CacheEntry(value, Instant.now().plus(ttl)));
    }

    @Override public void evict(String key) { store.remove(key); }

    @Override
    public void evictByPrefix(String prefix) {
        store.keySet().removeIf(k -> k.startsWith(prefix));
    }

    @Scheduled(fixedDelay = 60_000)
    public void cleanExpired() { store.entrySet().removeIf(e -> e.getValue().isExpired()); }

    private record CacheEntry(Object value, Instant expiresAt) {
        boolean isExpired() { return Instant.now().isAfter(expiresAt); }
    }
}
```

## Python Example

### JSON file provider (`FALLBACK_CACHE=jsonfile`)

```python
import json, os
from pathlib import Path
from datetime import datetime, timezone, timedelta
from threading import Lock
from typing import Any

CACHE_FILE = Path("./data/fallback-cache/cache.json")

class JsonFileCacheProvider:
    def __init__(self):
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not CACHE_FILE.exists():
            CACHE_FILE.write_text("{}")
        self._lock = Lock()
        logger.warning("fallback.active", fallback="cache", mode="jsonfile", path=str(CACHE_FILE))

    def get(self, key: str) -> Any | None:
        with self._lock:
            store = self._read()
            entry = store.get(key)
            if not entry:
                return None
            if datetime.fromisoformat(entry["expiresAt"]) < datetime.now(timezone.utc):
                del store[key]
                self._write(store)
                return None
            return entry["value"]

    def put(self, key: str, value: Any, ttl: timedelta) -> None:
        with self._lock:
            store = self._read()
            now = datetime.now(timezone.utc)
            store[key] = {
                "value": value,
                "cachedAt": now.isoformat(),
                "expiresAt": (now + ttl).isoformat(),
            }
            self._write(store)

    def evict(self, key: str) -> None:
        with self._lock:
            store = self._read()
            store.pop(key, None)
            self._write(store)

    def evict_by_prefix(self, prefix: str) -> None:
        with self._lock:
            store = self._read()
            keys = [k for k in store if k.startswith(prefix)]
            for k in keys: del store[k]
            self._write(store)

    def _read(self) -> dict:
        return json.loads(CACHE_FILE.read_text())

    def _write(self, store: dict) -> None:
        tmp = CACHE_FILE.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(store, indent=2, default=str))
        os.replace(tmp, CACHE_FILE)   # atomic rename
```

### In-memory provider (`FALLBACK_CACHE=inmemory`)

```python
class InMemoryCacheProvider:
    def __init__(self):
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = Lock()

    def get(self, key: str) -> Any | None:
        with self._lock:
            entry = self._store.get(key)
            if entry is None: return None
            value, expires_at = entry
            if time() > expires_at:
                del self._store[key]
                return None
            return value

    def put(self, key: str, value: Any, ttl: timedelta) -> None:
        with self._lock:
            self._store[key] = (value, time() + ttl.total_seconds())

    def evict(self, key: str) -> None:
        with self._lock: self._store.pop(key, None)
```

## Limitations

| Feature | Production Redis | JSON file fallback | In-memory fallback |
|---------|-----------------|-------------------|--------------------|
| Persistence | RDB/AOF | Yes — file survives restart | None — lost on restart |
| Inspectable | Redis CLI / RedisInsight | Yes — `cat cache.json \| jq` | No |
| Max memory / eviction | Configurable LRU/LFU | Unbounded (disk) | Unbounded (heap) |
| Cluster / replication | Yes | No (single process) | No |
| Pub/sub | Yes | No | No |
| Atomic operations | MULTI/EXEC | Lock per operation | `putIfAbsent` only |
| Performance | Sub-millisecond | File I/O per call (fast locally) | In-process (fastest) |
| Shared across instances | Yes | No (file lock not cross-process) | No |
| TTL precision | Millisecond | Second (ISO timestamp) | Lazy eviction + 60s sweep |

## What Works in Fallback

- Basic get/put/evict with TTL enforcement.
- `putIfAbsent` atomicity (single-process).
- Cache-aside pattern testing.
- Verifying key naming conventions.

## What Does NOT Work in Fallback

- Shared cache across multiple service instances.
- Redis-specific features (pub/sub, Lua scripts, sorted sets).
- Memory eviction under pressure.
- Production-grade latency characteristics.

## LLM Instructions

- When scaffolding a cache fallback, generate the **JSON file implementation** (`FALLBACK_CACHE=jsonfile`) as the primary option.
- Also generate the in-memory implementation as a secondary option for CI or no-disk environments.
- Auto-create `./data/fallback-cache/` directory on startup. Never overwrite an existing cache file.
- Wire via `@ConditionalOnProperty(name="fallback.cache", havingValue="jsonfile")` (Spring) or `settings.fallback_cache == "jsonfile"` (Python).
- Always use atomic writes (write to `.tmp`, then rename) to prevent corrupt reads.
- Always add startup validation that fails if `FALLBACK_CACHE` is set in production.
- Emit a structured `logger.warning` with `fallback=cache, mode=jsonfile` on startup when active.

## Review Checklist

- [ ] `FALLBACK_CACHE=jsonfile` is the default local fallback (not in-memory).
- [ ] Cache file stored at `./data/fallback-cache/cache.json`.
- [ ] Atomic writes via temp file + rename — no corrupt reads.
- [ ] Startup fails if `FALLBACK_CACHE` is set in production.
- [ ] Implements full `CacheProvider` interface.
- [ ] TTL enforced with ISO 8601 `expiresAt` timestamps.
- [ ] Thread-safe (file lock per operation).
- [ ] Fallback active warning emitted on startup.
- [ ] Limitations documented and understood by team.
