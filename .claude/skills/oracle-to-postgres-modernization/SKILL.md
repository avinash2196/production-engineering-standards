---
name: oracle-to-postgres-modernization
description: Use when assessing, planning, implementing, testing, or reviewing migration of an Oracle-backed Java/Spring Boot application to PostgreSQL.
---

# Oracle to PostgreSQL Modernization

This is a **skill**, not a standalone agent. It provides domain knowledge that different responsibility-focused agents can apply.

## Required Workflow

1. Assess Oracle usage and classify migration risk.
2. Inventory schema, SQL, PL/SQL, sequences, triggers, indexes, constraints, jobs, database links, and Oracle-specific ORM configuration.
3. Define target PostgreSQL semantics before translating syntax.
4. Plan schema/data migration and application changes as separate but coordinated workstreams.
5. Add compatibility and migration tests before cutover.
6. Use staged rollout or controlled downtime based on consistency and business requirements.
7. Reconcile row counts, checksums/business totals, constraints, and critical queries after migration.
8. Preserve a documented recovery path until the migration is accepted.

Read the references in this skill before proposing concrete conversions.

## Do Not

- perform mechanical search/replace of Oracle SQL
- assume Oracle `NUMBER`, empty-string/null behavior, date/time semantics, sequences, or locking map 1:1
- keep Oracle compatibility layers forever without an exit plan
- claim performance parity without PostgreSQL execution evidence

