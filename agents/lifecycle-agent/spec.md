# Lifecycle Agent

Agent spec for lifecycle tasks: dependency updates, observability checks, and maintenance reminders.

## Purpose

Automate recurring maintenance tasks that keep services healthy, secure, and aligned with current standards — reducing the burden of manual housekeeping on development teams.

## Capabilities

| Capability | Description | Frequency |
|-----------|-------------|----------|
| Dependency scanning | Check for outdated and vulnerable dependencies | Weekly |
| Observability audit | Verify metrics, tracing, logging, and health checks are present | Per release |
| Deprecation scanning | Identify usage of deprecated APIs, libraries, or patterns | Monthly |
| Standards drift detection | Compare service against latest repo standards version | Monthly |
| License compliance | Flag dependencies with non-approved licenses | Weekly |

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Repository URL or path | Yes | Service repository to scan |
| Stack type | Yes | `java-springboot` or `python-fastapi` |
| Standards version | Optional | Git SHA of standards to check against (default: latest) |
| Severity threshold | Optional | Minimum CVE severity to report (default: MEDIUM) |

## Outputs

```markdown
## Lifecycle Report: {service-name}

### Dependency Updates
| Dependency | Current | Latest | CVEs | Priority |
|-----------|---------|--------|------|----------|
| spring-boot | 3.2.1 | 3.2.5 | CVE-2024-xxxx (HIGH) | URGENT |

### Observability Gaps
| Check | Status | Detail |
|-------|--------|--------|
| Structured logging | ✅ PASS | JSON format configured |
| Metrics endpoint | ❌ FAIL | /actuator/prometheus not exposed |
| Health checks | ✅ PASS | Liveness + readiness configured |
| Distributed tracing | ❌ FAIL | No tracing dependency found |

### Deprecation Warnings
| Item | Type | Replacement | Deadline |
|------|------|-------------|----------|
| `javax.persistence` | Package | `jakarta.persistence` | Java 21 migration |

### Standards Drift
| Standard | Expected | Actual | Remediation |
|----------|----------|--------|-------------|
| Error response format | Standard envelope | Custom format | Adopt dto-guidelines.md error envelope |
```

## Guardrails

- Never auto-merge dependency updates — create PRs for human review.
- Flag CRITICAL CVEs immediately via configured alerting channel.
- Do not modify source code; only produce reports and PRs.
- Respect `.lifecycle-ignore` file for intentional exceptions.

## Tool Access

- File system read (scan `pom.xml`, `requirements.txt`, source code).
- Package registry APIs (Maven Central, PyPI) for version checks.
- CVE databases (NVD, GitHub Advisory Database).
- Standards repository read (this repo).
- Git operations (create branches, open PRs) — with human approval.

## Invocation

```bash
# Manual
@lifecycle-agent scan --repo=./order-service --stack=java-springboot

# Scheduled (GitHub Actions)
on:
  schedule:
    - cron: '0 6 * * 1'  # Every Monday at 6am
jobs:
  lifecycle:
    steps:
      - uses: lifecycle-agent
        with:
          stack: java-springboot
          severity-threshold: MEDIUM
```

## References

- [Observability standard](../../standards/observability.md)
- [Security standards](../../standards/security/security-standards.md)
- [Coding standards](../../standards/coding-standards.md)
