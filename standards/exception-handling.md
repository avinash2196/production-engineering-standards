# Exception Handling

Purpose
- Define consistent error propagation, translation, and observability for failures.

Mandatory Rules
- Surface typed domain errors from services; controllers map them to HTTP/gRPC responses.
- Capture and log context for unexpected exceptions including correlation IDs and key request metadata.
- Do not swallow exceptions silently; always handle or escalate.

Defaults
- Use a central exception mapper in each stack to convert internal errors to transport-level responses.
- Include an `errorCode` and `traceId` in error payloads for correlation.

Anti-patterns
- Catch-all empty `except`/`catch` blocks that drop stack traces or context.
- Returning generic 500 without structured error payload.

LLM instructions
- When generating exception-handling scaffolding, create centralized mappers and include hooks for custom error enrichment.
- Ask the user only if an error case implies data exposure, retention changes, or compliance impact.

Review checklist
- [ ] Central exception mapper exists.
- [ ] Errors include `errorCode` and `traceId`.
- [ ] Logging captures context and stack traces for unexpected failures.
