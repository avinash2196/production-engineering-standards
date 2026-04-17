# Correlation IDs

> Parent overview: [standards/observability.md](../observability.md)

Purpose
- Enable request-level tracing and log correlation across all services in a distributed call chain by propagating a single correlation identifier.

Mandatory Rules
- Every inbound HTTP request must carry or generate a correlation ID via the `X-Correlation-ID` header.
- If the header is absent, the edge service (API gateway or first-receiving controller) must generate a UUID v4 and attach it.
- The correlation ID must be propagated to all downstream HTTP calls, message publishes, and async job dispatches.
- The correlation ID must appear in every structured log line and as a span attribute in distributed traces.
- Never reuse or overwrite an existing correlation ID received from an upstream caller.

Defaults
- Java: Use a servlet filter or Spring `HandlerInterceptor` to extract/generate the ID and store in MDC (`MDC.put("correlationId", id)`). Add to outbound `RestTemplate`/`WebClient` interceptors.
- Python: Use FastAPI middleware to extract/generate the ID and store in `contextvars`. Add to outbound `httpx`/`aiohttp` request headers.

Anti-patterns
- Generating a new correlation ID at every service boundary (breaks end-to-end correlation).
- Storing correlation ID only in thread-local without propagating across async/reactive boundaries.
- Omitting correlation ID from message headers (breaks correlation across async flows).

LLM instructions
- When scaffolding a new service, include correlation ID middleware that extracts from `X-Correlation-ID` header, generates if missing, stores in request context, and propagates to outbound calls.
- When adding message publish/subscribe, include correlation ID in message headers.

Review checklist
- [ ] Correlation ID extracted or generated at service edge.
- [ ] ID propagated to all downstream HTTP and messaging calls.
- [ ] ID present in all structured log lines.
- [ ] ID preserved (not regenerated) across service boundaries.
