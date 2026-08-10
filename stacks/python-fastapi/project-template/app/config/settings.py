from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Minimal runtime settings.

    Add new settings only when an approved milestone introduces behavior that
    requires them. Do not preload database, messaging, cache, storage, security,
    or observability configuration into the starter.
    """

    model_config = SettingsConfigDict(
        env_prefix="",
        case_sensitive=False,
        extra="ignore",
    )

    service_name: str = Field(default="service-name", min_length=1)
    environment: Literal["local", "test", "development", "staging", "production"] = (
        "local"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
