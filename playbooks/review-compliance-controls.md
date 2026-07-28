# Workflow: Review Compliance Controls

## Purpose

Step-by-step procedure for auditing a service's engineering compliance controls, producing a findings report with remediation steps. Covers data protection, encryption, audit logging, access control, and HIPAA-specific controls when applicable.

## Prerequisites

- Service codebase accessible
- Data types handled by the service known (or will be identified in step 1)
- Compliance tier known (standard or HIPAA-aware)

## Steps

### 1. Data Inventory

Identify all data the service handles and classify each:

| Data Element | Classification | Storage Location | Transmitted To |
|-------------|---------------|-----------------|----------------|
| Patient name | Restricted/PHI | PostgreSQL `patients.name` | Downstream billing-service |
| Order total | Internal | PostgreSQL `orders.total` | — |
| API key | Secret | Vault | — |

**Classification levels:**
- **Public:** no restrictions
- **Internal:** not for external exposure, no special handling
- **Confidential:** requires encryption and access control
- **Restricted/PHI:** requires encryption, audit logging, access control, data minimization

Reference: `standards/compliance/data-classification.md`

### 2. Encryption Review

For each confidential/restricted data element:

| Check | Expected | Finding |
|-------|----------|---------|
| Encrypted at rest (DB column or storage) | AES-256 or equivalent | ✅/❌ |
| Encrypted in transit | TLS 1.2+ | ✅/❌ |
| Field-level encryption (if restricted/PHI) | App-layer encryption | ✅/❌ |
| Encryption key management | Via `SecretProvider` with rotation | ✅/❌ |
| Backups encrypted | Server-side encryption | ✅/❌ |

Reference: `standards/security/transport-encryption.md`, `standards/compliance/hipaa-controls.md`

### 3. Audit Logging Review

For each operation on confidential/restricted data:

| Check | Expected | Finding |
|-------|----------|---------|
| Create operations audit-logged | who, what, when, outcome | ✅/❌ |
| Read operations audit-logged | who, what, when, outcome | ✅/❌ |
| Update operations audit-logged | who, what, when, outcome, changes | ✅/❌ |
| Delete operations audit-logged | who, what, when, outcome | ✅/❌ |
| Audit logs tamper-resistant | Append-only or write-once storage | ✅/❌ |
| Audit logs do not contain raw PHI | Redacted or tokenized | ✅/❌ |
| Audit log retention | 6+ years for HIPAA | ✅/❌/N/A |

Reference: `standards/compliance/audit-logging.md`

### 4. Access Control Review

| Check | Expected | Finding |
|-------|----------|---------|
| Authentication on all data endpoints | OAuth2/JWT/mTLS | ✅/❌ |
| Authorization at service layer | RBAC or ABAC | ✅/❌ |
| Least privilege for service accounts | Minimal required permissions | ✅/❌ |
| No shared credentials | Unique identity per service/user | ✅/❌ |
| Emergency access procedure | Break-glass with full audit | ✅/❌ |

Reference: `standards/security/security-standards.md`

### 5. Data Minimization Review

| Check | Expected | Finding |
|-------|----------|---------|
| API responses return only needed fields | Projection DTOs | ✅/❌ |
| Logs do not contain PII/PHI | Redacted or masked | ✅/❌ |
| Error messages do not leak sensitive data | Generic error responses | ✅/❌ |
| Database queries avoid `SELECT *` on sensitive tables | Explicit column selection | ✅/❌ |
| Data retention policy documented and enforced | Automated disposal | ✅/❌ |

Reference: `standards/compliance-engineering.md`

### 6. Secret Management Review

| Check | Expected | Finding |
|-------|----------|---------|
| Secrets via `SecretProvider` in production | Vault/managed secret store | ✅/❌ |
| No secrets in source code | Confirmed via grep | ✅/❌ |
| No secrets in config files or Docker images | Confirmed | ✅/❌ |
| `SECRET_ADAPTER=env` disabled in production | Confirmed | ✅/❌ |
| Secret rotation strategy documented | Rotation schedule + process | ✅/❌ |

Reference: `standards/security/secrets-handling.md`

### 7. HIPAA-Specific Controls (if applicable)

Invoke **hipaa-reviewer** agent for full HIPAA control audit. Additional checks:

- [ ] PHI inventory complete with storage and transmission mapping
- [ ] Integrity controls (checksums/signatures on PHI)
- [ ] Breach detection support (anomaly alerting on PHI access)
- [ ] Data disposal is irreversible (crypto-shredding or secure deletion)
- [ ] No PHI in URL query parameters

Reference: `standards/compliance/hipaa-controls.md`

### 8. Produce Compliance Report

```markdown
## Compliance Review Report: <service-name>

### Data Classification Summary
- Restricted/PHI elements: N
- Confidential elements: N
- Internal elements: N

### Control Compliance
| Control Area | Status | Critical Gaps | Remediation |
|-------------|--------|---------------|-------------|
| Encryption at rest | ⚠️ Partial | SSN field unencrypted | Add field-level encryption |
| Encryption in transit | ✅ | — | — |
| Audit logging | ❌ | Read ops not logged | Add audit events |
| Access control | ✅ | — | — |
| Data minimization | ⚠️ Partial | Logs contain patient name | Add log redaction |
| Secret management | ✅ | — | — |

### Remediation Priority
1. [CRITICAL] Encrypt SSN field at application layer
2. [HIGH] Add audit logging for all PHI read operations
3. [MEDIUM] Implement log redaction for patient names

### Disclaimer
This review provides engineering control assessment. It does not constitute legal compliance certification.
```

## Completion Criteria

- [ ] Data inventory complete with classification
- [ ] All 6 control areas assessed (encryption, audit, access, minimization, secrets, HIPAA if applicable)
- [ ] Findings prioritized by severity
- [ ] Each finding includes specific remediation steps
- [ ] Report includes disclaimer about non-legal nature
