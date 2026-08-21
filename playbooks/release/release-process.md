# Release Process

## Purpose

Reference guidance for designing a repeatable, traceable, and recoverable release process. The adopting project's source-control model, artifact type, environments, approval gates, versioning scheme, and deployment platform remain explicit project/organization decisions.

## Required Outcomes

A production release process should provide evidence for the outcomes that apply:

- the released artifact/revision is uniquely identifiable and traceable to source;
- required automated tests/checks ran against the intended revision/artifact;
- production deployment uses an approved artifact without unreviewed mutation;
- rollout and rollback/forward-recovery behavior are defined for material risk;
- schema/data migrations preserve compatibility for the selected deployment strategy;
- required security/compliance/release approvals are captured;
- post-deployment verification can detect a bad release;
- operators know how to recover.

## Source-Control Model

Trunk-based development is one valid model, not a repository-wide mandate. Teams may use trunk-based, release branches, GitFlow-like models, or another approved process as long as the model preserves reviewability, traceability, and release correctness.

If using short-lived branches, document merge/review requirements. If using long-lived release branches, document synchronization/backport rules and how divergence risk is controlled.

## Artifact and Versioning

Prefer immutable/reproducible release artifacts when the platform supports them. Artifact examples include container images, packages, binaries, serverless revisions, infrastructure bundles, or signed source releases.

Use the project's established version/identifier scheme—semantic versioning, calendar versioning, Git SHA, build number, release ID, or another stable convention. Do not add SemVer solely because this playbook exists.

## Example Release Flow

```text
approved change
  -> build/test/security checks
  -> create identifiable release artifact/revision
  -> environment-specific verification/approval as required
  -> deploy/promote
  -> post-deploy verification
  -> rollback or forward recovery if acceptance criteria fail
```

The number/names of environments and manual gates are organization-specific. A project may deploy directly to production with strong automated controls or may require staging/canary/manual approval.

## Database / State Changes

Plan migrations according to the deployment topology and compatibility window. Expand-then-contract is a common safe pattern for rolling/mixed-version deployments, but not every migration needs three releases.

Avoid destructive changes while old application versions still depend on the old schema/state unless the deployment strategy guarantees they cannot coexist and the risk is explicitly accepted.

## Rollout and Recovery

Define measurable release acceptance/failure signals from the service SLOs and known risks. Do not copy universal thresholds such as “5% errors for 10 minutes” or “3 failed probes.”

Recovery may be:

- rollback to a prior immutable artifact;
- roll forward with a fix;
- disable/limit a feature through an approved mechanism;
- traffic shift/canary reversal;
- data repair/reconciliation when state has changed.

Record special recovery constraints for irreversible migrations or side effects.

## Pre-Release Checklist

Use only applicable checks:

- [ ] Required automated tests/checks pass for the release revision.
- [ ] Required security/dependency/image/source findings are assessed under the organization's risk policy.
- [ ] API/schema/data compatibility is understood.
- [ ] Configuration/secrets for the target environment are validated safely.
- [ ] Required documentation/runbook/migration steps are current.
- [ ] Release artifact/revision is identifiable and traceable.
- [ ] Rollout acceptance and recovery criteria are defined for material risks.
- [ ] Required human/compliance/change-management approvals are recorded.

## Release Record Template

```markdown
## Release <identifier>
- Source revision: <sha/change-set>
- Artifact/revision: <immutable identifier>
- Changes: <summary/links>
- Required checks: <evidence>
- Migration/config changes: <details or N/A>
- Rollout strategy: <strategy>
- Verification signals: <signals>
- Recovery strategy: <strategy>
- Approvals: <when applicable>
```

## References

- [Production Readiness](../../standards/production-readiness.md)
- [Observability](../../standards/observability.md)
- [Security Engineering Standard](../../standards/security/security-standards.md)
