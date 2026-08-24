---
description: "Review a service against explicitly applicable compliance, security, data-classification, and data-handling controls without inventing regulatory applicability."
argument-hint: "service/scope, known data classification or compliance policy, and relevant code/design/config"
agent: "compliance-reviewer"
---

Perform an engineering compliance review of the provided scope.

## Applicability Gate

Before evaluating controls, establish what actually applies from explicit requirements, approved policy, data classification, architecture decisions, or repository evidence.

- Do **not** infer HIPAA, PCI, GDPR, PHI, or another framework solely from domain/field names.
- If applicability or classification materially blocks a conclusion, mark it `NEEDS VERIFICATION` and ask only the smallest necessary question.
- Use HIPAA-specific guidance only when HIPAA/ePHI applicability is established.

## References

Load only relevant standards:

- [Compliance engineering](../../standards/compliance-engineering.md)
- [Data classification](../../standards/compliance/data-classification.md)
- [Audit logging](../../standards/compliance/audit-logging.md)
- [HIPAA controls](../../standards/compliance/hipaa-controls.md) — only when applicable
- [Security standard](../../standards/security/security-standards.md)
- [Transport protection](../../standards/security/transport-encryption.md)
- [Secrets handling](../../standards/security/secrets-handling.md)

## Review Rules

1. Evaluate every **applicable** control and cite concrete evidence.
2. Use statuses `PASS`, `FAIL`, `NOT APPLICABLE`, or `NEEDS VERIFICATION`.
3. Rate findings `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW` based on concrete impact/exposure/likelihood.
4. Do not require a particular mechanism (`SecretProvider`, Vault, mTLS, RBAC, field encryption, immutable storage, specific TLS version, fixed retention) unless approved requirements/policy select it.
5. Never claim legal or regulatory certification.
6. A production-blocking conclusion requires a concrete violated requirement/control or an explicitly required decision that is unresolved—not merely an absent optional pattern.

## Report

```markdown
## Compliance Engineering Review: <scope>

### Applicability
| Policy / Classification | Status | Evidence / Missing Decision |
|---|---|---|

### Findings
| # | Severity | Control Area | Status | Evidence | Finding | Remediation |
|---|---|---|---|---|---|---|

### Control Summary
| Area | Status | Notes |
|---|---|---|
| Data classification/minimization | ... | ... |
| Authentication/authorization | ... | ... |
| Data protection | ... | ... |
| Auditability | ... | ... |
| Secret handling | ... | ... |
| Retention/disposal | ... | ... |

### Open Decisions
- <only materially blocking decisions>
```

For a richer specialist persona, select the [Compliance Reviewer custom agent](../agents/compliance-reviewer.agent.md).
