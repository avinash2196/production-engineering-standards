# Java Microservice Reference Architecture

This directory is a documentation-only reference for how a Java/Spring Boot service can organize API, application, domain, ports, persistence, and infrastructure adapter concerns.

It is **not an executable project**: no Maven wrapper, build file, or source tree is included here. Use the Java stack template only after the service Plan and the current phase-specific Implementation Plan are approved.

## Intended Workflow

1. Create and approve a service Plan with separate RED and GREEN milestones and an optional REFACTOR milestone when justified.
2. Inspect the target repository and approve the RED milestone Implementation Plan; add only the approved tests/checks, confirm valid RED, record evidence, and stop.
3. Approve the GREEN milestone Implementation Plan only after the predecessor RED evidence is reviewed; implement the smallest Spring Boot change required for GREEN, run regression checks, record evidence, and stop.
4. When concrete cleanup is justified, approve a separate REFACTOR milestone Implementation Plan, preserve behavior, keep tests GREEN, and stop.
5. Do not auto-advance between phase milestones or authorize multiple phases from one Implementation Plan.

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
