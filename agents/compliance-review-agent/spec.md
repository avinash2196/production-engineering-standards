# Compliance Review Agent

Spec for an agent that reviews architecture artifacts against the repository's HIPAA-aware checklist.

## Purpose

Make engineering compliance reviews repeatable by scanning service designs, configuration, and code against the production-grade security, data-classification, and HIPAA control standards defined in this repository.

## Capabilities

| Capability | Description |
|-----------|-------------|
| Architecture review | Evaluate service design docs against `standards/architecture.md` layer rules |
| Data classification check | Verify PHI/PII handling aligns with `standards/compliance/data-classification.md` |
| HIPAA control mapping | Map service controls to `standards/compliance/hipaa-controls.md` safeguards |
| Security standards audit | Check against `standards/security/security-standards.md` |
| Transport encryption check | Verify TLS configuration per `standards/security/transport-encryption.md` |
| Secrets handling review | Audit secret storage per `standards/security/secrets-handling.md` |

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Service name | Yes | Name of the service being reviewed |
| Design document | Yes | Architecture / design doc (markdown or link) |
| Source code path | Optional | Path to source for automated scanning |
| Data categories handled | Yes | List of data types (PHI, PII, public, internal) |
| Deployment target | Yes | Cloud provider and deployment model |

## Outputs

```markdown
## Compliance Review Report: {service-name}

### Summary
- Overall status: PASS / FAIL / NEEDS_REVIEW
- Standards version: {git-sha}
- Review date: {ISO-8601}

### Findings
| # | Category | Severity | Finding | Standard Reference | Remediation |
|---|----------|----------|---------|--------------------|-------------|
| 1 | Data Handling | HIGH | ePHI lacks the approved at-rest safeguard | hipaa-controls.md | Apply/document the control required by the approved risk/security decision |

### Checklist Results
- [ ] Authentication: approved identity mechanism verified
- [ ] Authorization: RBAC/ABAC at service layer
- [ ] Transport: organization-approved secure transport configuration verified
- [ ] Secrets: No hardcoded credentials
- [ ] Data classification: PHI/PII fields identified and protected
- [ ] Audit logging: Access to sensitive data logged
- [ ] Encryption at rest: Enabled for all data stores
```

## Guardrails

- Do not mark a service ready when required safeguards for ePHI at rest or in transit are missing; determine requirements from the applicable risk assessment/policy rather than inventing an encryption pattern.
- Flag any `SecretProvider` bypass (direct env var reads for secrets in non-local environments).
- Require explicit data classification for every data store.
- Identify HIGH/CRITICAL findings for the project's approved security/risk escalation process; do not invent a team/channel or remediation SLA.

## Tool Access

- File system read (to scan source code and config files).
- Standards repository read (this repo, pinned to a specific version).
- No write access — agent produces reports, humans apply fixes.

## Invocation

```bash
# Manual
@compliance-review-agent review --service=order-service --data-categories=PII,internal

# CI (GitHub Actions)
- uses: compliance-review-agent
  with:
    service: order-service
    design-doc: docs/design/order-service.md
    data-categories: PII,internal
```

## References

- [Compliance check prompt](prompts/compliance-check.prompt.md)
- [HIPAA controls](../../standards/compliance/hipaa-controls.md)
- [Data classification](../../standards/compliance/data-classification.md)
- [Security standards](../../standards/security/security-standards.md)
- [Workflow: compliance review procedure](../../playbooks/compliance-review/procedure.md)
