# Verification and Cutover

## Before cutover
- schema objects reconciled
- full/incremental data-copy process tested
- application integration suite green against PostgreSQL
- critical query plans measured
- backup/recovery tested
- observability dashboards ready
- freeze/dual-write/CDC strategy explicitly chosen

## Data reconciliation
Use more than row counts where correctness matters:
- counts by business partition/status/date
- sums/totals for financial or quantitative columns
- deterministic checksums where suitable
- orphan/constraint checks
- sampled business records
- sequence/identity high-water marks

## Cutover patterns
Choose based on business constraints:
- controlled downtime with final delta
- CDC replication then switchover
- temporary dual-read verification
- dual-write only when the consistency complexity is justified and tested

## After cutover
Monitor:
- error rate
- connection pool saturation
- lock waits/deadlocks
- slow queries
- replication/CDC lag if still active
- data reconciliation drift
- sequence/identity collisions
- job/reporting behavior

Keep recovery options until acceptance criteria are met.
