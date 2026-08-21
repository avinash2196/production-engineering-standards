# Integration Testing

## Purpose

Verify real wiring and boundary behavior between components/adapters using the most realistic deterministic environment practical for the risk being tested.

## Required Outcomes

- Test the integration semantics that matter: serialization, queries, transactions, ordering, retries, timeouts, failure mapping, configuration, or adapter contracts as applicable.
- Keep setup reproducible and isolated enough for CI/repeatable local execution.
- Select infrastructure fidelity based on the risk: Testcontainers, official emulators, embedded implementations, approved local adapters, dedicated ephemeral environments, or another controlled test fixture.
- Do not claim a local adapter proves production-vendor behavior that it cannot reproduce.

## Decision Guidance

Use higher-fidelity infrastructure when vendor/protocol behavior is part of correctness. Use a fake/local adapter when the goal is application wiring or workflow behavior and the reduced guarantees are understood.

## Anti-Patterns

- Shared unstable integration environments as the only CI signal.
- Calling a test "integration" while mocking every boundary that matters.
- Assuming a local filesystem/in-memory queue proves cloud storage/broker durability semantics.
- Running expensive/flaky tests in every fast unit-test stage without a reason.

## LLM Instructions

- Choose the test environment from the boundary/failure behavior being validated, not from a universal Testcontainers rule.
- Include failure-path tests where integration failure behavior is part of the approved contract.

## Review Checklist

- [ ] The selected fixture has enough fidelity for the risk being tested.
- [ ] Setup is deterministic and reproducible.
- [ ] Important boundary/failure semantics are exercised.
- [ ] Reduced guarantees of emulators/local adapters are not overstated.
