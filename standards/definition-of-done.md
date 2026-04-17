# Definition of Done

A checklist that must be satisfied before marking work complete for services built from these templates.

Functional
- Feature implemented and verified against acceptance criteria.
- Unit tests added for business logic; integration tests added for infra wiring.

Operational
- Health checks present and documented.
- Metrics (latency, error, throughput) instrumented and exported.
- Tracing enabled and spans verified for key flows.

Security & Compliance
- No secrets in code or config files; secrets sourced from `SecretProvider`.
- Audit logging implemented for sensitive operations; retention and access policy specified.

Reliability
- Retries, timeouts, and idempotency considered for external calls.
- Chaos/local-failure tests exercised or documented.

Documentation
- ADR created if design choices are non-trivial.
- README explains local dev with fallbacks and environment toggles.

CI/CD
- Linting and unit tests run in CI and pass.
- Template generation and repo validators updated if necessary.
