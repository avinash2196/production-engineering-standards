# Project Context Template
<!--
  HOW TO USE:
  Copy to docs/project-context.md (or place at root as CONTEXT.md).
  Fill in every section. The agent reads this file to understand your project.
  See: playbooks/create-doc.md for full process.
-->

# Project Context: [PROJECT / SERVICE NAME]

**Owner:** [Team name]  
**Contact:** [Slack channel or email]  
**Last updated:** YYYY-MM-DD

## Summary

<!--
  One paragraph. What does this service do, why does it exist, and
  which business capability does it own?
-->

[One-paragraph description]

## Domain

| Item | Value |
|------|-------|
| Primary domain entities | [e.g. Order, OrderLine, Payment] |
| Bounded context | [e.g. Order Management] |
| Owns data for | [e.g. `orders`, `order_lines` tables] |
| Does NOT own | [e.g. Customer data — reads from Customer service] |

## Traffic & SLOs

| Metric | Target |
|--------|--------|
| Expected RPS (peak) | [e.g. 500] |
| Latency p50 | [e.g. ≤ 50 ms] |
| Latency p95 | [e.g. ≤ 200 ms] |
| Latency p99 | [e.g. ≤ 500 ms] |
| Availability | [e.g. 99.9%] |
| Max acceptable data loss | [e.g. 0 — all writes must be durable] |

## Stack

| Component | Choice |
|-----------|--------|
| Language / Framework | [e.g. Java 21 + Spring Boot 3.4 or Python 3.12 + FastAPI] |
| Database | [e.g. PostgreSQL 16] |
| Messaging | [e.g. Kafka 3.x via MessagePublisher] |
| Cache | [e.g. Redis 7 via CacheProvider] |
| Storage | [e.g. AWS S3 via ObjectStorageProvider] |
| Secrets | [e.g. HashiCorp Vault via SecretProvider] |

## Security & Compliance

| Item | Value |
|------|-------|
| Data classification | [Approved project classification, if applicable] |
| Compliance requirements | [Explicitly applicable policy/framework, or N/A] |
| Authentication | [Approved mechanism for protected resources, or N/A for public resources] |
| Sensitive/regulatory data | [List only if classification/policy establishes it] |

## Config Keys (summary)

| Key | Provider | Environment | Notes |
|-----|----------|-------------|-------|
| `[CONFIG_KEY]` | [Framework/platform source] | [Environment/scope] | [Purpose] |
| `MESSAGING_ADAPTER` | Env | Dev only | `db` for DB outbox, `inmemory` for ephemeral |
| `CACHE_ADAPTER` | Env | Dev only | `jsonfile` for JSON file, `inmemory` for ephemeral |
| [Add more rows] | | | |

## Local Adapter and Production Failure Configuration

| Dependency | Local adapter selector/value | Local reduced guarantees | Production failure behavior |
|------------|----------------|--------------------|----------------|
| Kafka | `MESSAGING_ADAPTER=db` | Writes to `outbox_message` DB table | None — persisted |
| Redis | `CACHE_ADAPTER=jsonfile` (if implemented) | File-backed, no distributed atomicity/concurrency | [bypass/stale/fail based on approved contract] |
| S3/GCS | `STORAGE_ADAPTER=local` (if implemented) | Local disk only; no managed durability/IAM/lifecycle parity | [retry/fail/queue based on approved contract] |
| Managed secret service (if used) | `SECRET_ADAPTER=env` only if this local adapter is adopted | Reads explicitly supplied local env values | Local-only reduced security; never an automatic production fallback |

## Key Stakeholders

| Role | Name / Team | Contact |
|------|------------|--------|
| Business owner | [Name] | [Slack/email] |
| Tech lead | [Name] | [Slack/email] |
| On-call | [Team] | [PagerDuty policy link] |
| Security reviewer | [Name] | [Slack/email] |

## References

- Architecture diagram: `docs/architecture.png` *(adjust the relative path to match where this context file is stored)*
- OpenAPI spec: `docs/openapi.yaml` *(adjust the relative path to match where this context file is stored)*
- Runbook: `docs/runbooks/`
- ADRs: `docs/decisions/`
- Jira board / GitHub project: [add project URL]

