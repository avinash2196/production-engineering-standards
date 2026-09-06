# Repository-Wide Copilot Instructions

This repository provides production-engineering customizations. Apply these rules unless a more specific path instruction narrows them.

## Control Boundaries

- Do not invent requirements when material behavior is unclear.
- Do not mark a Plan or Implementation Plan approved on behalf of a human reviewer.
- Do not claim tests, commands, validators, migrations, or deployments passed unless they were actually executed or evidence was supplied.
- Keep behavior-changing RED, GREEN, and optional REFACTOR phases separate when the adopting project uses the PDD workflow.
- Prefer the smallest safe change that satisfies the approved scope.
- Preserve public contracts unless an approved plan explicitly changes them.

## Engineering Baseline

- Treat correctness, data integrity, security, observability, and operability as design concerns, not post-processing.
- Prefer explicit dependency boundaries and dependency injection.
- Never log secrets, tokens, credentials, or sensitive payloads without an approved reason and protection.
- Handle errors deliberately; do not silently swallow failures.
- Add or update tests for behavior changes.
- Make degraded behavior explicit, observable, testable, and unable to activate silently.
- Separate local-development adapters from production degradation strategies.
- Use idempotency where retries or duplicate delivery can repeat side effects.
- Document material trade-offs instead of presenting one architecture choice as universally correct.

## Skills

Use a skill when specialized knowledge is relevant. Do not load every skill for every task.

Examples:
- architecture/distributed-system work → architecture-design and distributed-systems
- Spring Boot work → java-spring-boot
- API changes → api-design
- failure handling → resilience-and-degradation
- Oracle → PostgreSQL modernization → oracle-to-postgres-modernization

## Human Review

Human review remains required for requirement interpretation, phase approval, architecture trade-offs, production-readiness decisions, and exceptions.
