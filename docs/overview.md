# Overview

Production Engineering Standards is a reference repository for AI-assisted backend engineering. It captures engineering rules, review workflows, capability boundaries, stack guidance, project templates, and executable repository checks.

It is not a claim that one architecture, reliability target, or implementation choice fits every service. Adopting projects select the standards and enforcement mechanisms that apply to their requirements and operating context.

## What This Repository Provides

- **Engineering guidance** for architecture, testing, security, observability, reliability, performance, and production readiness.
- **Prompt-driven workflows** that separate Requirements, Plan, Implementation Plan, RED tests, GREEN implementation, refactoring, and final review.
- **Capability boundaries** for infrastructure concerns such as messaging, caching, storage, secrets, and configuration.
- **Local-adapter guidance** for development and CI without confusing local convenience with production failover.
- **Review agents and prompts** that make architecture, distributed-systems, security, compliance, and readiness reviews repeatable.
- **Executable repository checks** for rules that can be validated deterministically.

## Repository Structure

```text
.github/          Persistent Copilot guidance, task instructions, prompts, and repository CI
agents/           Agent responsibilities, guardrails, and review behavior
contracts/        Capability boundaries used by application code
standards/        Engineering rules and decision guidance
stacks/           Java/Spring Boot and Python/FastAPI stack guidance and templates
playbooks/        Delivery, local-development, review, and release procedures
templates/        Reusable planning, documentation, infrastructure, and monitoring templates
examples/         Reference architectures and documented behavior walkthroughs
tooling/          Dependency-free validator and repository tests
docs/             Overview, decisions, and enforcement status
```

## How to Use This Repository

### Developers

1. Start with [Engineering Principles](../standards/engineering-principles.md).
2. Follow the [Prompt-Driven Development Workflow](../standards/prompt-driven-development-workflow.md) for qualifying implementation work.
3. Read the standards relevant to the service rather than copying every rule blindly.
4. Use the [Java](../stacks/java-springboot/README.md) or [Python](../stacks/python-fastapi/README.md) stack guidance where applicable.
5. Use [Local Adapter Strategy](../standards/local-adapter-strategy.md) only when a local adapter adds value beyond mocks, Testcontainers, or an official emulator.

### AI-Assisted Work

- `.github/copilot-instructions.md` provides stable repository-level guidance.
- `.github/prompts/` contains repeatable planning, testing, implementation, refactoring, and review tasks.
- `agents/` defines specialized review behavior and guardrails.
- Human approval remains required where architecture, requirements, risk, or production behavior depends on context.

### Reviewers

Use the standard-specific checklists and review prompts, then verify evidence. A review prompt is guidance; it is not proof that a service satisfies a control.

## Key Distinctions

- **Local adapter:** an explicitly selected development/CI implementation with documented reduced guarantees and a production startup guard.
- **Production degradation:** the approved behavior of a live service when a dependency fails, such as fail fast, fail closed, bounded retry, circuit breaking, durable queueing, serving stale data, or bypassing a non-critical capability.
- **Executable enforcement:** a rule is described as enforced only when an automated check can block a violation. See the [Enforcement Matrix](enforcement-matrix.md).
- **Human judgment:** context-sensitive decisions remain reviewed rather than being presented as universally enforceable defaults.

## References

- [Engineering Principles](../standards/engineering-principles.md)
- [Architecture](../standards/architecture.md)
- [Local Adapter Strategy](../standards/local-adapter-strategy.md)
- [Production Dependency Failure and Degradation](../standards/fallback-strategy.md)
- [Enforcement Matrix](enforcement-matrix.md)
- [Glossary](glossary.md)
