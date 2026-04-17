from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Service identity
    service_name: str = "service-name"
    environment: str = "local"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/service_db"

    # Fallback toggles — match FALLBACK_* env var names
    fallback_kafka: bool = False
    fallback_cache: str = "redis"       # "redis" | "inmemory"
    fallback_storage: str = "s3"        # "s3" | "local"
    fallback_secrets: str = "vault"     # "vault" | "env"

    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_consumer_group: str = service_name

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Object storage (S3 / MinIO)
    s3_bucket: str = "service-bucket"
    s3_endpoint_url: str = ""           # Override for MinIO: http://localhost:9000
    s3_region: str = "us-east-1"

    # OIDC / JWT
    jwt_issuer_uri: str = "https://auth.myorg.com"


@lru_cache
def get_settings() -> Settings:
    return Settings()
