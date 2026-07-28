# Engineering Principles

## 1. Plan Before Implementation

For qualifying changes, separate requirements, Plan, Implementation Plan, tests, code, and refactoring. A plan defines scope; it is not permission to generate code.

**Evidence:** approved planning artifacts and RED/GREEN command results.

## 2. Protect Meaningful Boundaries

Use capability contracts around external systems when they improve testing, provider isolation, or migration safety. Do not create interfaces only because a template says every dependency needs one.

**Evidence:** application/domain code does not depend on provider SDK details where a boundary is justified.

## 3. Define Failure Behavior, Not a Universal Fallback

Every external dependency must have documented failure behavior. Choose fail fast, fail closed, bounded retry, circuit break, durable queue, stale data, bypass, or reduced functionality based on correctness and business impact.

Security, authorization, secrets, and correctness controls normally fail closed. Optional caches may be bypassed only when the system of record can safely absorb the load.

**Evidence:** dependency failure matrix, tests, and operational telemetry.

## 4. Separate Local Adapters from Production Degradation

A local database queue, JSON-file cache, local filesystem, or environment secret provider helps development and CI. It is not automatically a production failover mechanism.

Local-only adapters must be explicit, observable, document reduced guarantees, and fail startup in production.

**Evidence:** typed adapter settings and production-guard tests.

## 5. Test at the Right Level

Write approved behavior tests before production code. Use unit tests for policy, integration tests for adapters and persistence, contract tests for API/event boundaries, and end-to-end tests for critical flows only.

**Evidence:** valid RED before implementation, then focused and regression GREEN.

## 6. Make Transactions and Idempotency Explicit

Define local transaction boundaries and rollback behavior. Use idempotency keys, inbox/outbox, ordering keys, or saga coordination only when duplicate, partial, or distributed processing risks require them.

**Evidence:** tests for rollback, duplicate handling, ordering, or replay where applicable.

## 7. Build Security into Boundaries

Validate external input, enforce least privilege, retrieve production secrets through managed providers, and prevent sensitive data from entering standard logs.

**Evidence:** security tests/scans and review findings.

## 8. Operate What You Build

Provide logs and health information sufficient for the support model. Add metrics and tracing according to service criticality and incident-diagnosis needs, not as decorative boilerplate.

**Evidence:** operational checks and production-readiness review.

## 9. Prefer Evidence over Absolutes

Architecture and code-quality rules should identify concrete risk. Numeric line counts, layer counts, and dependency counts are review signals, not universal proof of poor design.

**Evidence:** findings explain impact and remediation rather than only quoting a threshold.

## 10. Human Review Remains a Gate

AI can accelerate planning, testing, implementation, and review, but humans approve scope, architecture trade-offs, and production readiness.

## LLM Instructions

- Follow the PDD lifecycle for qualifying changes.
- Do not require a fallback for every dependency; require explicit failure behavior.
- Distinguish local adapters from production degradation.
- Use concrete evidence when reporting violations.
- Do not invent requirements, infrastructure, or compliance controls.

## Review Checklist

- [ ] Planning and test gates were followed
- [ ] Boundaries and abstractions are justified
- [ ] Failure behavior is explicit
- [ ] Local adapters cannot silently run in production
- [ ] Transactions/idempotency are addressed where relevant
- [ ] Security and observability match actual risk
- [ ] Findings are evidence-based

## References

- [PDD Workflow](prompt-driven-development-workflow.md)
- [Architecture](architecture.md)
- [Local Adapter Strategy](local-adapter-strategy.md)
- [Production Dependency Failure and Degradation](fallback-strategy.md)
