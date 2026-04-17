# Agent Specs

This directory contains specifications for Copilot-style coding agents. Each agent has a defined identity, scope, inputs, behavior rules, output format, and review checklist.

## Agent Registry

| Agent | Purpose | File |
|-------|---------|------|
| **Backend Service Builder** | Scaffold production-grade services with layered architecture, abstractions, and fallbacks | [backend-service-builder.md](backend-service-builder.md) |
| **Code Reviewer** | Review code changes against all enterprise standards | [code-reviewer.md](code-reviewer.md) |
| **Test Engineer** | Generate unit, integration, and contract tests | [test-engineer.md](test-engineer.md) |
| **Refactoring Engineer** | Restructure code to align with standards without behavior changes | [refactoring-engineer.md](refactoring-engineer.md) |
| **Codebase Analyst** | Assess entire repositories with prioritized remediation report | [codebase-analyst.md](codebase-analyst.md) |
| **Production Readiness Reviewer** | Evaluate deployment readiness across config, observability, resilience, security | [production-readiness-reviewer.md](production-readiness-reviewer.md) |
| **Architecture Reviewer** | Review layered design, domain model, API design, coupling | [architecture-reviewer.md](architecture-reviewer.md) |
| **Distributed Systems Reviewer** | Verify idempotency, retries, timeouts, consistency models, failure modes | [distributed-systems-reviewer.md](distributed-systems-reviewer.md) |
| **Compliance Reviewer** | Audit data protection, encryption, audit logging, access control | [compliance-reviewer.md](compliance-reviewer.md) |
| **HIPAA Reviewer** | HIPAA-specific engineering controls audit for PHI-handling services | [hipaa-reviewer.md](hipaa-reviewer.md) |

## Agent Interaction Model

- Agents are standalone — each can be invoked independently.
- Agents can be composed in workflows (e.g., `create-new-service` invokes `backend-service-builder` then `code-reviewer`).
- Agents share the same standards references and produce output in consistent formats.
- When an agent detects an issue outside its scope, it references the appropriate agent (e.g., code-reviewer references compliance-reviewer for HIPAA findings).
