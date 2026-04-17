# Data Classification

## Purpose

Define data classification levels and the handling rules required for each level. Every data element stored, processed, or transmitted by a service must be classified. The classification determines which security, encryption, logging, and access controls are required.

## Classification Levels

| Level | Label | Description | Examples |
|-------|-------|-------------|----------|
| 1 | **Public** | Data intended for public consumption. No confidentiality requirement. | Marketing content, public API documentation, product catalog (non-priced) |
| 2 | **Internal** | Not for external exposure, but no special protection required. | Internal wiki, non-sensitive metrics, team meeting notes |
| 3 | **Confidential** | Business-sensitive data requiring access control and encryption. | Customer emails, financial records, pricing data, internal API keys |
| 4 | **Restricted / PHI** | Highest sensitivity. Regulatory requirements apply (HIPAA, PCI, GDPR). | Patient health records, SSN, payment card numbers, biometric data |

## Handling Rules Per Level

### Public (Level 1)

| Control | Requirement |
|---------|-------------|
| Encryption at rest | Not required |
| Encryption in transit | HTTPS recommended, not mandatory for non-auth endpoints |
| Access control | None (publicly accessible) |
| Audit logging | Not required |
| Data minimization | Not applicable |
| Retention | No specific policy required |
| Backup encryption | Not required |

### Internal (Level 2)

| Control | Requirement |
|---------|-------------|
| Encryption at rest | Server-side encryption (default DB/storage encryption) |
| Encryption in transit | TLS 1.2+ required |
| Access control | Authentication required; no fine-grained authorization needed |
| Audit logging | Not required for reads; log writes at application level |
| Data minimization | Avoid unnecessary exposure in API responses |
| Retention | Follow business retention policy |
| Backup encryption | Server-side encryption |

### Confidential (Level 3)

| Control | Requirement |
|---------|-------------|
| Encryption at rest | Server-side encryption (TDE for databases) |
| Encryption in transit | TLS 1.2+ required |
| Access control | Authentication + authorization (RBAC) required |
| Audit logging | Log all write operations; log reads of sensitive fields |
| Data minimization | Projection DTOs; no `SELECT *` on confidential tables |
| Retention | Defined retention policy with automated disposal |
| Backup encryption | Server-side encryption with access-controlled keys |
| Log handling | Redact confidential values in application logs |

### Restricted / PHI (Level 4)

| Control | Requirement |
|---------|-------------|
| Encryption at rest | Field-level encryption (application-layer AES-256) + TDE |
| Encryption in transit | TLS 1.2+ required; mTLS for service-to-service |
| Access control | Authentication + fine-grained authorization (RBAC or ABAC) |
| Audit logging | Full CRUD audit trail; retain ≥ 6 years; tamper-resistant |
| Data minimization | Strict minimum necessary; projection DTOs; no PHI in URLs |
| Retention | Regulatory retention policy (6-10 years typical); crypto-shredding on disposal |
| Backup encryption | Encrypted with key managed via `SecretProvider` |
| Log handling | No raw Restricted/PHI values in any log, error message, or metric |
| Additional | PHI inventory required; see `hipaa-controls.md` |

## Classification Process

### For New Services

1. During service design, list every data element the service will handle.
2. Classify each element using the table above.
3. Record the classification in the service's data inventory table.
4. Apply the handling rules for the highest classification level present.

### For Existing Services

1. Run the **compliance-reviewer** agent or execute the `review-compliance-controls` workflow.
2. The reviewer will identify data elements and assign proposed classifications.
3. The service owner validates and adjusts classifications.

## Data Inventory Template

| Data Element | Field/Column | Classification | Justification |
|-------------|-------------|---------------|---------------|
| Patient name | `patients.name` | Restricted/PHI | HIPAA — individually identifiable health info |
| Order total | `orders.total` | Confidential | Business-sensitive pricing data |
| Product name | `products.name` | Public | Displayed on public catalog |
| Employee email | `users.email` | Internal | Internal directory, not public |

## Cross-Cutting Rules

- **Default to higher classification when uncertain.** If a data element could be Internal or Confidential, treat it as Confidential until confirmed otherwise.
- **Mixed-classification tables:** if a database table contains both Internal and Restricted columns, the entire table must be treated at the Restricted level for access control. Use field-level encryption for individual Restricted columns.
- **Derived data:** aggregations or analytics derived from classified data inherit the classification of the source unless provably anonymized (k-anonymity ≥ 5 or differential privacy applied).
- **Temporary storage:** classification applies regardless of storage duration. A Restricted value in a temp file, cache, or queue must still be encrypted and access-controlled.

## LLM Instructions

- When generating a data model, ask the user to classify each field.
- If the user does not provide classification, infer based on the field name and err toward higher classification.
- Apply the handling rules for the highest classification level present in the service.
- Fields named `ssn`, `dob`, `diagnosis`, `patient*`, `health*` → default to Restricted/PHI.
- Fields named `password`, `secret`, `api_key`, `token` → these are secrets, not data classifications. Route to `SecretProvider`.

## Review Checklist

- [ ] Every data element in the service has an assigned classification.
- [ ] Handling rules match or exceed the requirements for the assigned level.
- [ ] Data inventory documented and maintained.
- [ ] No Restricted/PHI data at lower protection levels.
- [ ] Derived data classified based on source data.
