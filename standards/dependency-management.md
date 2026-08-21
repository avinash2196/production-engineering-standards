# Dependency Management

## Purpose

Keep third-party dependencies supportable, traceable, secure, and compatible with the target runtime without imposing one package/versioning/update product on every stack.

## Rules

- Declare direct dependencies explicitly using the target ecosystem's normal manifest/lock mechanism.
- Keep reproducible resolution evidence appropriate to the ecosystem (lockfile, dependency lock, pinned artifact set, or controlled build repository).
- Run the security/license/supply-chain checks required by organization policy and release risk.
- Review breaking/major upgrades with compatibility evidence proportional to their impact.
- Remove unused dependencies and avoid adding libraries for capabilities not yet required by an approved milestone.
- Assess vulnerabilities based on affected version, reachability/exposure, exploitability, data sensitivity, and organization risk policy; do not invent a universal CVE SLA.

Semantic versioning is common but not universal. Respect the package ecosystem's actual versioning and compatibility guarantees.

## Automation

Automated dependency update tooling may open or apply changes only under the project's review/test policy. Automated minor/patch labels do not prove compatibility.

## LLM Instructions

- Inspect the manifest/lockfile and current runtime compatibility before suggesting an upgrade.
- Use primary release notes/security advisories when current version facts are needed.
- Summarize relevant breaking/security changes and required verification.
- Do not add speculative dependencies or silently upgrade unrelated packages.

## Review Checklist

- [ ] Direct dependencies are intentional and version resolution is reproducible enough for the stack.
- [ ] Required security/license/supply-chain checks exist.
- [ ] Upgrade impact is supported by release-note/test evidence.
- [ ] Unused/speculative dependencies are absent.
