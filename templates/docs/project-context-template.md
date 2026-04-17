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
| Data classification | PHI · PII · Non-sensitive |
| Compliance requirements | [e.g. HIPAA, SOC2 Type II, PCI-DSS] |
| Authentication | [e.g. JWT via API Gateway, mTLS for internal] |
| PHI fields | [if applicable: list fields, e.g. `patient_id`, `diagnosis_code`] |

## Config Keys (summary)

| Key | Provider | Environment | Notes |
|-----|----------|-------------|-------|
| `DATABASE_URL` | Env / Vault | All | JDBC/asyncpg connection string |
| `KAFKA_BOOTSTRAP_SERVERS` | Env | All | Comma-separated host:port |
| `REDIS_URL` | Env / Vault | All | `redis://host:port` |
| `FALLBACK_KAFKA` | Env | Dev only | `db` for DB outbox, `inmemory` for ephemeral |
| `FALLBACK_CACHE` | Env | Dev only | `jsonfile` for JSON file, `inmemory` for ephemeral |
| [Add more rows] | | | |

## Fallback Configuration

| Dependency | Fallback toggle | Fallback behaviour | Data loss risk |
|------------|----------------|--------------------|----------------|
| Kafka | `FALLBACK_KAFKA=db` | Writes to `outbox_message` DB table | None — persisted |
| Redis | `FALLBACK_CACHE=jsonfile` | Reads/writes `./data/fallback-cache/cache.json` | None — persisted |
| S3 | `FALLBACK_STORAGE=local` | Reads/writes `./data/fallback-storage/` | None — local disk |
| Vault | `FALLBACK_SECRETS=env` | Reads env variables | Secrets in env — dev only |

## Key Stakeholders

| Role | Name / Team | Contact |
|------|------------|--------|
| Business owner | [Name] | [Slack/email] |
| Tech lead | [Name] | [Slack/email] |
| On-call | [Team] | [PagerDuty policy link] |
| Security reviewer | [Name] | [Slack/email] |

## References

- [Architecture diagram](docs/architecture.png)
- [OpenAPI spec](docs/openapi.yaml)
- [Runbook](docs/runbooks/)
- [ADRs](docs/decisions/)
- [Jira board / GitHub project link]

