# Overview

This repository documents architecture, standards, stacks, agents, templates, and examples for building enterprise backends.

## What This Repository Is

A **shared standards repository** that serves as the single source of truth for how enterprise backend services are designed, built, tested, deployed, and maintained. It is consumed by:

- **Developers** — as a reference for coding standards, architecture patterns, and integration guides.
- **LLM agents** — as grounding context for code generation, reviews, and scaffolding.
- **Reviewers** — as checklists for architecture reviews, compliance audits, and PR reviews.
- **Platform teams** — as templates for CI/CD pipelines, infrastructure, and observability.

## Repository Structure

```
enterprise-ai-engineering/
├── core/                    # Foundational architecture and abstractions
│   ├── architecture.md      # Layered architecture rules
│   ├── principles.md        # Non-negotiable engineering principles
│   ├── abstractions/        # Capability interfaces (MessagePublisher, CacheProvider, etc.)
│   ├── config/              # Configuration model and providers
│   └── fallbacks/           # Fallback implementations for local dev
├── standards/               # Cross-cutting standards
│   ├── coding-standards.md  # Naming, structure, style
│   ├── dto-guidelines.md    # Request/response DTOs
│   ├── observability.md     # Metrics, tracing, logging
│   ├── fallback-strategy.md # Fallback design philosophy
│   ├── security/            # Security, encryption, secrets
│   ├── compliance/          # HIPAA, data classification, audit logging
│   ├── testing/             # Unit, integration, contract testing
│   └── performance/         # Performance checklist and guidance
├── stacks/                  # Stack-specific implementation guides
│   ├── java-springboot/     # Java 21 + Spring Boot 3.x
│   └── python-fastapi/      # Python 3.12+ + FastAPI
├── agents/                  # LLM agent specifications and prompts
│   ├── scaffolding-agent/   # Generate new services from templates
│   ├── compliance-review-agent/  # Audit against compliance checklists
│   └── lifecycle-agent/     # Dependency updates, maintenance
├── workflows/               # Operational procedures
│   ├── local-dev/           # Run locally with/without infra
│   ├── compliance-review/   # Compliance audit procedure
│   └── release/             # Release and deployment process
├── templates/               # Reusable document templates
│   └── docs/               # ADR, design doc templates
├── examples/                # Working example services
│   ├── java-microservice/   # Minimal Java example
│   ├── python-microservice/ # Minimal Python example
│   └── fallback-demo/       # Demonstrates fallback toggling
└── docs/                    # Meta-documentation
    ├── overview.md          # This file
    └── glossary.md          # Key terms
```

## How to Use This Repository

### For Developers

1. Read [core/principles.md](../core/principles.md) to understand the foundational values.
2. Read [core/architecture.md](../core/architecture.md) for the layered architecture rules.
3. Use your stack guide ([Java](../stacks/java-springboot/README.md) | [Python](../stacks/python-fastapi/README.md)) for implementation details.
4. Follow [workflows/local-dev/](../workflows/local-dev/) to set up your development environment.

### For LLM Agents

1. Include the relevant standards files in the agent's context window.
2. Use the agent specs under `agents/` for structured task execution.
3. Reference this repo at a pinned git SHA for reproducible results.

### For Reviewers

1. Use the review checklists embedded in each standard.
2. Run the compliance-review-agent for automated audits.
3. Follow [workflows/compliance-review/procedure.md](../workflows/compliance-review/procedure.md) for full reviews.

## Key Concepts

- **Capability Interfaces:** Abstract infrastructure behind interfaces so services are testable and portable.
- **Fallback Implementations:** Run services locally without any infrastructure dependencies.
- **Standards as Code:** Standards are versioned, reviewable, and machine-readable.
- **Agent-Driven Automation:** LLM agents consume standards to automate scaffolding, reviews, and maintenance.

See [glossary.md](glossary.md) for full term definitions.

## References

- [Core principles](../core/principles.md)
- [Core architecture](../core/architecture.md)
- [Glossary](glossary.md)
