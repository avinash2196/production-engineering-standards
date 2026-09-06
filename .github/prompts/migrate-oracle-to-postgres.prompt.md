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

Start with assessment; do not mechanically convert SQL. Build a Plan that separates:
1. discovery/assessment,
2. target schema and compatibility decisions,
3. RED migration/application tests,
4. GREEN application/schema/data changes,
5. performance and reconciliation,
6. cutover/recovery,
7. optional cleanup/refactor.

Do not claim migration safety until PostgreSQL-specific verification evidence exists.
