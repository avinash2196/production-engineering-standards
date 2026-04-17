"""Local filesystem ObjectStorageProvider fallback.

Stores files under base_path/key. NOT for production use.
"""
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LocalFileStorageProvider:
    base_path: str = "./data/fallback-storage"

    async def upload(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        dest = Path(self.base_path) / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return str(dest)

    async def download(self, key: str) -> bytes:
        dest = Path(self.base_path) / key
        if not dest.exists():
            raise FileNotFoundError(f"Object not found: {key}")
        return dest.read_bytes()

    async def delete(self, key: str) -> None:
        dest = Path(self.base_path) / key
        if dest.exists():
            os.remove(dest)

    async def exists(self, key: str) -> bool:
        return (Path(self.base_path) / key).exists()
