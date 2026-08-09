# Compliance Review Procedure

Operational steps for running a compliance review using the compliance-review-agent and checklists.

## When to Run

| Trigger | Scope | Required? |
|---------|-------|-----------|
| New service creation | Full review | Yes |
| Pre-production launch | Full review | Yes |
| Periodic review | Scope/frequency defined by applicable compliance/security policy | As required by policy |
| Data category change | Targeted review | Yes |
| Major architecture change | Targeted review | Yes |
| Dependency with known CVE | Security-focused review | Yes |

## Prerequisites

- [ ] Service has a design document or architecture description.
- [ ] Data categories are documented (PHI, PII, internal, public).
- [ ] Service is deployed to at least a staging environment.
- [ ] Standards repository is at a known version (note the git SHA).

## Procedure

### Step 1: Prepare Inputs

Gather the following for the compliance-review-agent:

```yaml
service_name: order-service
data_categories: [PII, internal]
deployment_target: AWS EKS / Azure AKS
tech_stack: java-springboot
design_doc: docs/design/order-service.md
standards_version: abc123f  # git SHA of this repo
```

### Step 2: Run Automated Review

```bash
@compliance-review-agent review \
  --service=order-service \
  --data-categories=PII,internal \
  --design-doc=docs/design/order-service.md
```

The agent will produce a structured **Compliance Review Report** (see `agents/compliance-review-agent/spec.md` for output format).

### Step 3: Manual Checklist Supplement

The automated review cannot verify everything. Complete these manually:

#### Data Handling
- [ ] All PHI/PII fields are identified in the data model.
- [ ] Encryption at rest is enabled for all data stores containing PHI/PII.
- [ ] Data retention policies are defined and implemented.
- [ ] Data disposal procedures are documented.
- [ ] Cross-border data transfer requirements are met.

#### Access Control
- [ ] Service-to-service authentication uses mTLS or JWT.
- [ ] User authentication integrates with the organization's IdP.
- [ ] RBAC/ABAC policies are defined for all endpoints.
- [ ] Admin endpoints are restricted to authorized roles.

#### Audit Trail
- [ ] Access to sensitive data produces audit log entries.
- [ ] Audit logs include: who, what, when, from-where.
- [ ] Audit logs are shipped to a tamper-resistant store.
- [ ] Log retention meets the applicable legal/regulatory/organizational policy; do not infer a universal six-year audit-log rule from HIPAA documentation retention.

#### Third-Party Dependencies
- [ ] All third-party services handling PHI have a Business Associate Agreement (BAA).
- [ ] Third-party dependencies are scanned for known CVEs.
- [ ] No non-approved open-source licenses in the dependency tree.

### Step 4: Triage Findings

Categorize each finding:

| Severity | Default release disposition | Remediation timing |
|---|---|---|
| CRITICAL | Block release unless an authorized exception exists | Follow the organization's incident/risk process |
| HIGH | Normally block release or require explicit risk acceptance | Follow the approved risk/remediation policy |
| MEDIUM | Track and prioritize based on impact/exposure | Project/security policy |
| LOW | Track when useful | Project policy |

### Step 5: Remediate and Re-Review

1. Create tickets for all findings at MEDIUM or above.
2. Apply fixes.
3. Re-run the compliance-review-agent on the updated codebase.
4. Verify all previously-failed checks now pass.

### Step 6: Sign-Off

| Role | Responsibility |
|------|---------------|
| Service owner | Confirms all findings addressed |
| Security lead | Approves CRITICAL/HIGH remediations |
| Compliance officer | Signs off on HIPAA-regulated services |

Store the signed-off report in `docs/compliance/` within the service repository.

## Report Retention

- Retain compliance reports according to the applicable regulatory and organizational documentation-retention policy. HIPAA does require six-year retention for specified required documentation, but applicability to a particular report must be determined rather than assumed.
- Tag reports with the standards version used.
- Store in a version-controlled, access-controlled location.

## References

- [Compliance Review Agent spec](../../agents/compliance-review-agent/spec.md)
- [Compliance check prompt](../../agents/compliance-review-agent/prompts/compliance-check.prompt.md)
- [HIPAA controls](../../standards/compliance/hipaa-controls.md)
- [Data classification](../../standards/compliance/data-classification.md)
- [Security standards](../../standards/security/security-standards.md)
