# Java Microservice Example

Minimal example demonstrating `core` abstractions and fallbacks in a Java Spring Boot service.

## Overview

A simple order-service that implements the standard layered architecture with all capability interfaces wired (production + fallback). Use this as a reference for how a real service consumes the enterprise standards.

## Structure

```
java-microservice/
├── src/main/java/com/myorg/orderservice/
│   ├── controller/
│   │   └── OrderController.java        # REST endpoints
│   ├── service/
│   │   └── OrderService.java           # Business logic
│   ├── domain/
│   │   ├── Order.java                  # Entity
│   │   └── OrderStatus.java            # Enum
│   ├── repository/
│   │   └── OrderRepository.java        # JPA repository
│   ├── infrastructure/
│   │   ├── messaging/                  # KafkaMessagePublisher
│   │   ├── cache/                      # RedisCacheProvider
│   │   ├── storage/                    # S3ObjectStorageProvider
│   │   └── fallback/                   # All in-memory fallbacks
│   └── config/
├── src/main/resources/
│   ├── application.yml
│   └── application-local.yml
├── src/test/java/
│   ├── unit/                           # Unit tests with mocks
│   └── integration/                    # Testcontainers-based tests
├── Dockerfile
├── docker-compose.dev.yml
├── pom.xml
└── .env.local
```

## Running

```bash
cd examples/java-microservice

# With fallbacks (zero infra)
FALLBACK_KAFKA=true FALLBACK_CACHE=inmemory FALLBACK_STORAGE=local FALLBACK_SECRETS=env \
  ./mvnw spring-boot:run -Dspring-boot.run.profiles=local

# With real infra
docker compose -f docker-compose.dev.yml up -d
./mvnw spring-boot:run -Dspring-boot.run.profiles=local
```

## Key Patterns Demonstrated

| Pattern | Where |
|---------|-------|
| Layered architecture | `controller/ → service/ → domain/ → repository/` |
| Capability interface usage | Service injects `MessagePublisher`, `CacheProvider` |
| Fallback activation | `@Profile("fallback-kafka")` on fallback beans |
| DTO separation | Request/response records in `controller/dto/` |
| Structured logging | JSON format with traceId, spanId |
| Health checks | `/actuator/health` with readiness + liveness groups |
| Unit testing | Mocked capability interfaces in `unit/` |
| Integration testing | Testcontainers in `integration/` |

## References

- [Java Spring Boot stack](../../stacks/java-springboot/README.md)
- [Core architecture](../../core/architecture.md)
- [Core abstractions](../../core/abstractions/)
