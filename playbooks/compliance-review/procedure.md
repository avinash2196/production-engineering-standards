# Compliance Review Procedure

Operational steps for an evidence-based engineering compliance review. Use this procedure only when a project has explicitly adopted a compliance, security, privacy, or data-handling policy that makes the review applicable.

## When to Run

Run a review at the points required by the project's approved policy or release process. Common triggers include:

- introducing or materially changing sensitive-data handling;
- changing an explicitly adopted regulatory/control boundary;
- major architecture or authorization changes that affect protected data;
- pre-production review when required by policy;
- periodic review at a policy-defined cadence.

Do not infer HIPAA, PHI, PCI, or another regime from business-domain vocabulary alone.

## Prerequisites

Gather the evidence that exists and identify material gaps:

- service/design scope;
- data classification or approved data-handling policy;
- applicable compliance/security framework, if any;
- relevant source/configuration/deployment evidence;
- standards/policy version used for the review.

A staging deployment is not universally required just to perform a design/code review. If runtime evidence is necessary for a control, mark that control `NEEDS VERIFICATION` until the evidence exists.

## Procedure

### Step 1: Establish Applicability

Record only explicit or repository-confirmed facts:

```yaml
service_name: <service>
data_categories: <approved classifications or unknown>
applicable_framework: <framework/policy or none established>
deployment_target: <known target or unknown>
tech_stack: <stack>
standards_version: <git SHA/tag when available>
```

If missing classification/framework information materially blocks the review, ask the smallest set of questions needed before continuing.

### Step 2: Run the Review

Use either of the GitHub-native entry points:

- select `.github/agents/compliance-reviewer.agent.md` as the custom agent on a supported Copilot surface; or
- invoke `/compliance-review` from `.github/prompts/compliance-review.prompt.md` in a supported IDE.

The review must distinguish verified evidence from assumptions and use `NEEDS VERIFICATION` when a control cannot be assessed.

### Step 3: Supplement With Applicable Manual Evidence

Review only controls established by the project's classification, framework, policy, or approved architecture. Examples may include:

#### Data Handling
- [ ] Sensitive fields and stores are identified where required.
- [ ] Required at-rest/in-transit safeguards are evidenced.
- [ ] Retention/disposal behavior follows the applicable policy.
- [ ] Data minimization and non-production data handling are reviewed where applicable.

#### Access Control
- [ ] Protected resources use the approved authentication mechanism.
- [ ] Authorization decisions are enforced at an appropriate boundary when differentiated permissions exist.
- [ ] Service/workload permissions follow least privilege.

Do **not** require mTLS, JWT, RBAC, or ABAC unless the approved project model requires them.

#### Audit / Security Logging
- [ ] Required sensitive/security events are auditable.
- [ ] Audit evidence contains the fields required by the applicable policy.
- [ ] Storage/integrity/retention controls match the approved policy.

#### Third-Party and Supply Chain
- [ ] Required vendor/legal agreements are verified by the responsible process when applicable.
- [ ] Dependency/security scan evidence is current where the release policy requires it.
- [ ] License policy evidence exists where applicable.

### Step 4: Triage Findings

Use severity based on concrete exposure, impact, likelihood, and the project's approved risk process. Do not invent universal remediation SLAs.

| Severity | Typical interpretation |
|---|---|
| CRITICAL | Immediate material exposure or control failure with severe impact |
| HIGH | Significant required-control gap or likely material risk |
| MEDIUM | Partial/incomplete control or meaningful but bounded risk |
| LOW | Minor gap or hardening opportunity |
| NEEDS VERIFICATION | Insufficient evidence to decide |

### Step 5: Remediate and Re-Review

1. Track findings according to the project's approved risk/work-management process.
2. Apply approved fixes through the repository's normal PDD/TDD workflow when behavior changes.
3. Re-run focused review/checks.
4. Record what evidence changed and which findings remain open.

### Step 6: Sign-Off

Use only roles and approval gates defined by the adopting organization. Do not invent a security lead, compliance officer, release blocker, or exception authority if the project has not established one.

Store reports in the location required by the project's documentation and access-control policy.

## Report Retention

Retain review artifacts according to applicable legal, regulatory, contractual, and organizational policy. Do not turn a framework-specific documentation rule into a universal retention period for every application log or review report.

## References

- [Compliance Reviewer custom agent](../../.github/agents/compliance-reviewer.agent.md)
- [Compliance review prompt](../../.github/prompts/compliance-review.prompt.md)
- [HIPAA controls](../../standards/compliance/hipaa-controls.md)
- [Data classification](../../standards/compliance/data-classification.md)
- [Security standards](../../standards/security/security-standards.md)
