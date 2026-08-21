# Workflow: Review Compliance Controls

## Purpose

Review engineering controls for data protection and an explicitly applicable compliance/security policy. This workflow is not legal advice or certification and must not infer regulatory applicability from domain vocabulary.

## Prerequisites

- Relevant code/design/configuration evidence.
- Data inventory/classification or enough evidence to identify what still needs classification.
- The applicable organization/regulatory/contractual policy when controls depend on it.

## 1. Establish Applicability

Record the policy/classification basis before assessing controls:

| Item | Status | Evidence / Missing Decision |
|---|---|---|
| Data classification model | ESTABLISHED / NEEDS VERIFICATION | `<source>` |
| Regulatory/contractual framework | ESTABLISHED / N/A / NEEDS VERIFICATION | `<source>` |
| Organization security policy | ESTABLISHED / NEEDS VERIFICATION | `<source>` |

Do not infer HIPAA/PHI, PCI, GDPR, or another framework from field names alone.

## 2. Data Inventory and Minimization

For relevant data/flows:

| Data/flow | Classification | Storage/Transit | Consumers | Required controls | Evidence |
|---|---|---|---|---|---|
| `<item>` | `<approved classification>` | `<locations>` | `<callers>` | `<policy-derived>` | `<path/decision>` |

Check collection, exposure, logging, copying to non-production environments, retention, and disposal against the applicable policy.

## 3. Access Control

Where resources are protected, verify the approved identity and authorization model, enforcement boundary, least privilege, and privileged/emergency access behavior where applicable.

Do not require OAuth/JWT/mTLS, RBAC/ABAC, or a break-glass workflow unless the architecture/policy establishes them.

## 4. Data Protection

For applicable storage and network boundaries, verify the approved safeguards and evidence that they are enforced.

Do not invent encryption algorithms/key sizes, field-level encryption, TLS versions, mTLS, or backup controls. Use the current organization/platform security baseline and project risk decision.

References: [Security Engineering Standard](../standards/security/security-standards.md), [Transport Protection](../standards/security/transport-encryption.md).

## 5. Auditability

Where policy requires audit events, verify that the event model records enough attribution/context to support accountability without leaking raw sensitive values. Assess integrity/retention/monitoring controls according to the applicable policy and risk.

Append-only/immutable storage, synchronous writes, and a particular event schema are options—not universal requirements unless adopted.

Reference: [Audit Logging](../standards/compliance/audit-logging.md).

## 6. Secrets and Credentials

- no hardcoded/committed secrets;
- approved production secret delivery/access mechanism;
- least-privilege access;
- safe logging/telemetry;
- rotation/revocation behavior according to the selected backend/policy;
- local-only secret adapters cannot become implicit production fallbacks.

A `SecretProvider` abstraction or Vault product is optional unless the project explicitly adopts it.

Reference: [Secrets Handling](../standards/security/secrets-handling.md).

## 7. Framework-Specific Review

Only if applicability is established, load the relevant guidance. For HIPAA/ePHI, use the [HIPAA Reviewer custom agent](../.github/agents/hipaa-reviewer.agent.md) and [HIPAA Controls](../standards/compliance/hipaa-controls.md). Treat the result as engineering guidance requiring qualified compliance/security/legal interpretation where necessary.

## 8. Report

```markdown
## Compliance Engineering Review: <scope>

### Applicability
| Policy / Classification | Status | Evidence / Missing Decision |
|---|---|---|

### Findings
| # | Severity | Area | Status | Evidence | Finding | Remediation |
|---|---|---|---|---|---|---|

### Control Summary
| Area | Status | Notes |
|---|---|---|
| Data inventory/minimization | PASS / FAIL / N/A / NEEDS VERIFICATION | ... |
| Access control | ... | ... |
| Data protection | ... | ... |
| Auditability | ... | ... |
| Secrets/credentials | ... | ... |
| Retention/disposal | ... | ... |

### Disclaimer
Engineering control assessment only; not legal or regulatory certification.
```

## Completion Criteria

- [ ] Applicability was established before framework-specific controls were applied.
- [ ] Findings cite evidence and the relevant approved control/policy.
- [ ] No optional mechanism was presented as universally required.
- [ ] Missing material policy/classification decisions are marked `NEEDS VERIFICATION`.
- [ ] No raw secrets or unnecessary sensitive values appear in the review output.
