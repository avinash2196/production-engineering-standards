# Production Readiness

Purpose
- Checklist and automated gates required before service deployment to production.

Mandatory Rules
- Health checks (readiness and liveness) implemented and exercised in orchestration.
- Alerts and SLO targets defined for key metrics (latency, error rate, availability).
- Backup and recovery procedures documented for stateful components.

Defaults
- Default SLO: availability 99.9% for user-facing services; configurable via `ConfigProvider`.
- Default alerting: page on SLO breach and on sustained error spikes.

Anti-patterns
- Deploying without monitoring, rollout, or rollback strategy.

LLM instructions
- When producing deployment manifests, include health probes, resource requests/limits, and environment toggles for fallbacks.
- Ask the user if there are budget or regional constraints that affect deployment topology.

Review checklist
- [ ] Health probes configured.
- [ ] SLOs and alerting documented.
- [ ] Rollout and rollback procedures defined.
