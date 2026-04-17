# Architecture Decision Record

Template for ADRs. Copy this file into `docs/adr/` and number sequentially (e.g., `ADR-001-use-kafka.md`).

---

## ADR-NNN: [Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by [ADR-XXX]

**Date:** YYYY-MM-DD

**Author(s):** [Names]

### Context

Describe the situation that requires a decision. Include:

- What problem or requirement triggered this decision?
- What constraints exist (technical, regulatory, organizational)?
- What alternatives were considered?

### Decision

State the decision clearly in one or two sentences.

> We will use **[chosen option]** because [primary reason].

### Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| Option A | | |
| Option B | | |
| Option C | | |

### Consequences

#### Positive

- [Benefit 1]
- [Benefit 2]

#### Negative

- [Trade-off 1]
- [Trade-off 2]

#### Risks

- [Risk and mitigation]

### Compliance Impact

- **Data classification:** Does this change how PHI/PII is handled?
- **Security:** Does this introduce new attack surface?
- **Audit trail:** Does this affect audit logging requirements?

### References

- [Link to relevant standards or RFCs]
- [Link to related ADRs]
- [Engineering principles](../../standards/engineering-principles.md)

---

## Usage Instructions

1. Copy this template to `docs/adr/ADR-NNN-short-title.md`.
2. Fill in all sections. "Alternatives Considered" is mandatory even if obvious.
3. Submit as a PR. The ADR is accepted when the PR is merged.
4. To supersede, update the old ADR's status and link to the new one.
