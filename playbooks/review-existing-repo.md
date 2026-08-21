# Workflow: Review Existing Repository

## Purpose

Assess an existing repository against the Production Engineering Standards and produce an evidence-based remediation roadmap without forcing optional mechanisms or architecture patterns onto the codebase.

## Prerequisites

- Access to the repository and relevant build/deployment configuration.
- Enough context to understand the service's purpose, target environment, and important dependencies.
- Explicit project requirements/policies when a finding depends on security, compliance, availability, or data-handling decisions.

## Steps

### 1. Establish Context

Identify from repository evidence:

- stack/runtime and entry points;
- module/package boundaries;
- external dependencies and data stores;
- deployment/CI artifacts;
- current tests/checks;
- known requirements, SLOs, data classifications, and policies.

Record unknowns that materially affect the review instead of filling them with generic defaults.

### 2. Architecture Review

Use the [Architecture Reviewer custom agent](../.github/agents/architecture-reviewer.agent.md) or `/review-architecture` when useful.

Assess:

- whether responsibilities and dependency directions are understandable;
- whether abstractions protect real testing/portability/policy boundaries;
- data ownership and transaction boundaries;
- API/event contracts and coupling;
- unnecessary complexity as well as missing boundaries.

Do not require a fixed controller → service → domain → repository layering model for every service.

### 3. Dependency, Local-Development, and Failure Behavior

For each material external dependency, record what actually applies:

| Dependency | Boundary justified/used? | Local-development strategy needed? | Production failure behavior | Evidence / Gap |
|---|---|---|---|---|
| `<dependency>` | Yes / No / N/A | Yes / No / N/A | `<behavior>` | `<path/decision>` |

A service does not need a local adapter for every dependency, and a shared capability contract should not be introduced without a real boundary.

References: [Fallback Strategy](../standards/fallback-strategy.md), [Local Adapter Strategy](../standards/local-adapter-strategy.md), [Contracts](../contracts/).

### 4. Configuration and Secrets

- Does configuration use the target framework/platform's intended mechanism?
- If multiple sources exist, is their actual precedence understood and tested where important?
- Are required values validated safely?
- Are production secrets obtained through the approved secure mechanism?
- If local-only adapters/selectors exist, can they be rejected or prevented in production as designed?

Do not require `ConfigProvider`, dynamic configuration, `SecretProvider`, or a historical provider chain unless the project has adopted those boundaries.

Reference: [Configuration Management](../standards/configuration-management.md), [Secrets Handling](../standards/security/secrets-handling.md).

### 5. Observability and Operations

Assess whether operators can diagnose and support the service's critical paths using the approved operating model:

- logs/events useful for failure diagnosis;
- correlation/context propagation where flows cross boundaries;
- metrics/health evidence needed by the runtime and SLOs;
- tracing where it provides material value;
- alerts/runbooks/recovery evidence where required.

Do not require JSON logs, `X-Correlation-ID`, all four golden signals, OpenTelemetry, or a particular health endpoint shape by convention.

Reference: [Observability](../standards/observability.md).

### 6. Security and Compliance

Review trust boundaries, input handling, protected resources, authorization decisions, least privilege, secret handling, sensitive-data leakage, and dependency/supply-chain controls that apply.

Apply compliance-specific controls only after applicability/classification is established. Use the [Compliance Reviewer](../.github/agents/compliance-reviewer.agent.md) or [HIPAA Reviewer](../.github/agents/hipaa-reviewer.agent.md) only for the appropriate scope.

Reference: [Security Engineering Standard](../standards/security/security-standards.md).

### 7. Testing

Assess whether tests/checks provide evidence for the behavior and failure modes that matter:

- deterministic unit tests for business/application decisions;
- integration tests at boundaries where integration risk exists;
- contract/schema compatibility tests where independently evolving components need them;
- production safeguards/startup checks where required;
- regression evidence for known failure modes.

Do not require mocks, Testcontainers, Pact, or staging E2E for every project.

### 8. Distributed-System Behavior

For services with remote/distributed interactions, use the [Distributed Systems Reviewer](../.github/agents/distributed-systems-reviewer.agent.md) or `/review-distributed-systems`.

Assess applicable timeouts, retry safety, idempotency/deduplication, ordering, concurrency, consistency, recovery, and dependency-failure behavior. Do not manufacture mechanisms for interactions that do not need them.

### 9. Produce a Prioritized Roadmap

Use evidence and risk rather than generic checklist severity:

```markdown
## Remediation Roadmap: <repo-name>

### Production blockers
1. [CRITICAL] <concrete violated requirement/control> — <evidence> — <remediation>

### High priority
2. [HIGH] <material reliability/security/correctness gap> — <evidence> — <remediation>

### Planned improvements
3. [MEDIUM] <justified improvement> — <evidence> — <remediation>

### Backlog / optional
4. [LOW] <non-urgent improvement> — <evidence> — <remediation>

### Needs verification
- <missing decision/evidence that prevents a conclusion>
```

## Completion Criteria

- [ ] Context and applicability were established before judging mechanisms.
- [ ] Findings cite repository/requirement/policy evidence.
- [ ] Optional patterns were not treated as mandatory standards.
- [ ] Severity reflects concrete risk and impact.
- [ ] Remediation is scoped and does not silently expand architecture.
- [ ] Unresolved material decisions are explicitly marked `NEEDS VERIFICATION`.
