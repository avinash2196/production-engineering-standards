---
description: "Assess and plan migration of an Oracle-backed Spring Boot application to PostgreSQL."
argument-hint: "application/database scope and migration objective"
agent: "planner"
tools:
  - read
  - search
  - edit
---
Apply `oracle-to-postgres-modernization`, `requirements-analysis`, `architecture-design`, and `prompt-driven-development`.

Start with assessment; do not mechanically convert SQL. The Plan covers:
1. discovery/assessment,
2. target schema and compatibility decisions,
3. application, schema, and data changes,
4. performance and reconciliation,
5. cutover/recovery.

Type each milestone by the kind of change (`prompt-driven-development` Milestone Types), not by a fixed migration sequence: a migration step that preserves observable behavior is OTHER, with baseline behavior tests as its preserved tests and migration verification and reconciliation as its completion evidence; behavior the migration changes is RED then GREEN; a changed external contract is CONTRACT; missing test infrastructure the RED milestones need is FOUNDATION; behavior-preserving cleanup of production code afterwards is REFACTOR.

Do not claim migration safety until PostgreSQL-specific verification evidence exists.
