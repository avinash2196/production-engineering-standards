"""Contract tests for the inspectable JSON-file local cache adapter."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.infrastructure.local.json_file_cache import JsonFileCacheProvider


class JsonFileCacheProviderTest(unittest.IsolatedAsyncioTestCase):
    async def test_persists_and_reads_value(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cache_path = Path(directory) / "cache.json"
            cache = JsonFileCacheProvider(cache_path)

            await cache.set("quote:1", {"amount": 125}, ttl_seconds=0)

            reloaded = JsonFileCacheProvider(cache_path)
            self.assertEqual({"amount": 125}, await reloaded.get("quote:1"))

    async def test_delete_removes_value(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cache = JsonFileCacheProvider(Path(directory) / "cache.json")
            await cache.set("quote:1", "value")

            await cache.delete("quote:1")

            self.assertIsNone(await cache.get("quote:1"))

    async def test_expired_value_is_removed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            cache = JsonFileCacheProvider(Path(directory) / "cache.json")
            await cache.set("quote:1", "value", ttl_seconds=-1)

            self.assertIsNone(await cache.get("quote:1"))


if __name__ == "__main__":
    unittest.main()
