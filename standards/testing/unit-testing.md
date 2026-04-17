# Unit Testing

Purpose
- Define expectations for fast, isolated unit tests that exercise business logic without external infra.

Mandatory Rules
- Tests must run in-memory and not rely on networked services.
- Use mocks/stubs for `MessagePublisher`, `CacheProvider`, `ObjectStorageProvider`, `SecretProvider`, and `ConfigProvider`.
- Target high coverage for business logic; focus on behavior rather than implementation details.

Defaults
- Use stack-native test frameworks (`JUnit`/`Mockito` for Java, `pytest`/`pytest-mock` for Python).

Anti-patterns
- Integration-like tests that hit external services in unit test suites.

LLM instructions
- When generating tests, create mocks for capability abstractions and assert on interactions and returned values.
- Ask the user only if they want to include property-based tests or fuzzing for critical parsing logic.

Review checklist
- [ ] Unit tests run independently of network.
- [ ] Mocks used for external capabilities.
- [ ] Business logic behavior assertions present.
