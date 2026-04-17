# Dependency Management

Purpose
- Define how dependencies are managed, updated, and audited to maintain security and stability.

Mandatory Rules
- Pin direct dependencies and run dependency scanning in CI for known vulnerabilities.
- Apply semantic versioning policies and require PRs for major dependency upgrades with compatibility tests.

Defaults
- Automated minor/patch updates may be applied with CI validation; major upgrades require human review and testing.

Anti-patterns
- Blindly accepting automated upgrades without tests; committing transient lockfile changes without CI validation.

LLM instructions
- When proposing dependency updates, include changelog highlights and potential breaking changes; ask for approval for major upgrades.

Review checklist
- [ ] Dependency scanning configured in CI.
- [ ] Upgrade PRs include compatibility tests and changelog summary.
