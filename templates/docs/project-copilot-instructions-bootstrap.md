---
# How to use this file:
# 1. Copy this file to .github/copilot-instructions.md in your project.
# 2. Set STANDARDS_REPO_PATH to the local path where you cloned enterprise-ai-engineering.
# 3. Done — Copilot will enforce all org standards in that project automatically.
---

# Engineering Standards Bootstrap

This project follows the enterprise-ai-engineering standards.
Full rules, checklists, and examples live in the shared standards repo.

> **Standards repo path (update this):**
> `../enterprise-ai-engineering` ← adjust to your local clone path

---

## Architecture — Always Enforce

5-layer model. Dependencies flow **downward only**:

```
Controller → Service → Domain → Repository → Infrastructure
```

- **Controller/API**: routing + DTO binding only. No business logic.
- **Service**: business logic. Injects capability interfaces — never Kafka/Redis/S3 directly.
- **Domain**: pure business objects. Zero framework dependencies.
- **Repository**: data access. One class per aggregate root.
- **Infrastructure**: capability implementations + fallbacks.

Full rules: `{STANDARDS_REPO}/core/architecture.md`

---

## Capability Interfaces — Always Inject, Never Concrete Classes

| Interface | Use for |
|-----------|---------|
| `MessagePublisher` / `MessageSubscriber` | Messaging (Kafka) |
| `CacheProvider` | Caching (Redis) |
| `ObjectStorageProvider` | File storage (S3/MinIO) |
| `SecretProvider` | Secrets (Vault/Key Vault) |
| `ConfigProvider` | Runtime configuration |

Full specs: `{STANDARDS_REPO}/core/abstractions/`

---

## Fallback Toggles — Required in Every Service

Every service must run with zero infrastructure:

```bash
FALLBACK_KAFKA=true FALLBACK_CACHE=inmemory FALLBACK_STORAGE=local FALLBACK_SECRETS=env
```

Full guide: `{STANDARDS_REPO}/core/fallbacks/fallback-strategy.md`

---

## Non-Negotiable Rules

1. Domain objects have **zero** framework imports.
2. Secrets always via `SecretProvider` — never hardcoded or raw env vars.
3. All services emit structured JSON logs, Prometheus metrics, and OTEL traces from day one.
4. No N+1 queries — every collection fetch uses a join or batch.
5. Every external call has a timeout and a documented fallback.

Full principles: `{STANDARDS_REPO}/core/principles.md`

---

## Standards Quick Reference

| Concern | File in standards repo |
|---------|----------------------|
| Naming, method/class size | `standards/coding-standards.md` |
| Request / response DTOs | `standards/dto-guidelines.md` |
| API design | `standards/api-design.md` |
| Security, TLS, secrets | `standards/security/security-standards.md` |
| Observability | `standards/observability.md` |
| Testing strategy | `standards/testing/unit-testing.md` |
| Performance limits | `standards/performance/performance.md` |
| HIPAA controls | `standards/compliance/hipaa-controls.md` |

---

## Stack Conventions

- **Java 21 + Spring Boot 3.x**: `{STANDARDS_REPO}/stacks/java-springboot/java-spring.md`
- **Python 3.12+ + FastAPI**: `{STANDARDS_REPO}/stacks/python-fastapi/python-backend.md`

---

## Slash Commands (available if prompt files are installed)

Type `/` in Copilot Chat:
- `/scaffold-service` — generate a complete new service following all org standards
- `/compliance-review` — audit a service against security and compliance checklists

Install prompts: copy `{STANDARDS_REPO}/.github/prompts/*.prompt.md` → `.github/prompts/` in this repo.
The prompt files already declare `tools` in their frontmatter — no edits needed after copying.
