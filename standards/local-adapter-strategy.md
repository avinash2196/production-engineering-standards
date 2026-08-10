# Local Adapter Strategy

## Purpose

Allow developers and CI jobs to exercise service behavior without requiring every external platform. Local adapters are explicit development/testing implementations; they are not automatic production failover mechanisms.

## Decision Rule

Add a local adapter only when it provides meaningful value beyond mocks, Testcontainers, or an official emulator.

Questions:

- Does the team need to run offline or without cloud credentials?
- Does inspectable local state improve troubleshooting or learning?
- Can the adapter preserve enough semantics for the intended test?
- Would Testcontainers or an emulator provide more realistic behavior with less custom code?

## Standard Adapter Selectors

| Variable | Production values | Local-only values |
|---|---|---|
| `MESSAGING_ADAPTER` | `kafka`, `pubsub` | `db`, `inmemory` |
| `CACHE_ADAPTER` | `redis` | `jsonfile`, `inmemory` |
| `STORAGE_ADAPTER` | `s3`, `gcs` | `local` |
| `SECRET_ADAPTER` | `vault`, `secretmanager` | `env` |

Projects may support fewer values. Do not advertise an adapter that is not implemented and tested.

## Required Guarantees

1. The local adapter implements the same capability contract used by application code.
2. Selection is explicit and typed.
3. Startup emits a structured warning. When the project exposes application metrics, expose an adapter-active metric as well.
4. Documentation states reduced durability, ordering, consistency, concurrency, security, and multi-instance behavior.
5. Production startup rejects local-only values.
6. Adapter selection tests cover production and local values.
7. Local adapter data paths avoid real secrets and are safe to delete.

## Preferred Local Implementations

| Capability | Preferred local adapter | Why | Important limitation |
|---|---|---|---|
| Messaging | Database-backed queue/outbox | Durable across restarts and inspectable with SQL | Not equivalent to broker partitioning, fan-out, or consumer groups |
| Messaging | In-memory queue | Very small isolated tests | No durability or multi-instance coordination |
| Cache | JSON-file cache | Inspectable and restart-persistent | No distributed atomicity or safe concurrent writers by default |
| Cache | In-memory cache | Fast unit/local behavior | Process-local and lost on restart |
| Storage | Local filesystem | Easy inspection | No managed durability, lifecycle, encryption, or multi-instance coordination |
| Secrets | Environment provider | Simple local bootstrap | No rotation, centralized audit, or managed access policy |

## Production Guard

Production startup must fail when a local-only adapter is selected. Do not silently replace it with a production default because that can hide a deployment error.

Example validation behavior:

```text
environment=production + MESSAGING_ADAPTER=db → startup failure
```

## Test-First Implementation

Adding a local adapter follows the same phase-milestone PDD lifecycle as any behavior-changing work:

1. Add or confirm the approved Plan milestones for the adapter behavior.
2. Create and review a **RED milestone Implementation Plan** for contract, selector, and production-guard tests only.
3. Execute the RED milestone, confirm the expected RED, record evidence, and stop.
4. Create and review a separate **GREEN milestone Implementation Plan** for the smallest adapter and selector wiring required by the approved RED tests.
5. Execute the GREEN milestone, confirm focused and regression tests are GREEN, record evidence, and stop.
6. Create a separate **REFACTOR milestone and Implementation Plan only when justified**; keep behavior unchanged and tests GREEN.

Approval of the RED milestone does not authorize GREEN implementation. Approval of GREEN does not authorize refactoring.

## LLM Instructions

- Do not generate a local adapter automatically for every production dependency.
- Prefer the most inspectable implementation that preserves needed semantics.
- Keep local adapter selection separate from production degradation behavior.
- Reject production use through typed startup validation.
- State behavior differences explicitly rather than claiming parity.
- Do not collapse RED, GREEN, and optional REFACTOR work into one Implementation Plan.

## Review Checklist

- [ ] Local adapter has a justified development/CI use case
- [ ] RED tests were planned, reviewed, executed, and shown to fail for the expected missing behavior before GREEN implementation
- [ ] GREEN implementation has its own approved milestone and Implementation Plan
- [ ] Local-only values are typed and explicit
- [ ] Production startup rejects local-only values
- [ ] Reduced guarantees are documented
- [ ] Activation is observable
- [ ] Documentation lists only implemented adapters
