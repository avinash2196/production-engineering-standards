# HIPAA Controls (Engineering Guidance)

## Purpose

Engineering control guidance mapped to selected HIPAA Security Rule technical safeguards for services handling electronic Protected Health Information (ePHI). This document is not legal advice, a complete HIPAA control catalog, or compliance certification. Regulatory interpretation and organization-specific policy require qualified security/compliance/legal review.

## Applicability

Use this guidance when a project's data inventory identifies PHI/ePHI and the project is subject to HIPAA. Confirm applicable requirements, risk analysis, organizational policy, state law, contractual obligations, and any later regulatory changes before treating a control as mandatory for a specific system.

## Control Categories

### 1. Access Control (§164.312(a))

| Control | Engineering objective | Example implementation |
|---|---|---|
| Unique user identification | Attribute access to a unique user/service identity | OAuth/OIDC subject, service identity |
| Emergency access procedure | Provide approved emergency access with accountability | Break-glass role/process with audit trail |
| Automatic logoff | Terminate inactive sessions when reasonable and appropriate | Organization-approved inactivity timeout |
| Encryption/decryption | Protect ePHI according to risk analysis and approved safeguards | Platform/database/application encryption as appropriate |

**Engineering checklist:**
- [ ] PHI/ePHI endpoints require authenticated identities unless an approved exception exists.
- [ ] Authorization is enforced at the appropriate application/service boundary.
- [ ] Service-to-service access uses scoped identities and approved authentication mechanisms.
- [ ] Inactivity/session behavior follows the organization's security policy and risk assessment; the selected value and rationale are documented.
- [ ] Emergency access behavior is documented and auditable where applicable.

HIPAA's automatic-logoff specification describes termination after a **predetermined period of inactivity**; this repository does not impose a universal 15-minute value.

### 2. Audit Controls (§164.312(b))

| Control | Engineering objective | Example implementation |
|---|---|---|
| Audit logging | Record security-relevant activity involving ePHI | Structured access/modification audit events |
| Audit protection | Reduce unauthorized modification/deletion | Separate permissions, append-oriented/immutable storage where appropriate |
| Retention | Retain records according to applicable legal/regulatory/organizational policy | Storage lifecycle policy tied to approved retention schedule |
| Review/detection | Enable review of suspicious access and audit failures | SIEM/alerting and review procedures |

**Engineering checklist:**
- [ ] Required ePHI access/modification activity is auditable according to project policy.
- [ ] Audit events identify actor, action/resource, time, outcome, and useful request context without storing unnecessary raw PHI.
- [ ] Audit storage and permissions protect integrity and availability.
- [ ] Retention is defined by the applicable policy and implemented in storage lifecycle configuration.
- [ ] Audit pipeline failures and suspicious access patterns have an operational response where required.

HIPAA includes a six-year retention rule for documentation required by the Security Rule. Do not infer from that rule that every application audit log or medical record has a universal six-year retention period.

Reference: [Audit Logging](audit-logging.md)

### 3. Integrity Controls (§164.312(c))

- Protect ePHI from improper alteration or destruction with controls appropriate to the risk and data flow.
- Use database constraints, authorization, versioning/change tracking, checksums/signatures, or other integrity mechanisms where they address a real threat.
- Verify backup/restore integrity for state that requires recovery.

### 4. Transmission Security (§164.312(e))

- Protect ePHI in transit using approved transport safeguards.
- Use TLS for network transport where it is the approved control; use stronger/additional measures when risk analysis or policy requires them.
- Do not place raw PHI in URLs, logs, or diagnostic metadata unless specifically designed and protected for that purpose.
- For asynchronous transport, select confidentiality/integrity controls from the broker/network architecture and approved security policy rather than assuming every message requires separate application-level encryption/signing.

### 5. Encryption at Rest and Key Management

HIPAA's encryption implementation specifications are addressable under the current Security Rule: organizations determine reasonable and appropriate safeguards through risk analysis and document decisions/alternatives. This repository therefore does not claim that application-layer field encryption is universally mandated for every PHI column.

**Engineering checklist:**
- [ ] Approved at-rest protection is defined for databases, object/file storage, and backups containing ePHI.
- [ ] Additional field/application-level encryption is used when required by the risk assessment, architecture, or organizational policy.
- [ ] Encryption keys are managed through approved key/secret management with access control, rotation/recovery procedures, and separation from protected data where appropriate.
- [ ] Encryption decisions and exceptions are documented.

### 6. Data Minimization, Retention, and Disposal

- Collect, expose, and log only the data needed for the approved purpose.
- Define retention from applicable law, regulation, contract, and organization policy; do not infer medical-record retention from this repository.
- Use an approved disposal mechanism when retention expires.
- Apply redaction/tokenization where operational logs and diagnostics could otherwise expose PHI.

## PHI/ePHI Inventory Template

Every service subject to the control set should maintain an inventory appropriate to its architecture:

| PHI/ePHI element | Storage/flow | Protection at rest | Protection in transit | Access control | Audit requirement | Retention source |
|---|---|---|---|---|---|---|
| [Element] | [Location/flow] | [Approved control] | [Approved control] | [Role/policy] | [Yes/No + rationale] | [Law/policy/contract] |

## LLM Instructions

- Do not claim that a service is "HIPAA compliant" based on this checklist.
- Do not invent session timeouts, audit-log retention periods, encryption algorithms/key sizes, or field-level encryption requirements when the project's approved policy/risk assessment does not specify them.
- Never generate ordinary application logs containing raw PHI.
- Identify missing compliance/security decisions explicitly and request qualified review where interpretation is required.
- Include the disclaimer that this is engineering guidance, not legal compliance certification.

## Review Checklist

- [ ] PHI/ePHI inventory is complete enough for the reviewed scope.
- [ ] Access, audit, integrity, transmission, at-rest protection, minimization, retention, and disposal controls were assessed.
- [ ] Numeric/security-policy choices come from approved policy/risk decisions rather than this repository.
- [ ] Raw PHI is excluded from ordinary logs, URLs, and diagnostics unless explicitly designed and protected.
- [ ] Unresolved regulatory/policy decisions are identified for qualified review.

## References

- HHS, HIPAA Security Rule: https://www.hhs.gov/hipaa/for-professionals/security/index.html
- HHS, encryption as an addressable implementation specification: https://www.hhs.gov/hipaa/for-professionals/faq/2001/is-the-use-of-encryption-mandatory-in-the-security-rule/index.html
- HHS, Security Rule documentation retention: https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html
- HHS, medical-record retention FAQ: https://www.hhs.gov/hipaa/for-professionals/faq/580/does-hipaa-require-covered-entities-to-keep-medical-records-for-any-period/index.html

## Disclaimer

This document provides engineering guidance and does not constitute legal advice or compliance certification. Consult the organization's security, privacy/compliance, and legal functions for applicability and interpretation.
