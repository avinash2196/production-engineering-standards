from enum import StrEnum
from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class MessagingAdapter(StrEnum):
    KAFKA = "kafka"
    DB = "db"
    IN_MEMORY = "inmemory"


class CacheAdapter(StrEnum):
    REDIS = "redis"
    JSON_FILE = "jsonfile"
    IN_MEMORY = "inmemory"


class StorageAdapter(StrEnum):
    S3 = "s3"
    LOCAL = "local"


class SecretAdapter(StrEnum):
    VAULT = "vault"
    ENV = "env"


class Settings(BaseSettings):
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

    @model_validator(mode="after")
    def reject_local_adapters_in_production(self) -> "Settings":
        if self.environment.lower() == "production":
            invalid = {
                "messaging_adapter": {
                    MessagingAdapter.DB,
                    MessagingAdapter.IN_MEMORY,
                },
                "cache_adapter": {
                    CacheAdapter.JSON_FILE,
                    CacheAdapter.IN_MEMORY,
                },
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
                name
                for name, value in selected.items()
                if value in invalid[name]
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