# HIPAA Controls (Engineering)

## Purpose

Engineering-level controls checklist for services handling Protected Health Information (PHI). These are technical implementation requirements derived from the HIPAA Security Rule (45 CFR §164.312). This is **not** legal compliance certification — it is a practical engineering reference.

## Applicability

Apply these controls to any service where the data inventory (see `data-classification.md`) identifies Restricted/PHI data elements. Services that never touch PHI do not need these controls.

## Control Categories

### 1. Access Control (§164.312(a))

| Control | Requirement | Implementation |
|---------|-------------|----------------|
| Unique user identification | Every user and service account has a unique identity | OAuth2 subject claims, service principal IDs |
| Emergency access procedure | Break-glass access with full audit trail | Admin override role with automatic audit event |
| Automatic logoff | Sessions expire after inactivity | Token TTL ≤ 15 minutes for PHI-accessing sessions |
| Encryption and decryption | PHI encrypted when accessed/stored | Application-layer encryption for PHI fields |

**Engineering checklist:**
- [ ] All endpoints serving PHI require authentication (no anonymous access).
- [ ] Authorization enforced at the service layer, not just the API gateway.
- [ ] Role-based or attribute-based access control restricts PHI access to authorized roles.
- [ ] Service-to-service calls use mTLS or signed tokens with scoped permissions.
- [ ] Session timeout configured (≤ 15 minutes for PHI-accessing sessions).

### 2. Audit Controls (§164.312(b))

| Control | Requirement | Implementation |
|---------|-------------|----------------|
| Audit logging | Record all PHI access and modifications | Structured audit events for create/read/update/delete |
| Audit log protection | Logs tamper-resistant | Append-only storage, write-once buckets |
| Audit log retention | Retain for minimum 6 years | Automated lifecycle policy |
| Audit log review | Regular review for anomalies | Automated alerting on unusual PHI access patterns |

**Engineering checklist:**
- [ ] Every PHI create, read, update, delete produces an audit event.
- [ ] Audit events include: who (user/service ID), what (data element), when (timestamp), where (source IP/service), outcome (success/failure).
- [ ] Audit events do NOT contain raw PHI values — use record IDs or tokenized references.
- [ ] Audit logs stored in append-only or write-once storage.
- [ ] Retention policy enforced (≥ 6 years).
- [ ] Automated alerts on bulk PHI access or access from unusual sources.

Reference: `standards/compliance/audit-logging.md`

### 3. Integrity Controls (§164.312(c))

| Control | Requirement | Implementation |
|---------|-------------|----------------|
| Data integrity | Protect PHI from improper alteration or destruction | Checksums, database constraints, change tracking |
| Authentication of data | Verify data has not been altered in transit | Message signing, TLS, HMAC |

**Engineering checklist:**
- [ ] Database constraints prevent invalid PHI mutations (NOT NULL, CHECK, foreign keys).
- [ ] Change tracking on PHI tables (audit columns: `updated_by`, `updated_at`, or change data capture).
- [ ] Message integrity for PHI in transit (HMAC or message signing for async messages containing PHI).
- [ ] Backup integrity verified (checksums on backup files).

### 4. Transmission Security (§164.312(e))

| Control | Requirement | Implementation |
|---------|-------------|----------------|
| Encryption in transit | PHI encrypted during transmission | TLS 1.2+ for all connections |
| Integrity controls | Prevent unauthorized modification in transit | TLS provides this; additionally, sign payloads for async |

**Engineering checklist:**
- [ ] All external APIs enforce TLS 1.2+ (reject plaintext connections).
- [ ] Internal service-to-service calls use TLS or mTLS.
- [ ] Database connections use TLS.
- [ ] Message broker connections use TLS.
- [ ] No PHI transmitted in URL query parameters (use request body or headers).

### 5. Encryption at Rest

| Control | Requirement | Implementation |
|---------|-------------|----------------|
| Database encryption | PHI encrypted in database | Transparent data encryption (TDE) at minimum; field-level for sensitive columns |
| File/object encryption | PHI files encrypted | Server-side encryption (SSE) + application-layer for high-sensitivity |
| Backup encryption | Backups encrypted | Server-side encryption with managed keys |
| Key management | Encryption keys securely managed | `SecretProvider` with key rotation |

**Engineering checklist:**
- [ ] Database has TDE or equivalent enabled.
- [ ] PHI columns use field-level encryption (application-layer AES-256).
- [ ] Object storage uses SSE for all PHI objects.
- [ ] Encryption keys managed via `SecretProvider` with documented rotation schedule.
- [ ] Key rotation does not require downtime (envelope encryption pattern).

### 6. Data Minimization & Disposal

| Control | Requirement | Implementation |
|---------|-------------|----------------|
| Minimum necessary | Collect and expose only required PHI | Projection DTOs, column-level access |
| Data disposal | Irreversible deletion when retention expires | Crypto-shredding or certified secure deletion |
| Log redaction | PHI excluded from logs and error messages | Structured logging with redaction filters |

**Engineering checklist:**
- [ ] API responses use projection DTOs that include only the PHI fields needed by the caller.
- [ ] `SELECT *` is never used on tables containing PHI.
- [ ] Logs never contain raw PHI (redaction filters on structured logging).
- [ ] Error messages and stack traces never expose PHI.
- [ ] Data retention policy implemented with automated disposal.
- [ ] Disposal method is irreversible (crypto-shredding preferred).

## PHI Inventory Template

Every service handling PHI must maintain a PHI inventory:

| PHI Element | Storage | Encrypted At Rest | Encrypted In Transit | Access Control | Audit Logged | Retention |
|------------|---------|-------------------|---------------------|----------------|-------------|-----------|
| Patient name | `patients.name` | Field-level AES-256 | TLS 1.2 | RBAC: clinician role | Yes | 7 years |
| SSN | `patients.ssn` | Field-level AES-256 | TLS 1.2 | RBAC: admin role | Yes | 7 years |
| Diagnosis code | `encounters.icd10` | TDE | TLS 1.2 | RBAC: clinician role | Yes | 10 years |

## LLM Instructions

- When generating code that handles PHI, apply all 6 control categories.
- Always generate field-level encryption for PHI database columns.
- Never generate code that logs PHI values.
- Always include audit events for PHI access.
- Ask the user for PHI data elements before generating the data model.
- Include the disclaimer: this is engineering guidance, not legal compliance certification.

## Review Checklist (Summary)

- [ ] PHI inventory complete and current.
- [ ] All 6 control categories assessed and implemented.
- [ ] No raw PHI in logs, error messages, or URL parameters.
- [ ] Encryption at rest and in transit for all PHI.
- [ ] Audit logging for all PHI CRUD operations.
- [ ] Data disposal plan documented and automated.

## Disclaimer

This document provides engineering control guidance derived from HIPAA Security Rule requirements. It does not constitute legal advice or compliance certification. Consult your compliance team and legal counsel for official HIPAA compliance assessment.
