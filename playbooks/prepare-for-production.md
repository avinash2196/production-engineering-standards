# Playbook: Prepare a Service for Production

## Goal

Prepare an already planned and implemented service for its actual production environment without turning a generic enterprise checklist into invented architecture.

This playbook reviews every production-readiness area for applicability. It does **not** require every possible mechanism for every service.

## Preconditions

Before using this playbook:

- the service behavior is represented in an approved Plan;
- completed behavior-changing work has valid RED/GREEN evidence under the PDD workflow;
- the target environment and operating expectations are known enough to review, or unresolved items will be marked `NEEDS VERIFICATION`;
- no local-only adapter is being treated as automatic production fallback behavior.

## Step 1 — Establish Production Context

Read:

- approved requirements and `docs/.ai/Plan.md`;
- current service code/configuration;
- target runtime/deployment documentation;
- explicit NFRs/SLOs when they exist;
- explicit data classification/compliance requirements when they exist.

Do not infer missing compliance, SLO, cloud, Kubernetes, security, or dependency requirements from the words "enterprise" or "healthcare".

If a missing fact materially prevents safe readiness planning, ask the user or record it as `NEEDS VERIFICATION` according to the task.

## Step 2 — Classify Each Readiness Area

For each area use:

- `PASS`
- `FAIL`
- `NOT APPLICABLE`
- `NEEDS VERIFICATION`

Every `NOT APPLICABLE` must include a reason.

Review:

1. Build/release
2. Configuration/secrets
3. Security/privacy
4. Observability/operations
5. Dependencies/resilience/failure behavior
6. Data/persistence
7. Capacity/performance
8. Deployment target
9. Testing/verification
10. Operational ownership

Use `standards/production-readiness.md` as the canonical detail.

## Step 3 — Configuration and Secrets

Check applicable evidence:

- required config is explicit/validated;
- source precedence is deterministic when multiple sources exist;
- local-only selections are rejected in production where applicable;
- secrets use an approved mechanism and are not committed/logged;
- invalid required config fails safely.

Do not add dynamic configuration or a secret-manager product unless the approved design requires it.

## Step 4 — Security and Data Protection

Check actual trust boundaries and data classification:

- validate untrusted input;
- authenticate protected resources;
- authorize differing access where required;
- enforce least privilege;
- protect sensitive traffic/data at approved boundaries;
- prevent secret/sensitive-data leakage;
- verify adopted security/compliance controls.

Do not automatically choose JWT, mTLS, RBAC, ABAC, OAuth provider, or HIPAA/PHI controls.

## Step 5 — Observability

Confirm operators have enough evidence to detect/diagnose meaningful failures.

Select only justified mechanisms:

- structured/searchable logs;
- safe correlation identifiers;
- metrics tied to actual workload/failure/SLO needs;
- distributed tracing for meaningful cross-service diagnosis;
- health/readiness semantics required by the runtime;
- actionable alerts with ownership.

Do not require OpenTelemetry, Prometheus, every golden signal, or separate `/live`/`/ready` endpoints by convention.

## Step 6 — Dependency and Failure Behavior

For important dependencies confirm applicable:

- timeout behavior;
- bounded/safe retry where used;
- idempotency/duplicate handling;
- ordering/concurrency behavior;
- queue/DLQ/reconciliation behavior when messaging exists;
- explicit degradation/fail-fast/fail-closed behavior where required;
- graceful shutdown/drain behavior.

Do not invent circuit breakers, queues, stale serving, or fallback merely to make the service look resilient.

## Step 7 — Deployment and Recovery

Review only the selected target:

- container hardening if containers are used;
- probes/resources/autoscaling if the platform uses them;
- rollout/rollback behavior;
- migration behavior for schema changes;
- backup/restore/recovery for stateful components when required;
- infrastructure/configuration needed by the actual target.

Docker Compose is local-development tooling, not a universal production-readiness requirement.

## Step 8 — Create Remediation Milestones

A readiness review does not authorize implementation by itself.

For every blocking change:

1. trace it to an approved requirement/standard and concrete risk;
2. update the Plan if new repository-changing scope is needed;
3. for behavior-changing work create separate RED and GREEN milestones;
4. create a phase-specific Implementation Plan for the current milestone;
5. obtain human review;
6. execute only the approved phase and stop.

Use a separate REFACTOR milestone only when justified.

## Step 9 — Re-Review

After remediation, run the production-readiness review again and record:

- remaining blockers;
- non-blocking improvements;
- `NOT APPLICABLE` rationale;
- `NEEDS VERIFICATION` evidence still required.

Do not declare `READY` while a fact essential to safe deployment remains unresolved.

## Example Output

```markdown
## Production Readiness Review: document-service

### Verdict: NOT READY

| Area | Status | Evidence / Gap | Required Action |
|---|---|---|---|
| Configuration | PASS | Typed required settings validated at startup | None |
| Observability | NEEDS VERIFICATION | No approved operating/SLO model yet | Confirm production monitoring expectations |
| Resilience | FAIL | Remote inference call has no bounded timeout | Plan timeout behavior and add RED/GREEN milestones |
| Deployment | NOT APPLICABLE | Target runtime is not Kubernetes | None |
| Security/Privacy | NEEDS VERIFICATION | Data classification not established | Resolve classification before selecting controls |
```

## Exit Criteria

Preparation is complete when:

- production-readiness review has no blocking `FAIL`;
- verification required for safe deployment is resolved;
- all remediation followed the normal PDD gates;
- no optional mechanism was treated as mandatory without applicability evidence;
- no production mechanism was invented from generic enterprise/healthcare terminology.
