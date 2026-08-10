"""Typed settings used only by the local-adapter reference implementation."""

from enum import StrEnum
from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class MessagingAdapter(StrEnum):
    KAFKA = "kafka"
    PUBSUB = "pubsub"
    DB = "db"
    IN_MEMORY = "inmemory"


class CacheAdapter(StrEnum):
    REDIS = "redis"
    JSON_FILE = "jsonfile"
    IN_MEMORY = "inmemory"


class StorageAdapter(StrEnum):
    S3 = "s3"
    GCS = "gcs"
    LOCAL = "local"


class SecretAdapter(StrEnum):
    VAULT = "vault"
    SECRET_MANAGER = "secretmanager"
    ENV = "env"


class Settings(BaseSettings):
    """Reference-only adapter settings and production safety guard."""

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    service_name: str = "service-name"
    environment: str = "local"

    messaging_adapter: MessagingAdapter = MessagingAdapter.KAFKA
    cache_adapter: CacheAdapter = CacheAdapter.REDIS
    storage_adapter: StorageAdapter = StorageAdapter.S3
    secret_adapter: SecretAdapter = SecretAdapter.VAULT

    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/service_db"
    )
    outbox_table_name: str = "outbox_message"
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_consumer_group: str = "service-name"
    gcp_project_id: str = ""

    redis_url: str = "redis://localhost:6379/0"
    json_cache_path: str = "./data/local-cache/cache.json"

    s3_bucket: str = "service-bucket"
    s3_endpoint_url: str = ""
    s3_region: str = "us-east-1"
    gcs_bucket: str = ""
    local_storage_path: str = "./data/local-storage"

    vault_address: str = "http://localhost:8200"
    jwt_issuer_uri: str = "https://auth.myorg.com"

    @model_validator(mode="after")
    def reject_local_adapters_in_production(self) -> "Settings":
        if self.environment.lower() != "production":
            return self

        invalid = {
            "messaging_adapter": {MessagingAdapter.DB, MessagingAdapter.IN_MEMORY},
            "cache_adapter": {CacheAdapter.JSON_FILE, CacheAdapter.IN_MEMORY},
            "storage_adapter": {StorageAdapter.LOCAL},
            "secret_adapter": {SecretAdapter.ENV},
        }
        selected = {
            "messaging_adapter": self.messaging_adapter,
            "cache_adapter": self.cache_adapter,
            "storage_adapter": self.storage_adapter,
            "secret_adapter": self.secret_adapter,
        }
        violations = [
            name for name, value in selected.items() if value in invalid[name]
        ]
        if violations:
            raise ValueError(
                "Local-only adapters are not allowed in production: "
                + ", ".join(violations)
            )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
