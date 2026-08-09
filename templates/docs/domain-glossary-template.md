# Domain Glossary Template
<!--
  HOW TO USE:
  Copy to docs/domain-glossary.md (or <service>/docs/glossary.md).
  Add one row per term. Keep definitions under 2 sentences.
  See: playbooks/create-doc.md for full process.
-->

# Domain Glossary: [SERVICE / DOMAIN NAME]

**Owner:** [Team name]  
**Last updated:** YYYY-MM-DD

This glossary defines canonical terms used in code, APIs, and documentation for [domain name].
All DTOs, event names, and database column names must use these terms exactly.

## Terms

| Term | Definition | Owner | Appears in |
|------|-----------|-------|------------|
| **[TermName]** | [One sentence definition. What it is, not how it's implemented.] | [Team] | [e.g. `POST /orders` request body, `OrderCreatedEvent`] |
| **[TermName]** | [Definition] | [Team] | [API / event / DB column] |

## Local-Adapter and Degradation Terms

<!--
  Document terms that change meaning or have special handling in local-adapter or degraded-production mode.
  Example: "AuditEvent stored locally as a JSON file row during MESSAGING_ADAPTER=db mode."
-->

| Term | Normal behaviour | Fallback behaviour |
|------|-----------------|--------------------|
| [Term] | [Normal] | [Fallback] |

## Deprecated Terms

<!--
  Terms that have been renamed or removed. Keep here so older code/docs can be cross-referenced.
-->

| Old term | Replaced by | Removed in |
|----------|------------|------------|
| [OldTerm] | [NewTerm] | [Date or version] |

## References

- [Link to OpenAPI spec or event schema registry]
- [Link to database schema or ERD]

