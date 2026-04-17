"""In-memory CacheProvider fallback — TTL-aware HashMap.

NOT for production use. Does not survive process restart.
"""
import asyncio
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class _CacheEntry:
    value: Any
    expires_at: float  # epoch seconds; 0 = no expiry


@dataclass
class InMemoryCacheProvider:
    """Fallback implementation of CacheProvider using an in-memory dict."""

    _store: dict[str, _CacheEntry] = field(default_factory=dict)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def get(self, key: str) -> Any | None:
        async with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            if entry.expires_at and time.monotonic() > entry.expires_at:
                del self._store[key]
                return None
            return entry.value

    async def set(self, key: str, value: Any, ttl_seconds: int = 0) -> None:
        async with self._lock:
            expires_at = time.monotonic() + ttl_seconds if ttl_seconds else 0.0
            self._store[key] = _CacheEntry(value=value, expires_at=expires_at)

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._store.pop(key, None)
