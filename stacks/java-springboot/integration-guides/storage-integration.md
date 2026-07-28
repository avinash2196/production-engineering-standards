# Object Storage Integration — Java Spring Boot

## Purpose

Implement S3 or GCS behind `ObjectStorageProvider` and optionally a local filesystem adapter for approved development/testing.

## Delivery Sequence

1. Plan object keys, size/content rules, encryption, retention, ownership, and durable-success semantics.
2. Approve exact classes, configuration, tests, and deployment changes.
3. Add failing tests for validation, not-found/error mapping, path safety, selection, and production guards.
4. Implement the minimum provider behavior.
5. Run focused and emulator/Testcontainers integration tests.
6. Refactor after green.

## Configuration and Composition

```yaml
adapters:
  storage: ${STORAGE_ADAPTER:s3}
```

```java
@Bean
@ConditionalOnProperty(name = "adapters.storage", havingValue = "s3")
ObjectStorageProvider s3Storage(S3Client client, StorageProperties properties) {
    return new S3ObjectStorageProvider(client, properties.bucket());
}

@Bean
@ConditionalOnProperty(name = "adapters.storage", havingValue = "local")
ObjectStorageProvider localStorage(LocalStorageProperties properties) {
    return new LocalFileStorageProvider(properties.root());
}
```

Production accepts `s3` or `gcs`; it rejects `local`.

## Requirements

- prevent path traversal in local storage;
- enforce upload size and accepted content type at the API boundary;
- use least-privilege identity and required encryption;
- define timeouts, bounded retries, and not-found versus dependency errors;
- do not report durable success before upload completion unless a durable asynchronous contract is approved;
- avoid logging object contents or credentials.

## Verification

- unit tests for API validation/error mapping;
- local filesystem contract and traversal tests;
- LocalStack/emulator integration for the selected provider;
- signed URL policy tests where used;
- selection and production-guard tests;
- failure-path tests for unavailable storage.

## References

- [ObjectStorageProvider](../../../contracts/ObjectStorageProvider.md)
- [Storage local adapter](../../../standards/fallbacks/storage-fallback.md)
- [Security standards](../../../standards/security/security-standards.md)
