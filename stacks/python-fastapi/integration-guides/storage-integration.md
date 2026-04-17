# Storage Integration (Python FastAPI)

## Purpose

Step-by-step guide for wiring object storage (S3, Azure Blob, GCS) into a FastAPI service through the `ObjectStorageProvider` capability interface using `aiobotocore`, covering async uploads/downloads, presigned URLs, observability, and fallback setup.

## Dependencies

```txt
# requirements.txt
aiobotocore>=2.12.0
pydantic>=2.0
prometheus-client>=0.20.0
```

## Configuration

```python
# config/storage.py
from pydantic_settings import BaseSettings

class StorageSettings(BaseSettings):
    provider: str = "s3"                      # s3 | azure-blob | gcs
    bucket: str = "my-app-files"
    region: str = "us-east-1"
    endpoint_url: str | None = None           # override for LocalStack / MinIO
    max_upload_size_mb: int = 100
    presigned_url_expiry_seconds: int = 900   # 15 minutes

    class Config:
        env_prefix = "STORAGE_"
```

## ObjectStorageProvider Implementation (S3)

```python
# infrastructure/storage/s3_storage_provider.py
import time
from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from core.abstractions import ObjectStorageProvider

class S3ObjectStorageProvider(ObjectStorageProvider):
    def __init__(self, settings: StorageSettings, metrics: MetricsCollector):
        self._settings = settings
        self._session = get_session()
        self._metrics = metrics

    @asynccontextmanager
    async def _client(self):
        async with self._session.create_client(
            "s3",
            region_name=self._settings.region,
            endpoint_url=self._settings.endpoint_url,
        ) as client:
            yield client

    async def upload(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> None:
        start = time.monotonic()
        try:
            async with self._client() as s3:
                await s3.put_object(
                    Bucket=self._settings.bucket,
                    Key=key,
                    Body=data,
                    ContentType=content_type,
                    ServerSideEncryption="AES256",
                )
            self._metrics.increment("storage_uploads_total")
            self._metrics.increment("storage_bytes_uploaded_total", len(data))
        except Exception as e:
            self._metrics.increment("storage_errors_total", tags={"op": "upload"})
            raise StorageOperationError(f"Upload failed: key={key}") from e
        finally:
            self._metrics.observe("storage_operation_duration_seconds",
                                  time.monotonic() - start, tags={"op": "upload"})

    async def download(self, key: str) -> bytes:
        try:
            async with self._client() as s3:
                response = await s3.get_object(
                    Bucket=self._settings.bucket, Key=key)
                body = await response["Body"].read()
                self._metrics.increment("storage_downloads_total")
                return body
        except s3.exceptions.NoSuchKey:
            raise ObjectNotFoundError(key)
        except Exception as e:
            self._metrics.increment("storage_errors_total", tags={"op": "download"})
            raise StorageOperationError(f"Download failed: key={key}") from e

    async def delete(self, key: str) -> None:
        async with self._client() as s3:
            await s3.delete_object(
                Bucket=self._settings.bucket, Key=key)
            self._metrics.increment("storage_deletes_total")

    async def exists(self, key: str) -> bool:
        try:
            async with self._client() as s3:
                await s3.head_object(
                    Bucket=self._settings.bucket, Key=key)
                return True
        except Exception:
            return False

    async def get_signed_url(self, key: str, expiry_seconds: int | None = None) -> str:
        expiry = expiry_seconds or self._settings.presigned_url_expiry_seconds
        async with self._client() as s3:
            url = await s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self._settings.bucket, "Key": key},
                ExpiresIn=expiry,
            )
            return url
```

## FastAPI Dependency Wiring

```python
# dependencies.py
def get_storage_provider(settings: Settings = Depends(get_settings)) -> ObjectStorageProvider:
    if settings.fallback_storage == "local":
        return LocalFileStorageProvider(base_path="./data/fallback-storage")
    return S3ObjectStorageProvider(settings.storage, get_metrics())
```

## Key Naming Convention

```
{entity-type}/{entity-id}/{filename}
```

| Pattern | Example |
|---------|---------|
| User avatars | `users/abc-123/avatar.png` |
| Order attachments | `orders/ord-456/receipt.pdf` |
| Temp uploads | `tmp/{uuid}/{original-name}` |

## Upload Endpoint Example

```python
# api/files.py
from fastapi import APIRouter, UploadFile, Depends, HTTPException

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/upload/{entity_type}/{entity_id}")
async def upload_file(
    entity_type: str,
    entity_id: str,
    file: UploadFile,
    storage: ObjectStorageProvider = Depends(get_storage_provider),
):
    if file.size and file.size > 100 * 1024 * 1024:
        raise HTTPException(413, "File too large (max 100MB)")

    key = f"{entity_type}/{entity_id}/{file.filename}"
    content = await file.read()
    await storage.upload(key, content, content_type=file.content_type or "application/octet-stream")
    return {"key": key, "size": len(content)}

@router.get("/download/{key:path}")
async def download_file(
    key: str,
    storage: ObjectStorageProvider = Depends(get_storage_provider),
):
    signed_url = await storage.get_signed_url(key)
    return RedirectResponse(signed_url)
```

## Fallback Wiring

```python
# infrastructure/storage/local_file_storage.py
import json
from pathlib import Path
from core.abstractions import ObjectStorageProvider

class LocalFileStorageProvider(ObjectStorageProvider):
    """See standards/fallbacks/storage-fallback.md for full implementation."""

    def __init__(self, base_path: str = "./data/fallback-storage"):
        self._base = Path(base_path)
        self._base.mkdir(parents=True, exist_ok=True)

    async def upload(self, key: str, data: bytes, content_type: str = "") -> None:
        file_path = self._base / key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(data)
        # Write metadata sidecar
        meta_path = file_path.with_suffix(file_path.suffix + ".meta.json")
        meta_path.write_text(json.dumps({"contentType": content_type, "size": len(data)}))

    async def download(self, key: str) -> bytes:
        file_path = self._base / key
        if not file_path.exists():
            raise ObjectNotFoundError(key)
        return file_path.read_bytes()

    async def delete(self, key: str) -> None:
        file_path = self._base / key
        file_path.unlink(missing_ok=True)
        file_path.with_suffix(file_path.suffix + ".meta.json").unlink(missing_ok=True)
```

Activate via:
```bash
export FALLBACK_STORAGE=local
```

## Observability

| Metric | Description |
|--------|-------------|
| `storage_uploads_total` | Successful uploads |
| `storage_downloads_total` | Successful downloads |
| `storage_deletes_total` | Successful deletes |
| `storage_bytes_uploaded_total` | Total bytes uploaded |
| `storage_errors_total` | Operation failures by op type |
| `storage_operation_duration_seconds` | Latency histogram by op |

## Testing

```python
import pytest
from testcontainers.localstack import LocalStackContainer

@pytest.fixture(scope="module")
def localstack():
    with LocalStackContainer(image="localstack/localstack:3") as ls:
        yield ls

@pytest.mark.asyncio
async def test_upload_and_download(localstack):
    settings = StorageSettings(
        endpoint_url=localstack.get_url(),
        region="us-east-1",
        bucket="test-bucket",
    )
    provider = S3ObjectStorageProvider(settings, mock_metrics())
    content = b"hello world"
    await provider.upload("test/file.txt", content, "text/plain")
    result = await provider.download("test/file.txt")
    assert result == content
```

## References

- [ObjectStorageProvider.md](../../../contracts/ObjectStorageProvider.md)
- [storage-fallback.md](../../../standards/fallbacks/storage-fallback.md)
- [security-standards.md](../../../standards/security/security-standards.md)
