# Storage Abstraction

## Purpose

Guidance for object/blob/file storage boundaries. Use the optional `ObjectStorageProvider` capability when it creates a real testing, portability, policy, or vendor-isolation boundary.

## Required Decisions

For each adopted storage flow, define what matters:

- durability/availability expectations;
- consistency/listing semantics relied upon;
- object size/streaming behavior;
- naming/namespace/tenant boundaries;
- access-control and sensitive-data protection requirements;
- lifecycle/retention/deletion behavior where applicable;
- timeout/retry/failure behavior;
- presigned/delegated access semantics if used.

Do not assume every provider supports the same consistency, encryption, metadata, event, or URL-signing semantics.

## Boundary

Keep vendor SDK-specific types out of business/application code when the project has adopted a storage capability boundary. Direct SDK use in an infrastructure-only component can be perfectly valid.

A local filesystem adapter is optional and should be created only when local/CI execution benefits from it more than mocks, an emulator, or another controlled fixture. Document reduced guarantees and prevent local-only behavior from becoming a production fallback.

## LLM Instructions

- Confirm storage requirements and selected backend before defining the contract surface.
- Do not scaffold cloud + local providers automatically.
- Keep the interface as small as the approved use cases require.

## Review Checklist

- [ ] Required storage semantics/limits are explicit.
- [ ] Any abstraction has a concrete purpose.
- [ ] Sensitive-data/access/lifecycle controls match project policy.
- [ ] Local/test strategy is justified and documents reduced guarantees.
