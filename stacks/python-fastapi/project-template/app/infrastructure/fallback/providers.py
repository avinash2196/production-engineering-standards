"""
Fallback DI wiring — activated when FALLBACK_* env vars are set.

Usage in FastAPI endpoints / services:

    from app.infrastructure.fallback.providers import get_publisher

    async def my_endpoint(publisher: MessagePublisher = Depends(get_publisher)):
        ...
"""
from app.config.settings import get_settings
from app.infrastructure.fallback.inmemory_cache import InMemoryCacheProvider
from app.infrastructure.fallback.inmemory_publisher import InMemoryMessagePublisher
from app.infrastructure.fallback.local_storage import LocalFileStorageProvider
from app.infrastructure.fallback.env_secrets import EnvSecretProvider


def get_publisher():
    settings = get_settings()
    if settings.fallback_kafka:
        return InMemoryMessagePublisher()
    from app.infrastructure.messaging.kafka_publisher import KafkaMessagePublisher
    return KafkaMessagePublisher(bootstrap_servers=settings.kafka_bootstrap_servers)


def get_cache():
    settings = get_settings()
    if settings.fallback_cache == "inmemory":
        return InMemoryCacheProvider()
    from app.infrastructure.cache.redis_cache import RedisCacheProvider
    return RedisCacheProvider(url=settings.redis_url)


def get_storage():
    settings = get_settings()
    if settings.fallback_storage == "local":
        return LocalFileStorageProvider(base_path="./data/fallback-storage")
    from app.infrastructure.storage.s3_storage import S3ObjectStorageProvider
    return S3ObjectStorageProvider(
        bucket=settings.s3_bucket,
        endpoint_url=settings.s3_endpoint_url or None,
        region=settings.s3_region,
    )


def get_secrets():
    settings = get_settings()
    if settings.fallback_secrets == "env":
        return EnvSecretProvider()
    from app.infrastructure.secrets.vault_provider import VaultSecretProvider
    return VaultSecretProvider()
