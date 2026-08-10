"""In-memory message publisher for isolated local/test use only."""

import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryMessagePublisher:
    _store: dict[str, list[Any]] = field(default_factory=lambda: defaultdict(list))
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def publish(self, topic: str, message: Any, key: str | None = None) -> None:
        async with self._lock:
            self._store[topic].append({"key": key, "value": message})

    def get_messages(self, topic: str) -> list[Any]:
        return list(self._store.get(topic, []))

    def clear(self) -> None:
        self._store.clear()
