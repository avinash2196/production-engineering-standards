# Integration Testing

Purpose
- Define integration tests that verify wiring between services and their infra adapters using local fallbacks or test containers.

Mandatory Rules
- Integration tests must validate adapter contracts (e.g., publish/subscribe semantics, storage put/get) and service boundaries.
- Tests should run in CI using either test containers or explicit local fallback adapters.

Defaults
- Use testcontainers for DB and broker integration where available; otherwise, use the documented fallback adapters.

Anti-patterns
- Running flaky, long-running integration tests in the unit-stage of CI or relying on external shared services that can be noisy.

LLM instructions
- When generating integration tests, include both happy and failure path tests, exercise retries, and assert on emitted metrics/logs where appropriate.
- Ask the user if integration tests can rely on containerized infra or if they require fully local-only fallbacks.

Review checklist
- [ ] Integration tests validate adapter contracts.
- [ ] Tests run in CI with deterministic setup (containers or explicit fallbacks).
- [ ] Failure paths and retry semantics exercised.
