# Object Storage Integration — Python FastAPI

## Purpose

Wire S3 or GCS behind `ObjectStorageProvider` and optionally provide a local filesystem adapter for approved development/testing. Local storage does not reproduce managed durability, IAM, encryption policy, lifecycle, replication, or multi-instance behavior.

## Required Workflow

1. Plan object keys, ownership, size limits, content types, encryption, retention, and asynchronous acceptance semantics.
2. Approve exact adapters, endpoints, tests, and deployment configuration.
3. Add failing tests for validation, object-not-found behavior, selection, path safety, and production guards.
4. Implement the minimum provider behavior.
5. Run focused and object-store integration tests.
6. Refactor after green.

## Typed Selection

```python
class StorageAdapter(StrEnum):
    S3 = "s3"
    GCS = "gcs"
    LOCAL = "local"
```

```python
def get_storage(settings: Settings) -> ObjectStorageProvider:
    if settings.storage_adapter is StorageAdapter.LOCAL:
        return LocalFileStorageProvider(settings.local_storage_path)
    if settings.storage_adapter is StorageAdapter.GCS:
        return GcsObjectStorageProvider(
            project_id=settings.gcp_project_id,
            bucket=settings.gcs_bucket,
        )
    return S3ObjectStorageProvider(
        bucket=settings.s3_bucket,
        region=settings.s3_region,
        endpoint_url=settings.s3_endpoint_url or None,
    )
```

Production startup rejects `LOCAL`.

## Provider Requirements

- Validate object keys and prevent path traversal.
- Enforce upload size and accepted content types at the API boundary.
- Define whether success means durable upload completion or asynchronous acceptance.
- Configure request timeouts and bounded retries.
- Map vendor not-found responses to a stable application error.
- Avoid buffering unbounded uploads in memory; stream when required by the plan.
- Use short-lived signed URLs and least-privilege identity.
- Emit operation count, error, duration, and byte metrics without logging object contents.

## Local Filesystem Adapter

Use a configured base directory and resolve every object key beneath it. Tests should use a temporary directory and verify:

- upload/download/delete/exists behavior;
- nested key handling;
- path traversal rejection;
- restart persistence;
- production selection rejection.

## Production Failure Behavior

Do not silently report success when durable storage has not completed unless the API contract explicitly returns an asynchronous acceptance status backed by a durable pending record. For unavailable storage, choose reject/fail fast or durable queueing based on the approved design.

## Verification

- unit tests for endpoint validation and error mapping;
- local filesystem contract tests;
- Testcontainers LocalStack or a supported emulator for the chosen provider;
- signed URL and authorization tests where applicable;
- production guard and provider-selection tests.

## References

- [ObjectStorageProvider](../../../contracts/ObjectStorageProvider.md)
- [Storage local adapter detail](../../../standards/fallbacks/storage-fallback.md)
- [Security standards](../../../standards/security/security-standards.md)
