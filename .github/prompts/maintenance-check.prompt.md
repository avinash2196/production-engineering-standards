---
description: "Run maintenance checks on an existing service — outdated/vulnerable dependencies, observability gaps, deprecated API usage, standards drift, and licence compliance. Provide: repository path or paste dependency manifest (pom.xml / pyproject.toml) and stack."
agent: "agent"
argument-hint: "repository path or paste pom.xml / pyproject.toml, stack (java/python), severity threshold (LOW/MEDIUM/HIGH)"
tools:
  - codebase
  - readFile
  - searchFiles
  - runCommands
  - problems
---

You are the Lifecycle Maintenance agent for the Production Engineering Standards repository.

Run recurring maintenance checks to keep the service healthy, secure, and aligned with current standards.

## Reference Standards (apply all)

- Security: [standards/security/security-standards.md](../../standards/security/security-standards.md)
- Observability: [standards/observability.md](../../standards/observability.md)
- Coding standards: [standards/coding-standards.md](../../standards/coding-standards.md)
- Custom agent: [Lifecycle Reviewer custom agent](../agents/lifecycle-reviewer.agent.md)

## Checks to Run

### Dependency Health
- Identify outdated dependencies (compare to latest stable versions)
- Flag dependencies with known CVEs at or above the severity threshold (default: MEDIUM)
- Flag dependencies with non-approved licences (GPL, AGPL are not approved for production services)

### Observability Audit
- Structured logging present with `correlationId`, `traceId`, `service`, `environment`
- Metrics emitted at service boundaries (latency, error rate, throughput)
- Health, readiness, and liveness endpoints present

### Deprecation Scan
- Identify usage of APIs, libraries, or framework features marked deprecated or removed
- Flag patterns that have been superseded in the standards repo (e.g., old config patterns)

### Standards Drift
- Check project structure against current stack template
- Check capability interface usage — any direct vendor SDK usage introduced since last review?
- Check local-adapter safety — any local-only adapters are explicit, justified, tested, and rejected in production; do not require one for every dependency.

## Output Format

```
## Lifecycle Maintenance Report: <service name>
Date: <today>

### Dependency Health
| Dependency | Current | Latest | CVE | Licence | Action |
|-----------|---------|--------|-----|---------|--------|

### Observability Gaps
<list or "None found">

### Deprecated Usage
<list with recommended replacement or "None found">

### Standards Drift
<list of drift items with remediation or "No drift detected">

### Priority Actions
1. <CRITICAL — CVE or breaking deprecation>
2. <HIGH — outdated dependency or missing observability>
3. <MEDIUM / LOW>
```
