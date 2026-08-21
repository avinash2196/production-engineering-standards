# Security Basics

## Purpose

Quick-reference security invariants for services. The canonical standard is [Security Engineering Standard](security/security-standards.md); when this summary and the canonical document differ, the canonical document wins.

## Mandatory Invariants

- Never commit credentials, tokens, private keys, or other secrets to source control.
- Validate data crossing untrusted boundaries according to the actual input and threat model.
- Apply authentication and authorization where the approved requirements define protected resources and permissions.
- Use least-privilege identities and permissions.
- Protect sensitive/authenticated traffic at the required trust boundary using the organization/platform-approved transport mechanism.
- Handle sensitive data according to the approved classification and prevent leakage through logs, traces, metrics, errors, URLs, and local fixtures.
- Obtain production secrets through the approved secure delivery/access mechanism.

## Mechanisms Are Contextual

This summary does **not** require a specific identity provider, JWT, mTLS, RBAC/ABAC, Vault product, `SecretProvider`, application-level TLS termination, or encryption algorithm. Select mechanisms from project requirements, architecture, platform standards, and security policy.

Local adapters such as `SECRET_ADAPTER=env` are examples for explicitly approved local-development workflows only; they are not production fallbacks.

## LLM Instructions

- Establish public/protected resources, data classification, trust boundaries, and target platform before choosing security mechanisms.
- Do not introduce `SecretProvider` solely because the shared contract exists.
- Do not infer HIPAA, PCI, or another compliance framework from field or domain names.
- Surface unresolved security decisions instead of inventing them.

## Review Checklist

- [ ] No secrets are committed or exposed in telemetry.
- [ ] Protected resources have the approved authentication/authorization controls.
- [ ] Service/workload permissions follow least privilege.
- [ ] Sensitive traffic/storage protection matches the approved architecture and data policy.
- [ ] Local-only security adapters cannot activate unintentionally in production.
