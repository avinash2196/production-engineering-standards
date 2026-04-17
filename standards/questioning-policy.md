# Questioning Policy for Agents

This policy defines when Copilot-style agents must ask clarifying questions vs applying repository defaults.

When to ask questions (agent MUST ask):
1. Architecture choices that affect security or compliance
- Example: choosing whether to persist PHI in a shared object store vs a segregated encrypted bucket.

2. Data handling or retention policies
- Example: retention period for audit logs or whether logs contain PII that must be redacted.

3. External integrations requiring credentials or cross-account access
- Example: integrating with a customer-managed Kafka cluster or VPC-peered database.

4. Any deviation from `core` non-negotiables
- If the requested design would remove retries, tracing, or other mandatory controls, ask for explicit approval.

When not to ask questions (agent SHOULD NOT ask):
1. Trivial implementation choices covered by `engineering-style.md`.
2. Non-sensitive, well-scoped defaults such as using `FALLBACK_KAFKA=true` for local development when explicitly requested.

Questioning behavior rules:
- Questions must be specific, limited in number (≤3 per session), and scoped to make a single decision.
- Agents must present the recommended default and the minimal options with clear risk statements.
- For any question that impacts compliance, agent must collect evidence: data sensitivity classification, stakeholders, and expected retention.

Prompt hygiene:
- Agents must not fabricate legal or security advice; they can state engineering implications and refer to `standards/compliance/hipaa-controls.md`.
