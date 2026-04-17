# Capability Pattern

## Purpose

Define the architectural pattern used across this repository for abstracting infrastructure dependencies behind capability interfaces. This document explains the pattern, why every infrastructure dependency must use it, and how to wire production and fallback implementations.

## The Pattern

Every external dependency (message broker, cache, object storage, secret store, database) is accessed through a **capability interface** — a technology-agnostic contract that defines what the service needs, not how it's implemented.

```
Service Code  →  Capability Interface  →  Production Implementation (Kafka, Redis, S3, Vault)
                                       →  Fallback Implementation (in-memory, local file, env vars)
```

The service code depends only on the interface. The concrete implementation is injected at runtime based on configuration (Spring profiles, Python dependency injection).

## Why This Pattern

1. **Testability:** unit tests mock the interface. No need for running Kafka, Redis, or S3 in unit tests.
2. **Local development:** developers run the service without external infrastructure using fallback implementations.
3. **Portability:** switching from Redis to Memcached or from S3 to Azure Blob requires only a new implementation of the interface.
4. **Consistency:** all services use the same contracts, making cross-service code review and onboarding easier.

## Capability Interfaces in This Repository

| Capability | Interface | Production Example | Fallback |
|-----------|-----------|-------------------|----------|
| Messaging (publish) | `MessagePublisher` | Kafka, RabbitMQ | In-memory bus |
| Messaging (subscribe) | `MessageSubscriber` | Kafka consumer group | In-memory bus |
| Caching | `CacheProvider` | Redis | `ConcurrentHashMap` / `dict` |
| Object storage | `ObjectStorageProvider` | S3, Azure Blob | Local filesystem |
| Secrets | `SecretProvider` | Vault, Key Vault | Environment variables |
| Configuration | `ConfigProvider` | Spring Cloud Config, Consul | Env vars + local files |

## Implementation Rules

### 1. Interface Design

- Define the interface with domain-meaningful methods, not technology-specific ones.
- Use `publish(topic, message)`, not `kafkaSend(topic, key, value, headers)`.
- Include error types in the interface contract (e.g., `ObjectNotFoundException` for storage).

### 2. Production Implementation

- Implements the interface against the real infrastructure.
- Includes retry logic, connection pooling, health checks, and metrics.
- Activated by default (or by explicit production profile).

### 3. Fallback Implementation

- Implements the same interface with simple, local-only behavior.
- Must be functionally correct enough for development and testing.
- No durability, no clustering, no encryption required.
- Activated by a fallback toggle (environment variable or profile).
- **Must never be active in production.** Enforced by startup validation.

### 4. Wiring

**Java (Spring profiles):**
```java
@Component
@Profile("!fallback-kafka")
public class KafkaMessagePublisher implements MessagePublisher { ... }

@Component
@Profile("fallback-kafka")
public class InMemoryMessagePublisher implements MessagePublisher { ... }
```

**Python (dependency injection):**
```python
def get_message_publisher(settings: Settings) -> MessagePublisher:
    if settings.FALLBACK_KAFKA:
        return InMemoryMessagePublisher()
    return KafkaMessagePublisher(settings.kafka_config)
```

### 5. Fallback Toggles

| Toggle | Default | Production | Local Dev |
|--------|---------|-----------|-----------|
| `FALLBACK_KAFKA=true` | `false` | **Must be false** | `true` |
| `FALLBACK_CACHE=inmemory` | unset | **Must be unset** | `inmemory` |
| `FALLBACK_STORAGE=local` | unset | **Must be unset** | `local` |
| `FALLBACK_SECRETS=env` | unset | **Must be unset** | `env` |

### 6. Startup Validation

Every service must validate at startup:
- If running in a production environment, ensure no fallback toggles are active.
- Log the active implementation for each capability at INFO level.
- Fail startup if a fallback is detected in production.

## Adding a New Capability

1. Define the interface in `core/abstractions/<Name>.md` following the template of existing ones.
2. Provide Java and Python interface definitions with method signatures, semantics, and error types.
3. Document production vs fallback differences.
4. Define the fallback toggle.
5. Add to the table above.
6. Update `standards/` if the capability intersects with existing standards (e.g., new messaging type → update messaging-abstraction.md).

## LLM Instructions

- When a service needs an infrastructure dependency, always use the corresponding capability interface.
- Never generate code that directly imports a vendor SDK in service-layer or domain-layer code.
- Controller and configuration layers may reference vendor-specific code for wiring.
- If no capability interface exists for a dependency, flag it and propose one following this pattern.

## Review Checklist

- [ ] Service code depends only on capability interfaces, not vendor SDKs.
- [ ] Production and fallback implementations both exist.
- [ ] Fallback is wired via profile/toggle, not conditional logic in business code.
- [ ] Startup validates no fallback is active in production.
- [ ] Active implementation logged at startup.
