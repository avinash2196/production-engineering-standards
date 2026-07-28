"""Configuration tests for typed adapter selection and production guards."""

from __future__ import annotations

import unittest

from pydantic import ValidationError

from app.config.settings import (
    CacheAdapter,
    MessagingAdapter,
    SecretAdapter,
    Settings,
    StorageAdapter,
)


class SettingsTest(unittest.TestCase):
    def test_accepts_production_adapters_in_production(self) -> None:
        settings = Settings(
            _env_file=None,
            environment="production",
            messaging_adapter=MessagingAdapter.KAFKA,
            cache_adapter=CacheAdapter.REDIS,
            storage_adapter=StorageAdapter.S3,
            secret_adapter=SecretAdapter.VAULT,
        )

        self.assertEqual(MessagingAdapter.KAFKA, settings.messaging_adapter)
        self.assertTrue(settings.database_url.startswith("postgresql+asyncpg://"))
        self.assertEqual("localhost:9092", settings.kafka_bootstrap_servers)

    def test_accepts_gcp_production_adapters(self) -> None:
        settings = Settings(
            _env_file=None,
            environment="production",
            messaging_adapter=MessagingAdapter.PUBSUB,
            cache_adapter=CacheAdapter.REDIS,
            storage_adapter=StorageAdapter.GCS,
            secret_adapter=SecretAdapter.SECRET_MANAGER,
        )

        self.assertEqual(MessagingAdapter.PUBSUB, settings.messaging_adapter)
        self.assertEqual(StorageAdapter.GCS, settings.storage_adapter)
        self.assertEqual(SecretAdapter.SECRET_MANAGER, settings.secret_adapter)

    def test_rejects_each_local_only_adapter_in_production(self) -> None:
        local_selections = (
            {"messaging_adapter": MessagingAdapter.DB},
            {"messaging_adapter": MessagingAdapter.IN_MEMORY},
            {"cache_adapter": CacheAdapter.JSON_FILE},
            {"cache_adapter": CacheAdapter.IN_MEMORY},
            {"storage_adapter": StorageAdapter.LOCAL},
            {"secret_adapter": SecretAdapter.ENV},
        )

        for selection in local_selections:
            with self.subTest(selection=selection):
                with self.assertRaises(ValidationError):
                    Settings(
                        _env_file=None,
                        environment="production",
                        **selection,
                    )


if __name__ == "__main__":
    unittest.main()
