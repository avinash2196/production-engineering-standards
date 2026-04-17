# Release Process

Release and tagging workflow guidance for promoting services through environments.

## Overview

All services follow a trunk-based development model with automated CI/CD. Releases are immutable artifacts (container images) promoted through environments without rebuilding.

## Branching Model

```
main (trunk)
  ├── feature/PROJ-123-add-payment   (short-lived, < 2 days)
  ├── feature/PROJ-456-fix-timeout   (short-lived)
  └── hotfix/PROJ-789-critical-fix   (from main, merged back to main)
```

**Rules:**
- `main` is always deployable.
- Feature branches live < 2 days. Use feature flags for longer work.
- No long-lived release branches.
- Hotfixes branch from `main` and merge back to `main`.

## Release Flow

```
1. Developer merges PR to main
2. CI pipeline runs:
   a. Build + unit tests
   b. Lint + static analysis
   c. Contract tests
   d. Build container image
   e. Tag image with: git SHA + semver
   f. Push to container registry
3. CD pipeline promotes to staging (automatic)
4. Staging validation (smoke tests + integration tests)
5. Production promotion (manual approval gate)
6. Post-deploy verification (health checks + canary metrics)
```

## Versioning

Use **semantic versioning** (`MAJOR.MINOR.PATCH`):

| Change type | Version bump | Example |
|-------------|-------------|----------|
| Breaking API change | MAJOR | `2.0.0` |
| New feature (backward compatible) | MINOR | `1.3.0` |
| Bug fix | PATCH | `1.2.4` |

Container images are tagged with both:
- `v1.2.4` (human-readable)
- `abc123f` (git SHA, for traceability)

## Tagging

```bash
# Tag the release
git tag -a v1.2.4 -m "Release 1.2.4: add payment retry logic"
git push origin v1.2.4
```

The CI pipeline detects the tag and builds the release artifact.

## Pre-Release Checklist

- [ ] All tests pass on `main` (unit, integration, contract).
- [ ] No CRITICAL or HIGH CVEs in dependency scan.
- [ ] Compliance review is current (if data categories changed).
- [ ] Database migrations are backward-compatible (expand-then-contract).
- [ ] Feature flags are configured for any partially-complete features.
- [ ] Changelog is updated.
- [ ] Runbook is updated if operational procedures changed.

## Database Migration Strategy

Migrations must be **backward-compatible** to support rolling deployments:

```
Release N:   Add new column (nullable) + write to both old and new columns
Release N+1: Migrate data, switch reads to new column
Release N+2: Drop old column
```

Never rename or drop a column in the same release that changes the app code.

## Rollback Procedure

### Automatic Rollback
- If canary metrics show error rate > 5% within 10 minutes of deploy, auto-rollback.
- If health check fails 3 consecutive times, auto-rollback.

### Manual Rollback

```bash
# Redeploy previous image
kubectl set image deployment/order-service \
  order-service=registry.example.com/order-service:v1.2.3

# Or via CD tool
cd rollback --service=order-service --version=v1.2.3
```

### Post-Rollback
1. Notify the team channel.
2. Create an incident ticket.
3. Analyze the failure (logs, traces, metrics).
4. Fix forward — do not leave the main branch in a broken state.

## Changelog

Maintain a `CHANGELOG.md` in each service repository:

```markdown
## [1.2.4] - 2026-04-16
### Fixed
- Payment retry now respects idempotency key (#PROJ-789)

### Added
- Webhook notification for order status changes (#PROJ-456)

## [1.2.3] - 2026-04-10
### Fixed
- Connection pool exhaustion under load (#PROJ-750)
```

Follow [Keep a Changelog](https://keepachangelog.com/) format.

## Environment Promotion

| Environment | Deploy trigger | Approval | Tests |
|-------------|---------------|----------|-------|
| CI | Every PR | Automatic | Unit + contract |
| Staging | Merge to main | Automatic | Smoke + integration |
| Production | Manual promotion | Team lead | Canary + health checks |

## References

- [Coding standards](../../standards/coding-standards.md)
- [Observability](../../standards/observability.md)
- [Security standards](../../standards/security/security-standards.md)
