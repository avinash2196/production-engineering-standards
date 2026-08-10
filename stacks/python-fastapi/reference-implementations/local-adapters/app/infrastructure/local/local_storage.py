"""Local filesystem object-storage adapter for development and tests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class LocalFileStorageProvider:
    base_path: str = "./data/local-storage"

    def __post_init__(self) -> None:
        self._root = Path(self.base_path).resolve()
        self._root.mkdir(parents=True, exist_ok=True)

    def _resolve_key(self, key: str) -> Path:
        if not key or Path(key).is_absolute():
            raise ValueError("Object key must be a non-empty relative path")
        destination = (self._root / key).resolve()
        try:
            destination.relative_to(self._root)
        except ValueError as exc:
            raise ValueError("Object key must remain within the storage root") from exc
        return destination

    async def upload(
        self,
        key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> str:
        del content_type
        destination = self._resolve_key(key)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        return str(destination)

    async def download(self, key: str) -> bytes:
        destination = self._resolve_key(key)
        if not destination.exists():
            raise FileNotFoundError(f"Object not found: {key}")
        return destination.read_bytes()

    async def delete(self, key: str) -> None:
        self._resolve_key(key).unlink(missing_ok=True)

    async def exists(self, key: str) -> bool:
        return self._resolve_key(key).exists()
