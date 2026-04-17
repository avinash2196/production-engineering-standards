# Compliance Engineering

Purpose
- Provide engineering controls and checklists that help teams design for privacy- and compliance-sensitive systems (HIPAA-aware), without giving legal certification.

Mandatory Rules
- Classify data by sensitivity and document handling rules for each class.
- Encrypt sensitive data at rest and in transit; ensure keys are rotated per policy.
- Implement immutable audit logging for security-relevant events and make access auditable.

Defaults
- Default retention windows set in config and reviewed by compliance owners.
- Redact PII/PHI from logs by default; provide opt-in mechanisms for debug traces controlled by environment and limited time windows.

Anti-patterns
- Storing PHI unencrypted or shipping PII in logs without consent and access controls.

LLM instructions
- Agents must ask targeted questions before proposing designs that store or transmit sensitive data (what data, expected retention, intended audience).
- Provide evidence items: data classification, stakeholders, regulatory constraints, and retention windows.

Review checklist
- [ ] Data classification documented.
- [ ] Encryption at rest and in transit configured.
- [ ] Audit logging implemented for access and modification of sensitive records.
