---
description: "Use when creating a new service, microservice, API, or backend application. Covers project structure, capability interface wiring, fallback setup, testing scaffold, and Dockerfile generation for Java Spring Boot or Python FastAPI."
---

Follow the scaffolding procedure in [workflows/create-new-service.md](../../workflows/create-new-service.md) and the full spec in [agents/scaffolding-agent/spec.md](../../agents/scaffolding-agent/spec.md).

## What to Generate

For every new service, produce **all** of the following — no partial scaffolds:

1. **Project structure** matching the layered layout for the chosen stack:
   - Java: [stacks/java-springboot/project-template/](../../stacks/java-springboot/project-template/)
   - Python: [stacks/python-fastapi/project-template/](../../stacks/python-fastapi/project-template/)

2. **Source files** for each layer (Controller/API, Service, Domain, Repository, Infrastructure).

3. **Capability interface wiring** — only for the capabilities the user requests:
   - Messaging → `MessagePublisher` + `MessageSubscriber`
   - Cache → `CacheProvider`
   - Object storage → `ObjectStorageProvider`
   - Secrets → `SecretProvider`
   - Each must include a **production implementation AND a fallback implementation**.

4. **Configuration**:
   - Java: `application.yml` + `application-local.yml` (all fallbacks enabled)
   - Python: `app/config/settings.py` with `FALLBACK_*` toggles

5. **Tests**:
   - At least one unit test per service class (mock capability interfaces)
   - At least one integration test per infrastructure adapter (Testcontainers)

6. **`docker-compose.dev.yml`** with PostgreSQL, Redis, Kafka (KRaft), MinIO.

7. **`.env.local`** with all fallback toggles enabled.

8. **`Dockerfile`** — multi-stage, non-root user.

9. **`README.md`** with quick-start and fallback run commands.

## Checklist Before Finishing

- [ ] Domain classes have zero framework imports
- [ ] Services inject interfaces, not concrete infrastructure classes
- [ ] All `FALLBACK_*` vars are connected to DI wiring
- [ ] Health/liveness/readiness endpoints present
- [ ] Structured logging with correlation ID configured
- [ ] Prometheus metrics endpoint exposed
- [ ] At least one unit test and one integration test generated
