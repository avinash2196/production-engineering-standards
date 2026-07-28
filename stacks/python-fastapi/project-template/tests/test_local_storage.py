"""Behavior tests for the local filesystem storage adapter."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.infrastructure.local.local_storage import LocalFileStorageProvider


class LocalFileStorageProviderTest(unittest.IsolatedAsyncioTestCase):
    async def test_round_trip_uses_configured_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            provider = LocalFileStorageProvider(directory)

            await provider.upload("orders/123/invoice.txt", b"invoice")

            self.assertEqual(
                b"invoice",
                await provider.download("orders/123/invoice.txt"),
            )
            self.assertTrue(await provider.exists("orders/123/invoice.txt"))
            self.assertTrue(
                (Path(directory) / "orders" / "123" / "invoice.txt").exists()
            )

    async def test_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            provider = LocalFileStorageProvider(directory)

            with self.assertRaisesRegex(ValueError, "storage root"):
                await provider.upload("../outside.txt", b"unsafe")


if __name__ == "__main__":
    unittest.main()
