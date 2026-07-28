"""In-memory MessagePublisher fallback — stores published messages in a list.

NOT for production use. Messages are lost on process restart.
"""
import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryMessagePublisher:
    """Fallback implementation of MessagePublisher using an in-memory list."""

    _store: dict[str, list[Any]] = field(default_factory=lambda: defaultdict(list))
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def publish(self, topic: str, message: Any, key: str | None = None) -> None:
        async with self._lock:
            self._store[topic].append({"key": key, "value": message})

    def get_messages(self, topic: str) -> list[Any]:
        """Test helper — inspect published messages."""
        return list(self._store.get(topic, []))

    def clear(self) -> None:
        """Test helper — reset state between tests."""
        self._store.clear()
