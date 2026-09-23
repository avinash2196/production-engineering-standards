# Capability Boundaries

Use interfaces/adapters when the application needs a stable business-facing capability boundary across providers or local/testing implementations.

Common capability examples:
- CacheProvider
- ConfigProvider
- MessagePublisher / MessageSubscriber
- ObjectStorageProvider
- SecretProvider

Do not create an abstraction merely to hide one framework call. A useful capability boundary should isolate meaningful provider behavior, testing concerns, portability, failure behavior, or ownership.

Production and local adapters must document their different guarantees.
