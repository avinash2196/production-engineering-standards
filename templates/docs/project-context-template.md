# Project Context Template

Purpose
- Capture the minimal contextual information required to reason about a project: business domain, stakeholders, compliance constraints, and target environments.

Placeholders
- Project name: <PROJECT_NAME>
- Short description: <ONE_LINE_SUMMARY>
- Business owner: <TEAM>
- Stakeholders: <NAMES/TEAMS>

Domain / Data
- Primary domain entities: <list>
- Expected throughput (RPS): <estimate>
- Latency SLOs: <p50/p95/p99>

Config & Overrides
- Primary config keys and default locations: list keys and note whether they are operator-overrides, dynamic, env, or local-file.

Fallbacks
- Which dependencies have fallbacks enabled in dev and how they behave (durability, ordering, consistency).

Infra dependencies
- Required infra: e.g., `postgresql:13`, `kafka:2.x`, `redis:6`, `object-storage`.
- Local dev mapping: which services can use fallbacks and what environment toggles to set.

Security & Compliance
- Data classification (PHI/PII/Non-sensitive)
- Compliance owners and required controls

Notes
- Add links to ADRs, diagrams, and runbooks.
