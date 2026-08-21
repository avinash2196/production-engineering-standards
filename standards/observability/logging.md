# Logging

> Parent overview: [Observability](../observability.md)

## Purpose

Provide operationally useful, machine-searchable logs without forcing one serialization format, logging library, or correlation mechanism into every service.

## Required Outcomes

Production logging must:

- use the runtime/platform's supported logging mechanism rather than ad-hoc console printing for operational events;
- provide stable, searchable context for important events;
- use levels consistently;
- avoid secrets, credentials, tokens, and unnecessary sensitive payloads;
- include safe correlation/operation context when that context materially improves diagnosis;
- distinguish application diagnostics from formal audit logging when the project requires an audit trail.

Structured logging is preferred when the target platform benefits from it, but JSON and a fixed field schema are not universal requirements.

## Context

Useful context may include service/component, operation, request/trace/job/message identifiers, dependency, outcome, and error category. Include only fields that are safe, bounded, and useful.

Do not require a custom `X-Correlation-ID` when W3C trace context, a platform request ID, message ID, or another approved mechanism already provides correlation.

## Audit Logging

Security/compliance audit events are required only when the project's threat model, data classification, compliance framework, or policy establishes them. Use the dedicated [Audit Logging](../compliance/audit-logging.md) standard when applicable.

## Anti-Patterns

- `print()`/`System.out.println()` as production operational logging.
- Logging full request/response bodies without data-classification review.
- Logging secrets or high-risk personal data for convenience.
- Requiring the same fields in every event even when they have no meaning.
- Treating normal application logs as sufficient evidence for an audit control without checking the applicable policy.

## LLM Instructions

- Select logging structure and context from the service's runtime, platform, failure modes, and support needs.
- Reuse an established trace/request/job/message identifier when one exists.
- Never invent audit obligations or sensitive fields.

## Review Checklist

- [ ] Important operational events are searchable and diagnosable.
- [ ] Levels/context are used consistently.
- [ ] Sensitive values are excluded or protected.
- [ ] Correlation uses the project's established mechanism where needed.
- [ ] Audit requirements are handled separately when applicable.
