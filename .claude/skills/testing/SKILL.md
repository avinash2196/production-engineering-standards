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

