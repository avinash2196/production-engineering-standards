"""Inspectable JSON-file cache for local development and CI.

This adapter is process-local and does not provide distributed atomicity or safe
multi-process writes. It must not be selected in production.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class JsonFileCacheProvider:
    path: Path | str
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False)

    def __post_init__(self) -> None:
        self.path = Path(self.path)

    async def get(self, key: str) -> Any | None:
        async with self._lock:
            store = self._read_store()
            entry = store.get(key)
            if entry is None:
                return None
            expires_at = float(entry.get("expires_at", 0))
            if expires_at and time.time() >= expires_at:
                del store[key]
                self._write_store(store)
                return None
            return entry.get("value")

    async def set(self, key: str, value: Any, ttl_seconds: int = 0) -> None:
        async with self._lock:
            store = self._read_store()
            expires_at = time.time() + ttl_seconds if ttl_seconds else 0.0
            store[key] = {"value": value, "expires_at": expires_at}
            self._write_store(store)

    async def delete(self, key: str) -> None:
        async with self._lock:
            store = self._read_store()
            if store.pop(key, None) is not None:
                self._write_store(store)

    def _read_store(self) -> dict[str, dict[str, Any]]:
        if not self.path.exists():
            return {}
        try:
            content = self.path.read_text(encoding="utf-8")
            return json.loads(content) if content.strip() else {}
        except (json.JSONDecodeError, OSError) as exc:
            raise RuntimeError(f"Unable to read local cache file: {self.path}") from exc

    def _write_store(self, store: dict[str, dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(self.path.suffix + ".tmp")
        try:
            temporary_path.write_text(
                json.dumps(store, indent=2, sort_keys=True), encoding="utf-8"
            )
            os.replace(temporary_path, self.path)
        except (TypeError, OSError) as exc:
            temporary_path.unlink(missing_ok=True)
            raise RuntimeError(f"Unable to write local cache file: {self.path}") from exc
