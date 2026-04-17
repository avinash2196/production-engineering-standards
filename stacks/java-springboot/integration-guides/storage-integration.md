# Storage Integration (Java Spring Boot)

## Purpose

Step-by-step guide for wiring object storage (S3, Azure Blob, GCS) into a Spring Boot service through the `ObjectStorageProvider` capability interface, covering SDK configuration, streaming uploads/downloads, presigned URLs, observability, and fallback setup.

## Dependencies

Choose one SDK based on the target cloud:

```xml
<!-- AWS S3 (default) -->
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3</artifactId>
</dependency>

<!-- Azure Blob -->
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-storage-blob</artifactId>
</dependency>
```

## Configuration

```yaml
# application.yml
storage:
  provider: ${STORAGE_PROVIDER:s3}          # s3 | azure-blob | gcs
  bucket: ${STORAGE_BUCKET:my-app-files}
  region: ${STORAGE_REGION:us-east-1}
  endpoint: ${STORAGE_ENDPOINT:}            # blank = default cloud endpoint
  max-upload-size: 100MB
  presigned-url-expiry: 15m
```

## ObjectStorageProvider Implementation (S3)

```java
@Component
@Profile("!fallback-storage")
@ConditionalOnProperty(name = "storage.provider", havingValue = "s3")
public class S3ObjectStorageProvider implements ObjectStorageProvider {
    private final S3Client s3;
    private final S3Presigner presigner;
    private final MeterRegistry meterRegistry;
    private final StorageProperties props;

    @Override
    public void upload(String key, InputStream data, long contentLength, String contentType) {
        Timer.Sample sample = Timer.start(meterRegistry);
        try {
            PutObjectRequest request = PutObjectRequest.builder()
                .bucket(props.getBucket())
                .key(key)
                .contentType(contentType)
                .contentLength(contentLength)
                .serverSideEncryption(ServerSideEncryption.AES256)
                .build();
            s3.putObject(request, RequestBody.fromInputStream(data, contentLength));
            meterRegistry.counter("storage_uploads_total").increment();
            meterRegistry.counter("storage_bytes_uploaded_total").increment(contentLength);
        } catch (S3Exception e) {
            meterRegistry.counter("storage_errors_total", "op", "upload").increment();
            throw new StorageOperationException("Upload failed: key=" + key, e);
        } finally {
            sample.stop(meterRegistry.timer("storage_operation_duration", "op", "upload"));
        }
    }

    @Override
    public InputStream download(String key) {
        try {
            ResponseInputStream<GetObjectResponse> response = s3.getObject(
                GetObjectRequest.builder().bucket(props.getBucket()).key(key).build());
            meterRegistry.counter("storage_downloads_total").increment();
            return response;
        } catch (NoSuchKeyException e) {
            throw new ObjectNotFoundException(key);
        } catch (S3Exception e) {
            meterRegistry.counter("storage_errors_total", "op", "download").increment();
            throw new StorageOperationException("Download failed: key=" + key, e);
        }
    }

    @Override
    public void delete(String key) {
        s3.deleteObject(DeleteObjectRequest.builder()
            .bucket(props.getBucket()).key(key).build());
        meterRegistry.counter("storage_deletes_total").increment();
    }

    @Override
    public URI getSignedUrl(String key, Duration expiry) {
        PresignedGetObjectRequest presigned = presigner.presignGetObject(
            GetObjectPresignRequest.builder()
                .signatureDuration(expiry)
                .getObjectRequest(b -> b.bucket(props.getBucket()).key(key))
                .build());
        return presigned.url().toURI();
    }

    @Override
    public boolean exists(String key) {
        try {
            s3.headObject(HeadObjectRequest.builder()
                .bucket(props.getBucket()).key(key).build());
            return true;
        } catch (NoSuchKeyException e) {
            return false;
        }
    }
}
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

**Rules:**
- No leading `/`.
- All lowercase, hyphens for word separation.
- Move from `tmp/` to permanent path after validation.

## Streaming Large Files

For files > 100 MB, use multipart upload:

```java
public void uploadLarge(String key, Path filePath) {
    CreateMultipartUploadRequest create = CreateMultipartUploadRequest.builder()
        .bucket(props.getBucket()).key(key).build();
    String uploadId = s3.createMultipartUpload(create).uploadId();

    // Upload parts in 10 MB chunks
    List<CompletedPart> parts = new ArrayList<>();
    try (InputStream is = Files.newInputStream(filePath)) {
        byte[] buffer = new byte[10 * 1024 * 1024];
        int partNumber = 1;
        int bytesRead;
        while ((bytesRead = is.read(buffer)) > 0) {
            UploadPartResponse response = s3.uploadPart(
                UploadPartRequest.builder()
                    .bucket(props.getBucket()).key(key)
                    .uploadId(uploadId).partNumber(partNumber).build(),
                RequestBody.fromBytes(Arrays.copyOf(buffer, bytesRead)));
            parts.add(CompletedPart.builder()
                .partNumber(partNumber++).eTag(response.eTag()).build());
        }
    }
    s3.completeMultipartUpload(CompleteMultipartUploadRequest.builder()
        .bucket(props.getBucket()).key(key).uploadId(uploadId)
        .multipartUpload(CompletedMultipartUpload.builder().parts(parts).build())
        .build());
}
```

## Fallback Wiring

```java
@Component
@Profile("fallback-storage")
public class LocalFileStorageProvider implements ObjectStorageProvider {
    // See core/fallbacks/storage-fallback.md for implementation
}
```

Activate via:
```properties
FALLBACK_STORAGE=local
```

## Observability

| Metric | Description |
|--------|-------------|
| `storage_uploads_total` | Successful uploads |
| `storage_downloads_total` | Successful downloads |
| `storage_deletes_total` | Successful deletes |
| `storage_bytes_uploaded_total` | Total bytes uploaded |
| `storage_errors_total` | Operation failures by op type |
| `storage_operation_duration` | Latency histogram by operation |

## Testing

```java
@SpringBootTest
@Testcontainers
class S3StorageProviderTest {
    @Container
    static LocalStackContainer localstack = new LocalStackContainer(
            DockerImageName.parse("localstack/localstack:3"))
        .withServices(LocalStackContainer.Service.S3);

    @DynamicPropertySource
    static void overrideProperties(DynamicPropertyRegistry registry) {
        registry.add("storage.endpoint", () -> localstack.getEndpoint().toString());
        registry.add("storage.region", () -> localstack.getRegion());
    }

    @Autowired ObjectStorageProvider storageProvider;

    @Test
    void should_upload_and_download_file() {
        byte[] content = "hello".getBytes();
        storageProvider.upload("test/file.txt", 
            new ByteArrayInputStream(content), content.length, "text/plain");
        InputStream downloaded = storageProvider.download("test/file.txt");
        assertThat(downloaded.readAllBytes()).isEqualTo(content);
    }
}
```

## References

- [ObjectStorageProvider.md](../../../core/abstractions/ObjectStorageProvider.md)
- [storage-fallback.md](../../../core/fallbacks/storage-fallback.md)
- [security-standards.md](../../../standards/security/security-standards.md)
