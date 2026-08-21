# Unit Testing

## Purpose

Define fast, isolated tests for business/application logic without loading unnecessary infrastructure.

## Required Outcomes

- Unit tests are deterministic and do not depend on shared/networked production services.
- Test behavior and externally meaningful outcomes rather than private implementation detail.
- Replace only the external collaborators the unit actually uses with fakes/stubs/mocks as appropriate.
- Cover approved positive, negative, boundary, and error behavior without inventing requirements.

Do not create mocks for every repository capability contract when the code under test does not use those capabilities.

## Defaults

Use the stack-native test framework unless the project has selected another tool. Prefer simple fakes/stubs where they make tests clearer; use interaction mocks when the interaction itself is part of the behavior being verified.

## Anti-Patterns

- Network/shared-service dependence in a unit suite.
- Mocking internal implementation details until refactoring breaks otherwise valid tests.
- Asserting tests for behavior not established by requirements or current code contract.

## LLM Instructions

- During an approved RED milestone, add only tests/checks for approved behavior and prove the intended RED reason.
- Mock/fake only collaborators involved in the tested path.

## Review Checklist

- [ ] Tests run deterministically without shared infrastructure.
- [ ] Assertions focus on behavior.
- [ ] External collaborators are isolated only where needed.
- [ ] RED failures, when applicable, are caused by missing approved behavior.
