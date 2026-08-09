# Glossary

Key terms used throughout this repository.

| Term | Definition |
|------|------------|
| **Capability Interface** | An abstract contract (e.g., `MessagePublisher`, `CacheProvider`) that decouples business logic from infrastructure. Production implementations and approved local adapters may be selected through dependency injection/configuration. |
| **Local Adapter** | An explicitly selected development/CI implementation of a capability, such as an in-memory queue or local filesystem, with documented reduced guarantees and a production startup guard. |
| **Adapter Selector** | Typed configuration such as `MESSAGING_ADAPTER` or `CACHE_ADAPTER` that selects an implemented production or local adapter. Local-only values must be rejected in production. |
| **DTO** | Data Transfer Object — a typed, validated structure used to carry data across API boundaries. Separate from domain objects. |
| **Domain Object** | A class representing business concepts (entities, value objects, aggregates). No framework dependencies. |
| **Aggregate Root** | The top-level domain object that controls access to a cluster of related entities. One repository per aggregate root. |
| **Correlation ID** | A unique identifier propagated across all services in a request chain for distributed tracing (header: `X-Correlation-ID` or W3C `traceparent`). |
| **Idempotency Key** | A client-provided identifier used to deduplicate messages and ensure exactly-once processing semantics. |
| **PHI** | Protected Health Information — any health-related data that can identify an individual. Subject to HIPAA controls. |
| **PII** | Personally Identifiable Information — data that can identify a person (name, email, SSN, etc.). |
| **BAA** | Business Associate Agreement — a HIPAA-required contract with third parties that handle PHI. |
| **DLT / DLQ** | Dead-Letter Topic / Dead-Letter Queue — a destination for messages that failed processing after all retries. |
| **Consumer-Driven Contract** | A testing pattern where the API consumer defines the expected interaction, and the provider verifies compliance. |
| **Pact** | A contract testing framework implementing consumer-driven contracts for HTTP and messaging. |
| **CacheProvider** | Capability interface for read/write caching operations with TTL support. |
| **MessagePublisher** | Capability interface for publishing messages/events to a topic. |
| **MessageSubscriber** | Capability interface for consuming messages/events from a topic. |
| **ObjectStorageProvider** | Capability interface for uploading, downloading, and managing files in object storage. |
| **SecretProvider** | Capability interface for retrieving secrets (API keys, passwords, certificates) from a secure store. |
| **ConfigProvider** | Capability interface for resolving configuration values from a prioritized chain of sources. |
| **SLO** | Service Level Objective — a target for service reliability (e.g., 99.9% availability, P95 latency < 250ms). |
| **Canary Deployment** | A release strategy that routes a small percentage of traffic to the new version before full rollout. |
| **Expand-then-Contract** | A database migration strategy where new schema is added first, data migrated, then old schema removed in a later release. |
| **Trunk-Based Development** | A branching model where all developers commit to `main` via short-lived feature branches (< 2 days). |
| **Feature Flag** | A runtime toggle that controls whether a feature is active, enabling incremental rollout and safe experimentation. |
| **Stale-While-Revalidate** | A caching pattern where expired data is served while a background refresh fetches updated data. |

## References

- [Overview](overview.md)
- [Engineering principles](../standards/engineering-principles.md)
- [Contracts](../contracts/)
