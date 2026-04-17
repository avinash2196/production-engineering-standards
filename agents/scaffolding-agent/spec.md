# Scaffolding Agent

Agent spec to scaffold projects from templates while respecting core abstractions and standards.

## Purpose

Generate new service projects that are wired to the organization's capability interfaces, follow the standard architecture, and include observability, fallbacks, and CI configuration out of the box.

## Capabilities

| Capability | Description |
|-----------|-------------|
| Project generation | Create a new service from stack-specific templates |
| Abstraction wiring | Wire `MessagePublisher`, `CacheProvider`, `ObjectStorageProvider`, `SecretProvider`, `ConfigProvider` with production + fallback beans |
| Config scaffolding | Generate environment-specific config files with correct resolution chain |
| CI pipeline generation | Create GitHub Actions workflow with build, test, lint, and contract test stages |
| Dockerfile generation | Create multi-stage Dockerfile following container best practices |
| README generation | Create service README with quickstart, architecture, and runbook links |

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Service name | Yes | e.g., `order-service` |
| Stack | Yes | `java-springboot` or `python-fastapi` |
| Capabilities needed | Yes | List from: `messaging`, `caching`, `storage`, `secrets` |
| Data categories | Yes | Data types handled (PHI, PII, internal, public) |
| Team / owner | Yes | Owning team for CODEOWNERS |
| Database | Optional | `postgresql` (default), `mysql`, `none` |
| API style | Optional | `rest` (default), `grpc` |

## Outputs

### Java Spring Boot

```
order-service/
├── src/main/java/com/myorg/orderservice/
│   ├── controller/
│   ├── service/
│   ├── domain/
│   ├── repository/
│   ├── infrastructure/
│   │   ├── messaging/     # if messaging selected
│   │   ├── cache/         # if caching selected
│   │   ├── storage/       # if storage selected
│   │   └── fallback/
│   └── config/
├── src/main/resources/
│   ├── application.yml
│   ├── application-local.yml
│   └── application-prod.yml
├── src/test/java/
├── Dockerfile
├── pom.xml
├── .github/workflows/ci.yml
├── .env.local
├── docker-compose.dev.yml
└── README.md
```

### Python FastAPI

```
order-service/
├── src/order_service/
│   ├── api/
│   ├── service/
│   ├── domain/
│   ├── repository/
│   ├── infrastructure/
│   ├── config/
│   └── main.py
├── tests/
├── Dockerfile
├── requirements.txt
├── .github/workflows/ci.yml
├── .env.local
├── docker-compose.dev.yml
└── README.md
```

## Guardrails

- Every generated project must compile/pass `mvn verify` or `pytest` before presenting to user.
- Fallback implementations must be present for all selected capabilities.
- Generated code must pass the compliance-review-agent's basic checks.
- No placeholder `// TODO` comments without an associated task description.
- Health check endpoints must be included.

## Post-Scaffold Checklist

The agent presents this checklist after generation:

- [ ] Review generated `README.md` and update service description.
- [ ] Verify capability interfaces match your requirements.
- [ ] Run `docker-compose -f docker-compose.dev.yml up` to validate local setup.
- [ ] Run full test suite: `./mvnw verify` or `pytest`.
- [ ] Run compliance review: `@compliance-review-agent review --service={name}`.
- [ ] Add to team's deployment pipeline.

## Invocation

```bash
@scaffolding-agent create \
  --name=order-service \
  --stack=java-springboot \
  --capabilities=messaging,caching,storage \
  --data-categories=PII,internal \
  --team=platform-team
```

## References

- [Project scaffold prompt](prompts/project-scaffold.prompt.md)
- [Architecture standard](../../standards/architecture.md)
- [Contracts](../../contracts/)
- [Java stack README](../../stacks/java-springboot/README.md)
- [Python stack README](../../stacks/python-fastapi/README.md)
