# Storage Abstraction

Purpose
- Define the `ObjectStorageProvider` capability and required semantics for production and approved local adapters.

Mandatory Rules
- Implementations must document consistency and durability guarantees (strong, eventual, best-effort).
- Providers must support server-side encryption options and enforce encryption at rest for sensitive containers.
- Provide a local disk adapter with configurable root path for dev/test.

Defaults
- Production adapters use cloud object storage with server-side encryption; local dev uses `./local-storage` or a mounted directory.

Anti-patterns
- Directly coupling business code to cloud SDKs; leaking SDK-specific types into domain models.

Abstraction Patterns
- Define a small, stable interface: `put(key, stream|bytes, metadata)`, `get(key) -> stream|bytes`, `delete(key)`, `list(prefix)`, and `presign(key, ttl)`.
- Return/accept opaque metadata maps for extensibility; avoid returning SDK-specific handle types.

Production vs Local Differences
- Production: strong durability SLAs, replication, and access controls. Local: best-effort file writes without replication. Tests must account for differences.

LLM instructions
- When generating adapters, scaffold both the cloud-backed provider and the local file-backed provider and add explicit tests validating the contract semantics.
- Ask the user if objects will be used as event triggers (e.g., object create events) because this affects adapter responsibilities.

Review checklist
- [ ] `ObjectStorageProvider` interface documented and used.
- [ ] Cloud and local adapters included in templates.
- [ ] Encryption-at-rest and access controls documented for production.
