# Java Microservice Reference Architecture

This directory is a documentation-only reference for how a Java/Spring Boot service can organize API, application, domain, ports, persistence, and infrastructure adapter concerns.

It is **not an executable project**: no Maven wrapper, build file, or source tree is included here. Use the Java stack template and an approved implementation plan when creating a runnable service.

## Intended Workflow

1. Create and approve a service plan.
2. Inspect the target repository and approve an implementation plan with exact files and tests.
3. Add tests for the first behavior and confirm the expected failure.
4. implement the smallest Spring Boot change required for green.
5. Refactor only while tests remain green.

## Suggested Structure

```text
src/main/java/<base-package>/
  api/                 transport and DTO mapping
  application/         use-case orchestration
  domain/              business rules where complexity justifies them
  ports/               repository and capability contracts
  infrastructure/      JPA and vendor/local adapter implementations
  config/              composition, typed configuration, production guards
```

A straightforward CRUD service may combine some areas when the decision is documented and dependencies remain controlled.

## Local Adapter Example

A local profile may select:

```yaml
adapters:
  messaging: db
  cache: jsonfile
  storage: local
  secrets: env
```

These are local development choices, not production failover. Startup validation must reject local-only values in production. A database-backed outbox is preferred over an in-memory queue when restart durability and inspectability matter during development.

## References

- [Java/Spring standards](../../stacks/java-springboot/java-spring.md)
- [Prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md)
- [Local adapter strategy](../../standards/local-adapter-strategy.md)
- [Production degradation strategy](../../standards/fallback-strategy.md)
