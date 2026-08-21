# Data Classification

## Purpose

Provide a reference classification model for projects that do not already have an organization-approved data-classification taxonomy. If the adopting organization/project has its own classification policy, **that policy takes precedence**.

Classification labels describe sensitivity and handling needs. They do not by themselves establish that HIPAA, PCI DSS, GDPR, or another legal/regulatory framework applies.

## Reference Levels

| Level | Label | Description | Illustrative examples |
|---|---|---|---|
| 1 | **Public** | Approved for public disclosure. | Public documentation, published catalog/content |
| 2 | **Internal** | Non-public operational/business information with limited sensitivity. | Internal process metadata, non-sensitive internal docs |
| 3 | **Confidential** | Sensitive information requiring controlled access and protection. | Customer contact data, non-public financial/business data |
| 4 | **Restricted** | Highest-sensitivity information under an approved policy/risk model. | Government identifiers, regulated payment/health data **when the applicable policy classifies it here**, highly sensitive credentials/material |

Secrets such as passwords, private keys, API tokens, and credentials are governed by secret-management policy and should not be treated merely as ordinary classified business data.

## Handling Model

The exact controls for each level come from the adopting organization's current security/data-handling policy. At a minimum, classification should drive decisions about:

- who/what may access the data;
- required protection at storage and network boundaries;
- logging/telemetry restrictions;
- auditability where required;
- retention and disposal;
- backup/replica/test-data handling;
- data minimization and exposure in APIs;
- incident/monitoring requirements where applicable.

This repository intentionally does **not** assign universal TLS versions, mTLS, RBAC/ABAC, encryption algorithms, retention periods, or audit-storage mechanisms to a label.

## Classification Process

### New Work

1. Identify the data/flow relevant to the approved scope.
2. Apply the organization's approved classification policy; if none exists, the reference levels above may be proposed for human/security review.
3. Record the classification and its source/rationale.
4. Apply controls from the relevant approved security/compliance policy.
5. Escalate unresolved classifications that materially affect the current design rather than inventing a lower-risk assumption.

### Existing Work

Use repository evidence to build an inventory, but treat inferred classifications as **proposals requiring confirmation** when policy evidence is absent.

## Data Inventory Template

| Data / Field / Flow | Proposed or Approved Classification | Policy / Rationale | Storage / Transit | Required Controls / Owner |
|---|---|---|---|---|
| `<item>` | `<label>` | `<policy/decision>` | `<locations>` | `<controls>` |

## Cross-Cutting Rules

- Apply classification to copies, caches, queues, exports, backups, and temporary storage as required by the approved policy—not only to the primary database.
- Derived data retains source sensitivity unless an approved de-identification/aggregation/reclassification process establishes otherwise.
- Mixed-sensitivity storage requires controls that prevent lower-classification access paths from exposing higher-sensitivity data; do not automatically classify an entire physical table at the highest level if approved column/row controls provide the required isolation.
- When classification is uncertain, mark it `NEEDS VERIFICATION`; use a temporary conservative handling decision only when explicitly justified for the current work.

## Regulatory Applicability

- Healthcare vocabulary does not prove HIPAA applicability.
- Payment-related fields do not automatically establish PCI DSS scope.
- Personal data does not by itself determine which privacy law/jurisdiction applies.

When a framework is explicitly applicable, load its specific engineering guidance (for example [HIPAA Controls](hipaa-controls.md)) and seek qualified compliance/legal interpretation where required.

## LLM Instructions

- Ask for or inspect the project's classification/policy source before applying fixed controls.
- Do not infer a regulatory regime solely from names such as `patient`, `card`, `ssn`, `email`, or `health`.
- Propose classifications only as reviewable suggestions when policy evidence is missing.
- Treat obvious credentials/tokens/keys as secret-handling concerns and route them to the approved secret mechanism; do not automatically require the optional `SecretProvider` abstraction.
- Never invent retention periods, encryption mechanisms, or access-control models from this reference classification alone.

## Review Checklist

- [ ] Relevant data/flows have an approved classification or are explicitly marked `NEEDS VERIFICATION`.
- [ ] Classification source/policy is identified.
- [ ] Controls are derived from that policy and the actual architecture.
- [ ] Copies/derived data/non-production use are considered.
- [ ] Regulatory applicability is established separately from classification labels.
