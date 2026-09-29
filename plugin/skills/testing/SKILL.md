---
name: testing
description: Use when designing unit, integration, contract, migration, concurrency, or failure-path tests.
---

# Testing

Test behavior and risk, not line count.

Choose the smallest useful test level:
- unit tests for deterministic domain behavior
- integration tests for framework/database/provider behavior
- contract tests for stable boundaries
- migration tests for schema/data compatibility
- concurrency tests for races or duplicate effects
- failure-path tests for retries, degradation, and recovery

A RED test must fail for the intended missing/wrong behavior—not because of unrelated setup failure.

A test that asserts only that something does not happen — no event, call, write, or message — passes vacuously while the behavior under test is absent. In the same test, first exercise the positive case that proves the behavior is active, then assert the negative.

A test that fails intermittently on unchanged code is a finding, not noise: reproduce it on the baseline, report it with that evidence, and keep its result visible. Do not rerun until it passes, and do not skip or weaken it to get a clean run.

Tests must verify behavior produced by the system or unit under test — a mocked dependency must not supply the exact value or behavior the assertion is meant to prove. When a unit computes or transforms data before calling a dependency, verify the argument, state change, or observable behavior the unit actually produced, not a value the mock was configured to return (in Java/Mockito, for example, this often means asserting on an argument captured with `ArgumentCaptor` rather than on the mock's stubbed return value — but no specific mechanism is mandated).

Tests that depend on isolation — a separate datastore, overridden configuration, a temporary directory — must assert that the isolation is actually in effect, not only the outcome that depends on it. Tests that touch persistent state must not depend on the starting state they find and must pass on repeated runs without cleanup.

In-process test clients can bypass parts of the real runtime, such as the server's error handling. When an approved contract fixes an error status or error body, verify it at least once through the real transport.
