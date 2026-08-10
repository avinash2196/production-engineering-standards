"""Environment-variable secret provider for local development only."""

import os
from dataclasses import dataclass


@dataclass
class EnvSecretProvider:
    async def get(self, key: str) -> str:
        env_key = key.upper().replace(".", "_").replace("-", "_")
        value = os.environ.get(env_key)
        if value is None:
            raise KeyError(f"Secret not found in environment: {env_key}")
        return value
