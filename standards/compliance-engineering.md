# Compliance Engineering

## Purpose

Provide engineering guidance for systems with explicitly established privacy, data-protection, contractual, or regulatory controls. This repository does not provide legal advice or compliance certification.

## Applicability First

Before applying a framework-specific control:

- identify the data/processing scope;
- identify the approved classification and policy source;
- establish which regulatory/contractual framework actually applies;
- mark unresolved applicability as `NEEDS VERIFICATION` rather than inferring it from domain/field names.

## Core Engineering Outcomes

When required by the applicable policy:

- minimize collection/exposure of sensitive data;
- protect data at relevant storage/network boundaries;
- enforce approved identity/access controls and least privilege;
- create sufficient audit evidence for accountable actions;
- keep secrets and sensitive values out of ordinary diagnostics;
- define retention/disposal from an identified policy source;
- ensure required controls are testable/reviewable and operational failures are visible.

The exact mechanisms—immutable storage, mTLS, RBAC/ABAC, field encryption, a particular secret manager, key rotation period, or retention window—are policy/architecture decisions, not universal defaults.

## HIPAA

Use [HIPAA Controls](compliance/hipaa-controls.md) only when HIPAA/ePHI applicability is established. Healthcare terminology alone does not establish HIPAA scope.

## LLM Instructions

- Ask only targeted questions that materially affect the current compliance/security decision.
- Cite policy/requirement/repository evidence for controls and findings.
- Do not claim legal/regulatory certification.
- Do not invent retention periods, cryptographic parameters, authentication models, audit-storage products, or regulatory applicability.

## Review Checklist

- [ ] Applicability and data classification are established or marked `NEEDS VERIFICATION`.
- [ ] Required access/data-protection/audit/minimization controls have evidence.
- [ ] Retention/disposal has an identified policy source when applicable.
- [ ] Sensitive values are excluded from ordinary telemetry and error surfaces.
- [ ] Optional mechanisms are not treated as universal requirements.
