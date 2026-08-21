# Contract Testing

## Purpose

Verify compatibility at important service/API/event boundaries without assuming every integration requires consumer-driven contracts or a specific tool such as Pact.

## When Contract Tests Are Useful

Consider contract testing when:

- independently deployed producer/provider and consumer teams need compatibility feedback before integration;
- an API/event schema has a compatibility policy that can be verified deterministically;
- integration environments are expensive or insufficient to catch shape/semantic compatibility regressions;
- multiple consumers evolve independently.

A small internal system with one jointly deployed caller/provider may be adequately covered by unit/integration tests instead. Third-party APIs may require schema/client tests, stubs, sandbox integration, or provider-specific conformance rather than consumer-driven contracts.

## Contract Model

Choose the model that matches ownership and protocol:

- consumer-driven interaction contracts;
- provider-owned OpenAPI/JSON Schema/Protobuf/AsyncAPI compatibility checks;
- event-schema registry compatibility;
- generated-client conformance;
- another explicitly adopted compatibility mechanism.

Pact/Pact Broker is one valid consumer-driven implementation, not a repository-wide requirement.

## Required Outcomes When Contract Testing Is Adopted

- The contract represents behavior/shape that matters to real consumers.
- Provider and consumer versions can be related to the contract evidence.
- Breaking changes fail the appropriate CI/release check.
- Additive/evolution-compatible changes are not blocked by brittle exact-value assertions.
- Provider states/fixtures are deterministic and do not silently depend on shared environments.
- Message/event contracts include compatibility semantics relevant to serialization, required fields, and versioning.

## CI and Release Integration

Place verification at the stage where it can prevent incompatible delivery. The exact broker, registry, webhook, `can-i-deploy` style gate, or CI workflow depends on the selected contract tool and release process.

## Anti-Patterns

- Mandating Pact when another adopted schema/compatibility mechanism already solves the problem.
- Provider-authored "consumer" expectations that do not represent real consumer needs.
- Exact matching on irrelevant values that makes compatible changes fail.
- Treating contract tests as substitutes for business-logic or integration testing.
- Declaring a change compatible without executing the selected compatibility check.

## LLM Instructions

- Determine the integration ownership, deployment independence, protocol, and existing schema/contract tooling before recommending a contract-test mechanism.
- If Pact is already adopted, follow the project's Pact conventions; otherwise do not introduce it automatically.
- Generate only compatibility assertions required by the approved external contract.

## Review Checklist

- [ ] Contract testing is justified for the boundary.
- [ ] The chosen contract source reflects actual provider/consumer ownership.
- [ ] CI/release integration blocks real incompatible changes.
- [ ] Assertions allow approved backward-compatible evolution.
- [ ] Contract tests complement rather than replace behavior/integration tests.
