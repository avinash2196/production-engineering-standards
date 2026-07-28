"""Selector tests for explicit local adapter wiring."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.config.settings import (
    CacheAdapter,
    MessagingAdapter,
    SecretAdapter,
    Settings,
    StorageAdapter,
)
from app.infrastructure.local.database_outbox_publisher import (
    DatabaseOutboxMessagePublisher,
)
from app.infrastructure.local.env_secrets import EnvSecretProvider
from app.infrastructure.local.inmemory_cache import InMemoryCacheProvider
from app.infrastructure.local.inmemory_publisher import InMemoryMessagePublisher
from app.infrastructure.local.json_file_cache import JsonFileCacheProvider
from app.infrastructure.local.local_storage import LocalFileStorageProvider
from app.infrastructure.local.providers import (
    get_cache,
    get_publisher,
    get_secrets,
    get_storage,
)


class ProviderSelectionTest(unittest.TestCase):
    def test_selects_local_adapters_explicitly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            settings = Settings(
                _env_file=None,
                environment="local",
                messaging_adapter=MessagingAdapter.DB,
                cache_adapter=CacheAdapter.JSON_FILE,
                storage_adapter=StorageAdapter.LOCAL,
                secret_adapter=SecretAdapter.ENV,
                json_cache_path=str(Path(directory) / "cache.json"),
                local_storage_path=str(Path(directory) / "storage"),
            )

            with patch(
                "app.infrastructure.local.providers.get_settings",
                return_value=settings,
            ):
                with self.assertLogs(
                    "app.infrastructure.local.providers", level="WARNING"
                ) as captured:
                    self.assertIsInstance(
                        get_publisher(), DatabaseOutboxMessagePublisher
                    )
                    self.assertIsInstance(get_cache(), JsonFileCacheProvider)
                    self.assertIsInstance(get_storage(), LocalFileStorageProvider)
                    self.assertIsInstance(get_secrets(), EnvSecretProvider)

                combined = " ".join(captured.output)
                self.assertIn("local_adapter.active", combined)
                self.assertIn("capability=messaging value=db", combined)
                self.assertIn("capability=cache value=jsonfile", combined)

    def test_selects_inmemory_adapters(self) -> None:
        settings = Settings(
            _env_file=None,
            environment="test",
            messaging_adapter=MessagingAdapter.IN_MEMORY,
            cache_adapter=CacheAdapter.IN_MEMORY,
        )

        with patch(
            "app.infrastructure.local.providers.get_settings",
            return_value=settings,
        ):
            with self.assertLogs(
                "app.infrastructure.local.providers", level="WARNING"
            ):
                self.assertIsInstance(get_publisher(), InMemoryMessagePublisher)
                self.assertIsInstance(get_cache(), InMemoryCacheProvider)

    def test_missing_production_adapter_has_actionable_error(self) -> None:
        settings = Settings(
            _env_file=None,
            environment="local",
            messaging_adapter=MessagingAdapter.KAFKA,
        )

        with patch(
            "app.infrastructure.local.providers.get_settings",
            return_value=settings,
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "KafkaMessagePublisher.*approved implementation plan",
            ):
                get_publisher()


if __name__ == "__main__":
    unittest.main()
