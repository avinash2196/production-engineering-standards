# Logging

> Parent overview: [standards/observability.md](../observability.md)

Purpose
- Provide structured, machine-parseable log output that supports correlation, audit, and diagnostics across distributed services.

Mandatory Rules
- All log output must be JSON-structured with fields: `timestamp`, `level`, `service`, `traceId`, `spanId`, `message`.
- Include `correlationId` (from `X-Correlation-ID` header) in every request-scoped log line.
- Log levels must follow: `ERROR` (actionable failures), `WARN` (degraded but operational), `INFO` (key business events), `DEBUG` (development only, never enabled in production by default).
- Never log secrets, tokens, passwords, or full PII. Redact or mask sensitive fields before writing.
- Audit-sensitive operations (data access, permission changes, authentication events) must be logged to an audit-specific channel or tagged with `audit: true`.

Defaults
- Java: SLF4J + Logback with JSON encoder. Inject MDC values for `traceId`, `spanId`, `correlationId`.
- Python: `structlog` or stdlib `logging` with `python-json-logger`. Attach context via contextvars or middleware.

Anti-patterns
- Unstructured `print()` or `System.out.println()` in production code.
- Logging request/response bodies that may contain PHI/PII without classification check.
- Using `DEBUG` level in production without dynamic level control.

LLM instructions
- When adding logging, always use structured logger (never raw print). Include correlationId from request context.
- For audit events, add `"audit": true` field and ensure the event includes who, what, when, and outcome.

Review checklist
- [ ] All logs are JSON-structured with required fields.
- [ ] Correlation ID present in request-scoped logs.
- [ ] No secrets or unredacted PII in log output.
- [ ] Audit events tagged and include who/what/when/outcome.
