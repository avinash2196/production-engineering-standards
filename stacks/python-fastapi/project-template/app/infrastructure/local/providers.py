"""Composition-root factories for explicit adapter selection.

Local adapters are implemented in this template because their behavior and
production guards are part of the shared standard. Production adapters are
created only when an approved implementation plan selects the corresponding
platform. A missing production adapter therefore produces an actionable error
instead of an opaque import failure.
"""

from __future__ import annotations

from importlib import import_module
import logging
from typing import Any

from app.config.settings import (
    CacheAdapter,
    MessagingAdapter,
    SecretAdapter,
    StorageAdapter,
    get_settings,
)
from app.infrastructure.local.database_outbox_publisher import (
    DatabaseOutboxMessagePublisher,
    SqlAlchemyOutboxStore,
)
from app.infrastructure.local.env_secrets import EnvSecretProvider
from app.infrastructure.local.inmemory_cache import InMemoryCacheProvider
from app.infrastructure.local.inmemory_publisher import InMemoryMessagePublisher
from app.infrastructure.local.json_file_cache import JsonFileCacheProvider
from app.infrastructure.local.local_storage import LocalFileStorageProvider

logger = logging.getLogger(__name__)


def _announce_local_adapter(capability: str, value: str, limitation: str) -> None:
    logger.warning(
        "local_adapter.active capability=%s value=%s limitation=%s",
        capability,
        value,
        limitation,
    )


def _load_adapter(module_name: str, class_name: str) -> type[Any]:
    """Load a generated production adapter with a clear planning error."""
    try:
        module = import_module(module_name)
        adapter_class = getattr(module, class_name)
    except (ImportError, AttributeError) as exc:
        raise RuntimeError(
            f"{class_name} is not included in the base template. "
            "Add it only through an approved implementation plan for the "
            "selected production capability."
        ) from exc

    return adapter_class


def get_publisher() -> Any:
    settings = get_settings()

    if settings.messaging_adapter is MessagingAdapter.DB:
        _announce_local_adapter(
            "messaging",
            "db",
            "no broker partitions, consumer groups, or rebalancing",
        )
        return DatabaseOutboxMessagePublisher(
            SqlAlchemyOutboxStore(
                settings.database_url,
                table_name=settings.outbox_table_name,
            )
        )
    if settings.messaging_adapter is MessagingAdapter.IN_MEMORY:
        _announce_local_adapter(
            "messaging",
            "inmemory",
            "process-local and lost on restart",
        )
        return InMemoryMessagePublisher()
    if settings.messaging_adapter is MessagingAdapter.PUBSUB:
        publisher_type = _load_adapter(
            "app.infrastructure.messaging.pubsub_publisher",
            "PubSubMessagePublisher",
        )
        return publisher_type(project_id=settings.gcp_project_id)

    publisher_type = _load_adapter(
        "app.infrastructure.messaging.kafka_publisher",
        "KafkaMessagePublisher",
    )
    return publisher_type(bootstrap_servers=settings.kafka_bootstrap_servers)


def get_cache() -> Any:
    settings = get_settings()

    if settings.cache_adapter is CacheAdapter.JSON_FILE:
        _announce_local_adapter(
            "cache",
            "jsonfile",
            "no distributed atomicity or multi-process consistency",
        )
        return JsonFileCacheProvider(settings.json_cache_path)
    if settings.cache_adapter is CacheAdapter.IN_MEMORY:
        _announce_local_adapter(
            "cache",
            "inmemory",
            "process-local and lost on restart",
        )
        return InMemoryCacheProvider()

    cache_type = _load_adapter(
        "app.infrastructure.cache.redis_cache",
        "RedisCacheProvider",
    )
    return cache_type(url=settings.redis_url)


def get_storage() -> Any:
    settings = get_settings()

    if settings.storage_adapter is StorageAdapter.LOCAL:
        _announce_local_adapter(
            "storage",
            "local",
            "no managed durability, IAM, or multi-instance behavior",
        )
        return LocalFileStorageProvider(base_path=settings.local_storage_path)
    if settings.storage_adapter is StorageAdapter.GCS:
        storage_type = _load_adapter(
            "app.infrastructure.storage.gcs_storage",
            "GcsObjectStorageProvider",
        )
        return storage_type(
            project_id=settings.gcp_project_id,
            bucket=settings.gcs_bucket,
        )

    storage_type = _load_adapter(
        "app.infrastructure.storage.s3_storage",
        "S3ObjectStorageProvider",
    )
    return storage_type(
        bucket=settings.s3_bucket,
        endpoint_url=settings.s3_endpoint_url or None,
        region=settings.s3_region,
    )


def get_secrets() -> Any:
    settings = get_settings()

    if settings.secret_adapter is SecretAdapter.ENV:
        _announce_local_adapter(
            "secrets",
            "env",
            "no managed rotation, centralized policy, or audit trail",
        )
        return EnvSecretProvider()
    if settings.secret_adapter is SecretAdapter.SECRET_MANAGER:
        secret_type = _load_adapter(
            "app.infrastructure.secrets.secret_manager_provider",
            "SecretManagerProvider",
        )
        return secret_type(project_id=settings.gcp_project_id)

    secret_type = _load_adapter(
        "app.infrastructure.secrets.vault_provider",
        "VaultSecretProvider",
    )
    return secret_type(address=settings.vault_address)
