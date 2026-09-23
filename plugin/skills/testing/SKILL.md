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

Tests must verify behavior produced by the system or unit under test — a mocked dependency must not supply the exact value or behavior the assertion is meant to prove. When a unit computes or transforms data before calling a dependency, verify the argument, state change, or observable behavior the unit actually produced, not a value the mock was configured to return (in Java/Mockito, for example, this often means asserting on an argument captured with `ArgumentCaptor` rather than on the mock's stubbed return value — but no specific mechanism is mandated).

