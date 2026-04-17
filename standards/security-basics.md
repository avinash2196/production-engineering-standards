# Security Basics

Purpose
- Provide minimal, enforceable security rules for all services.

Mandatory Rules
- No hardcoded credentials in code or config repositories.
- All network traffic must use TLS in production; certificate management documented.
- Principle of least privilege for service identities and secrets access.

Defaults
- Use cloud secret managers (Vault, AWS Secrets Manager, Azure Key Vault). Local development uses environment-variable fallback with explicit toggles.

Anti-patterns
- Committing secrets, using wildcard IAM permissions, or disabling TLS for convenience.

LLM instructions
- When wiring secret access, generate code that uses `SecretProvider` abstraction and a clear env-controlled fallback.
- Ask the user if they require hardware-backed keys or FIPS requirements.

Review checklist
- [ ] No secrets in source.
- [ ] TLS enforced in production configs.
- [ ] Least-privilege IAM/role policies documented.
