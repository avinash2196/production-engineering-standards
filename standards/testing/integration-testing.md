# Integration Testing

Purpose
- Define integration tests that verify wiring between services and their infra adapters using Testcontainers/emulators or approved local adapters.

Mandatory Rules
- Integration tests must validate adapter contracts (e.g., publish/subscribe semantics, storage put/get) and service boundaries.
- Tests should run in CI using either test containers or explicit local adapters.

Defaults
- Use testcontainers for DB and broker integration where available; otherwise, use documented local adapters only when justified.

Anti-patterns
- Running flaky, long-running integration tests in the unit-stage of CI or relying on external shared services that can be noisy.

LLM instructions
- When generating integration tests, include both happy and failure path tests, exercise retries, and assert on emitted metrics/logs where appropriate.
- Ask the user if integration tests can rely on containerized infra or if they require fully local-only adapters.

Review checklist
- [ ] Integration tests validate adapter contracts.
- [ ] Tests run in CI with deterministic setup (containers/emulators or explicit local adapters).
- [ ] Failure paths and retry semantics exercised.
