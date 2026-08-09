# Production Readiness

## Purpose

Define evidence that should be reviewed before a service is deployed to production.

## Mandatory Rules

- Readiness and liveness behavior is defined and exercised for the target orchestrator where applicable.
- Service-level objectives or operational targets are documented for the signals that matter to the service.
- Alerting reflects business impact, service objectives, and the operating/on-call model.
- Stateful components have documented backup, restore, and recovery expectations where applicable.
- Rollout and rollback behavior is documented and tested to the level required by deployment risk.
- Production adapter selectors use approved production values; local-only selections are rejected by startup validation.

## Target Selection

SLO targets must come from approved service requirements, operating history, or an explicit project decision. Do not invent repository-wide availability or latency targets.

Alert thresholds and routing should reflect service SLOs, business impact, dependency behavior, and the operating model of the adopting project.

## Anti-patterns

- Deploying without monitoring, rollback, or ownership.
- Copying a generic availability percentage into a service without understanding business impact.
- Treating a passing local-adapter test as evidence of production dependency behavior.

## LLM Instructions

- When producing deployment guidance, include health probes and resource boundaries only when supported by the target platform and approved plan.
- Ask for or locate the project's availability/latency/recovery requirements instead of inventing them.
- Keep local-adapter configuration separate from production dependency degradation.

## Review Checklist

- [ ] Health/readiness behavior is appropriate for the service's dependency contract.
- [ ] SLOs or operational targets are documented with rationale/source.
- [ ] Alerts map to meaningful failure conditions and ownership.
- [ ] Rollout and rollback procedures are defined.
- [ ] Backup/restore and recovery are addressed for stateful components where applicable.
- [ ] Production configuration rejects local-only adapters.
