---
applyTo: "**/*.sql,**/db/**,**/migrations/**"
---
# SQL and Migration Instructions

- Treat schema changes as production changes with rollback/recovery considerations.
- Make data-type, nullability, default, sequence/identity, index, and constraint behavior explicit.
- Do not assume Oracle and PostgreSQL semantics are equivalent.
- Verify generated SQL and ORM behavior against the target database.
- For Oracle → PostgreSQL work, apply the `oracle-to-postgres-modernization` skill.
