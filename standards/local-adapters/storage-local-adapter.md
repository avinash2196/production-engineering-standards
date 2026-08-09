# Storage Local Adapter

## Purpose

Local filesystem-based object storage replacement for development when S3/Azure Blob/GCS is unavailable. Activated by `STORAGE_ADAPTER=local`. Implements `ObjectStorageProvider` interface using a local directory.

## Activation

| Environment | Toggle | Active |
|-------------|--------|--------|
| Local dev | `STORAGE_ADAPTER=local` | Yes |
| Staging | `s3` or `gcs` | Production adapter |
| Production | `s3` or `gcs` | Local value rejected |

**Startup validation:** if `STORAGE_ADAPTER=local` and the environment is production, fail startup.

## Behavior

```
Storage root: ./data/local-storage/ (configurable)

put("my-bucket", "orders/123/invoice.pdf", data, metadata)
    → writes file to ./data/local-storage/my-bucket/orders/123/invoice.pdf
    → writes metadata to ./data/local-storage/my-bucket/orders/123/invoice.pdf.meta.json

get("my-bucket", "orders/123/invoice.pdf")
    → reads file and metadata from disk
    → throws ObjectNotFoundException if file does not exist

delete("my-bucket", "orders/123/invoice.pdf")
    → deletes file and metadata (idempotent — no error if already deleted)

exists("my-bucket", "orders/123/invoice.pdf")
    → returns true if file exists on disk

list("my-bucket", "orders/")
    → lists files in ./data/local-storage/my-bucket/orders/ recursively
```

## Directory Structure

```
./data/local-storage/
├── my-bucket/
│   └── orders/
│       └── 123/
│           ├── invoice.pdf
│           └── invoice.pdf.meta.json
└── another-bucket/
    └── ...
```

Metadata sidecar file (`.meta.json`):
```json
{
  "contentType": "application/pdf",
  "uploadedBy": "order-service",
  "uploadedAt": "2024-01-15T10:30:00Z",
  "correlationId": "req-789",
  "customMetadata": {}
}
```

## Java Example

```java
@Component
@ConditionalOnProperty(name = "adapters.storage", havingValue = "local")
public class LocalFileObjectStorageProvider implements ObjectStorageProvider {
    private final Path root;

    public LocalFileObjectStorageProvider(
            @Value("${adapters.storage.root:./data/local-storage}") String rootPath) {
        this.root = Path.of(rootPath);
    }

    @Override
    public void put(String bucket, String key, InputStream data, ObjectMetadata metadata) {
        Path filePath = root.resolve(bucket).resolve(key);
        Files.createDirectories(filePath.getParent());
        Files.copy(data, filePath, StandardCopyOption.REPLACE_EXISTING);
        writeMetadata(filePath, metadata);
    }

    @Override
    public StorageObject get(String bucket, String key) {
        Path filePath = root.resolve(bucket).resolve(key);
        if (!Files.exists(filePath)) {
            throw new ObjectNotFoundException(bucket, key);
        }
        ObjectMetadata metadata = readMetadata(filePath);
        return new StorageObject(Files.newInputStream(filePath), metadata);
    }

    @Override
    public void delete(String bucket, String key) {
        Path filePath = root.resolve(bucket).resolve(key);
        Files.deleteIfExists(filePath);
        Files.deleteIfExists(Path.of(filePath + ".meta.json"));
    }

    @Override
    public boolean exists(String bucket, String key) {
        return Files.exists(root.resolve(bucket).resolve(key));
    }

    @Override
    public URL getSignedUrl(String bucket, String key, Duration expiration) {
        log.warn("Signed URLs not supported in local-adapter mode, returning file:// URI");
        return root.resolve(bucket).resolve(key).toUri().toURL();
    }
}
```

## Python Example

```python
from pathlib import Path
import json, shutil

class LocalFileObjectStorageProvider:
    def __init__(self, root: str = "./data/local-storage"):
        self._root = Path(root)

    def put(self, bucket: str, key: str, data: BinaryIO, metadata: ObjectMetadata) -> None:
        file_path = self._root / bucket / key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(data, f)
        meta_path = Path(str(file_path) + ".meta.json")
        meta_path.write_text(json.dumps(metadata.to_dict()))

    def get(self, bucket: str, key: str) -> StorageObject:
        file_path = self._root / bucket / key
        if not file_path.exists():
            raise ObjectNotFoundError(bucket, key)
        metadata = json.loads(Path(str(file_path) + ".meta.json").read_text())
        return StorageObject(open(file_path, "rb"), ObjectMetadata(**metadata))

    def delete(self, bucket: str, key: str) -> None:
        file_path = self._root / bucket / key
        file_path.unlink(missing_ok=True)
        Path(str(file_path) + ".meta.json").unlink(missing_ok=True)
```

## Limitations

| Feature | Production (S3/Blob/GCS) | Local adapter |
|---------|--------------------------|----------|
| Encryption at rest | SSE / CMK | None |
| Lifecycle policies | Auto-expiration, tier transitions | None |
| Signed URLs | Time-limited pre-signed URLs | file:// URI (warning logged) |
| Versioning | Object versioning | No |
| Multi-instance access | Yes (object store is shared) | No (local filesystem) |
| Max object size enforcement | Storage service limits | Not enforced (log warning) |
| Consistency | Read-after-write | Filesystem-dependent |
| Durability | Managed/provider-dependent | Local disk only |

## What Works in the Local Adapter

- Basic put/get/delete/exists/list operations.
- Metadata storage and retrieval.
- Key naming convention validation.
- Functional testing of upload/download workflows.

## What the Local Adapter Does Not Reproduce

- Encryption at rest.
- Lifecycle/expiration policies.
- Pre-signed URLs (returns file:// URI with warning).
- Object versioning.
- Multi-instance shared storage.
- Durability guarantees.

## Gitignore

Add to `.gitignore`:
```
data/local-storage/
```

## LLM Instructions

- When scaffolding a storage local adapter, use the local filesystem pattern above.
- Wire via `@ConditionalOnProperty(name = "adapters.storage", havingValue = "local")` or Python conditional injection.
- Always create the metadata sidecar file alongside the object.
- Always add `data/local-storage/` to `.gitignore`.
- Generate startup validation that rejects the local adapter in production.

## Review Checklist

- [ ] Local adapter activated only by `STORAGE_ADAPTER=local`.
- [ ] Startup fails if local adapter active in production.
- [ ] Implements full `ObjectStorageProvider` interface.
- [ ] Metadata sidecar files created for every object.
- [ ] `data/local-storage/` in `.gitignore`.
- [ ] Limitations documented and understood by team.
