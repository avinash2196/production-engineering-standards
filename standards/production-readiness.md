# Production Readiness Standard

## Purpose

Define evidence required to decide whether a service is safe to deploy to its actual production environment.

Production readiness is outcome- and risk-based. Review every readiness area for applicability, but do not require every possible enterprise mechanism for every service.

## Status Model

Every reviewed area must be classified as one of:

- `PASS` — an applicable requirement is supported by evidence.
- `FAIL` — an applicable requirement is violated or required evidence is missing.
- `NOT APPLICABLE` — the area/mechanism does not apply and the reason is stated.
- `NEEDS VERIFICATION` — applicability or evidence cannot be established from available context.

`NOT APPLICABLE` is not a shortcut. State why the item does not apply.

`NEEDS VERIFICATION` must be used instead of inventing a target environment, SLO, compliance obligation, security mechanism, or dependency behavior.

## Readiness Areas

### 1. Build and Release

Verify applicable evidence for:

- reproducible build/package creation;
- tests/checks required by the project;
- dependency/source/image scanning adopted by the project;
- versioning/artifact identity;
- release provenance where required;
- rollback or safe redeployment strategy proportional to release risk.

Do not require containers when the selected runtime does not use them.

### 2. Configuration and Secrets

Verify:

- required configuration is explicit and validated;
- production-unsafe/local-only selections are rejected where applicable;
- multiple configuration sources have deterministic precedence when they exist;
- secrets are not committed and use an approved production mechanism;
- configuration failures produce safe startup/runtime behavior.

Do not require dynamic configuration or a specific secret product unless selected by the system design.

### 3. Security and Privacy

Verify applicable evidence for:

- trust-boundary input validation;
- authentication for protected resources;
- authorization where identities have differing access;
- least privilege;
- secure transport at the approved boundary;
- safe secret handling;
- sensitive-data protection according to approved classification;
- no sensitive leakage through logs/metrics/traces/errors;
- adopted compliance controls.

Apply HIPAA/PHI-specific checks only when the project explicitly establishes that scope.

### 4. Observability and Operations

Verify that operators can detect and diagnose meaningful failures through the telemetry selected for the service:

- useful logging;
- metrics tied to workload/failure modes/SLOs where applicable;
- correlation across boundaries where useful;
- distributed tracing where cross-service diagnosis requires it;
- health/readiness behavior required by the target platform;
- actionable alerting and ownership where operational alerts are part of the model.

Do not universally require OpenTelemetry, every golden signal, Prometheus, or separate health endpoints.

### 5. Dependencies, Resilience, and Failure Behavior

For each important remote/managed dependency, verify applicable behavior for:

- timeout/bounded waiting;
- retry safety and limits when retry is used;
- idempotency/duplicate handling where effects can repeat;
- ordering/concurrency where workload correctness depends on them;
- queue/DLQ/reconciliation behavior where messaging exists;
- explicit fail-fast/fail-closed/degraded/stale/bypass behavior where justified;
- graceful shutdown/work-drain behavior according to runtime/workload.

Do not require circuit breakers, durable queues, fallback, or stale serving when the dependency/risk model does not justify them.

### 6. Data and Persistence

When the service owns or modifies state, verify applicable evidence for:

- schema/migration strategy;
- transaction boundaries;
- data integrity constraints;
- concurrency/conflict behavior;
- backup/restore/recovery expectations where required;
- data retention/deletion only when requirements/policy define them;
- safe migration/rollback behavior proportional to risk.

### 7. Capacity and Performance

Verify only targets established by workload expectations or approved NFRs.

Evidence may include:

- load/capacity tests;
- resource limits;
- autoscaling settings;
- queue/backlog thresholds;
- concurrency/thread/connection-pool sizing;
- rate limiting/backpressure.

Do not invent throughput, latency, concurrency, or availability targets.

### 8. Deployment Target

Review mechanisms that apply to the selected target, such as:

- container/image hardening;
- Kubernetes probes/resources;
- serverless concurrency/timeouts;
- VM/service-unit behavior;
- ingress/network policy;
- deployment rollout strategy;
- infrastructure-as-code controls.

Do not require Kubernetes, Docker Compose, service mesh, or a particular cloud product without target-specific justification.

### 9. Testing and Verification

Verify evidence for approved behavior and important failure paths.

Use realistic integration/contract tests where they provide material confidence. Local adapters may validate application contracts/local workflows but do not prove production dependency guarantees.

Do not use a repository-wide coverage percentage as a substitute for behavior-focused test evidence.

### 10. Operational Ownership

Where the service is production-operated, identify enough ownership information to respond to incidents and releases.

This may include:

- owning team/service owner;
- escalation path/on-call model where applicable;
- runbook links for meaningful failure modes;
- dashboard/alert ownership;
- recovery procedure ownership.

Do not invent an on-call model or escalation SLA if the organization has not defined it.

## Production Readiness Verdict

Use:

- `READY` — no blocking `FAIL` or unresolved verification item required for safe deployment remains.
- `CONDITIONALLY READY` — deployment may proceed only with clearly stated approved conditions; use sparingly and according to organizational policy.
- `NOT READY` — one or more blockers make deployment unsafe or violate an approved requirement.

A missing fact that is essential to the verdict remains `NEEDS VERIFICATION`; do not turn it into a guessed `PASS` or `FAIL`.

## PDD Integration

Production readiness does not bypass PDD gates.

When readiness remediation changes behavior or production code/configuration, add the appropriate approved milestone(s) and phase-specific Implementation Plan(s). Preserve separate RED/GREEN/optional-REFACTOR control boundaries for behavior-changing work.

A review finding is not authorization to implement an unplanned mechanism.

## Anti-Patterns

- Treating production readiness as "add Docker + metrics + JWT + probes".
- Marking optional mechanisms as release blockers without applicability evidence.
- Inventing SLOs, compliance requirements, deployment targets, or recovery objectives.
- Treating successful local-adapter tests as proof of production dependency behavior.
- Skipping an applicable security/data/recovery area because it is inconvenient.
- Declaring READY while required evidence is still unknown.
