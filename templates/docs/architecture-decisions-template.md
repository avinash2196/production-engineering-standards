# Architecture Decision Record (ADR) Template
<!--
  HOW TO USE:
  1. Copy this file to docs/decisions/ADR-NNN-<kebab-title>.md
  2. Fill in every section. Delete sections that do not apply.
  3. Set Status to Proposed and open a PR for review.
  See: playbooks/create-doc.md for full process.
-->

# ADR-NNN: [DECISION TITLE]

**Date:** YYYY-MM-DD  
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-NNN  
**Deciders:** [Names or roles, e.g. Backend Lead, Security, Data]

---

## Context

<!--
  What situation, constraint, or problem led to this decision?
  Include relevant background: scale requirements, compliance constraints,
  team size, existing debt, time pressure, etc.
-->

[Describe the context and problem here.]

## Decision

<!--
  State the decision clearly in one or two sentences.
  Use active voice: "We will use X for Y" not "X was chosen".
-->

[State the decision here.]

## Consequences

### Positive

- [Benefit 1]
- [Benefit 2]

### Negative / Trade-offs

- [Trade-off 1]
- [Trade-off 2]

### Neutral

- [Any side effects that are neither clearly positive nor negative]

## Alternatives Considered

| Option | Summary | Why rejected |
|--------|---------|-------------|
| [Option A] | [One-line description] | [Reason] |
| [Option B] | [One-line description] | [Reason] |

## Implementation Notes

<!--
  Key technical notes, migration steps, or constraints the implementer needs.
  Reference related config keys, fallback toggles, or infra changes.
-->

- Config keys affected: [e.g. `FALLBACK_KAFKA`, `feature.cache.ttl-seconds`]
- Infra changes required: [e.g. new RDS instance, new Kafka topic]
- Migration steps: [none | see migration/NNN-...sql]
- Rollback plan: [how to revert if this causes issues]

## References

- [Link to design doc, Jira ticket, RFC, or prior ADR]

