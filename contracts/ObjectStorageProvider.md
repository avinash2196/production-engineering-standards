# ObjectStorageProvider

## Purpose

Define the file/blob storage behavior application code needs without exposing S3, GCS, or filesystem details throughout the service.

## Contract Decisions

Select only required operations such as upload, download, delete, exists, list, or signed URL. Document:

- object key format and ownership;
- maximum size and accepted content types;
- durable-success versus asynchronous-acceptance semantics;
- encryption and access policy;
- retention/lifecycle requirements;
- not-found versus dependency-error behavior;
- timeout/retry policy;
- metadata and audit needs.

## Production and Local Implementations

| Selection | Use | Limitation |
|---|---|---|
| `s3` / `gcs` | managed object storage | provider-specific IAM, lifecycle, and durability |
| `local` | development/test filesystem | no managed durability, IAM, lifecycle, replication, or multi-instance semantics |

Production startup rejects `local`.

## Security Rules

- Reject absolute/path-traversal keys in local storage.
- Enforce upload limits at the transport boundary.
- Do not log object contents or credentials.
- Use short-lived signed URLs and least-privilege identities.
- Do not report durable success before storage confirmation unless the API explicitly accepts work asynchronously through a durable pending record.

## Composition

```java
@Bean
@ConditionalOnProperty(name = "adapters.storage", havingValue = "local")
ObjectStorageProvider localStorage(LocalStorageProperties properties) {
    return new LocalFileStorageProvider(properties.root());
}
```

```python
if settings.storage_adapter is StorageAdapter.LOCAL:
    return LocalFileStorageProvider(settings.local_storage_path)
```

## Test-First Requirements

- upload/download/delete/not-found behavior;
- size/content validation;
- path traversal rejection;
- timeout/error translation;
- signed URL policy where selected;
- local selection and production rejection;
- emulator/Testcontainers integration for the production provider.

## Review Checklist

- [ ] Durable success semantics are explicit
- [ ] Object keys and upload limits are validated
- [ ] Security/retention requirements come from approved scope
- [ ] Local filesystem limitations and production guard are tested
