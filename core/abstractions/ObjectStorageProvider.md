# ObjectStorageProvider

## Purpose

Define the capability interface for storing and retrieving binary objects (files, documents, images) with explicit encryption, lifecycle, and consistency contracts. Services depend on this abstraction, never directly on S3, Azure Blob, GCS, or MinIO.

## Interface Contract

- `put(bucket, key, data, metadata)` → stores an object. Returns storage confirmation.
- `get(bucket, key)` → returns object data and metadata, or throws `ObjectNotFoundException`.
- `delete(bucket, key)` → removes an object. Idempotent (no error if already deleted).
- `exists(bucket, key)` → returns `true`/`false`.
- `list(bucket, prefix, options)` → returns paginated list of object keys matching prefix.
- `getSignedUrl(bucket, key, expiration)` → returns a pre-signed URL for time-limited direct access (production only).

## Required Semantics

- **Encryption at rest:** all objects must be encrypted. Server-side encryption (SSE) by default. Application-layer encryption for Restricted/PHI data.
- **Encryption in transit:** TLS 1.2+ for all storage operations.
- **Consistency:** read-after-write consistency for `put` followed by `get`. Eventual consistency acceptable for `list` operations.
- **Key naming convention:** `<service>/<entity-type>/<id>/<filename>` (e.g., `order-service/invoices/12345/invoice.pdf`).
- **Metadata:** every stored object must include `contentType`, `uploadedBy`, `uploadedAt`, and `correlationId` in metadata.
- **Size limits:** enforce a configurable max object size (default 100MB). Reject oversized uploads immediately.
- **Lifecycle:** define retention and expiration rules per bucket. Expired objects auto-deleted.

## Error Handling

- `ObjectNotFoundException` → on get/delete of non-existent key. Caller decides how to handle.
- Storage errors (network, quota) → retry with exponential backoff (3 retries, 500ms initial). After exhaustion, throw a typed exception.
- Never silently return null on a storage failure. Distinguish between "not found" and "error."

## Observability

- Metrics: `<service>_storage_put_total`, `<service>_storage_get_total`, `<service>_storage_delete_total`, `<service>_storage_errors_total`, `<service>_storage_latency_seconds`, `<service>_storage_bytes_uploaded_total`, `<service>_storage_bytes_downloaded_total`.
- Create spans for each storage operation.
- Log upload/download operations at INFO level with `correlationId`, bucket, and key (never log full object content).

## Production vs Local Differences

- **Production:** S3, Azure Blob Storage, GCS, or equivalent managed object store. Server-side encryption, lifecycle policies, access logging.
- **Local / fallback (`FALLBACK_STORAGE=local`):** local filesystem under a configurable directory (e.g., `./data/storage/`). No encryption. No lifecycle management. Acceptable for development only.
- Fallback must never be active in production. Enforce via startup validation.

## Java Example

```java
public interface ObjectStorageProvider {
    void put(String bucket, String key, InputStream data, ObjectMetadata metadata);
    StorageObject get(String bucket, String key);
    void delete(String bucket, String key);
    boolean exists(String bucket, String key);
    Page<String> list(String bucket, String prefix, ListOptions options);
    URL getSignedUrl(String bucket, String key, Duration expiration);
}

@Component
@Profile("!fallback-storage")
public class S3ObjectStorageProvider implements ObjectStorageProvider {
    // AWS S3 implementation with SSE, retry, tracing
}

@Component
@Profile("fallback-storage")
public class LocalFileObjectStorageProvider implements ObjectStorageProvider {
    // Local filesystem implementation
}
```

## Python Example

```python
class ObjectStorageProvider(Protocol):
    def put(self, bucket: str, key: str, data: BinaryIO, metadata: ObjectMetadata) -> None: ...
    def get(self, bucket: str, key: str) -> StorageObject: ...
    def delete(self, bucket: str, key: str) -> None: ...
    def exists(self, bucket: str, key: str) -> bool: ...
    def list(self, bucket: str, prefix: str, options: ListOptions | None = None) -> Page[str]: ...
    def get_signed_url(self, bucket: str, key: str, expiration: timedelta) -> str: ...
```

## Anti-Patterns

- **Unencrypted storage in production:** all objects must be encrypted at rest and in transit.
- **No metadata on stored objects:** every object must have contentType, uploadedBy, uploadedAt.
- **Unbounded uploads:** always enforce a max object size.
- **Using storage as a database:** object storage is for blobs, not structured queries.

## LLM Instructions

- When adding file storage to a service, use `ObjectStorageProvider`, not direct S3/Blob SDK calls.
- Always include encryption configuration and metadata on uploads.
- Ask the user about retention/lifecycle requirements.
- Wire fallback via Spring profile or Python dependency injection.

## Review Checklist

- [ ] All objects encrypted at rest (SSE or application-layer for PHI).
- [ ] Key naming follows `<service>/<entity>/<id>/<filename>` convention.
- [ ] Metadata includes `contentType`, `uploadedBy`, `uploadedAt`, `correlationId`.
- [ ] Max object size enforced.
- [ ] Retry policy on transient failures.
- [ ] Metrics emitted for puts, gets, deletes, errors, and bytes.
- [ ] Fallback implementation exists for local development.
- [ ] Fallback cannot activate in production.
