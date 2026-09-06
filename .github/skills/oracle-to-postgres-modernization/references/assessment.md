# Assessment

Inventory before changing code.

## Database
- Oracle version and features in use
- schemas, tables, partitions
- primary/foreign/unique/check constraints
- indexes and function-based indexes
- sequences and triggers
- views/materialized views
- synonyms and database links
- stored procedures/functions/packages
- scheduled jobs
- LOBs and large tables
- isolation/locking assumptions

## Application
- JDBC driver/dialect
- native queries
- JPQL/HQL depending on Oracle functions
- stored-procedure calls
- sequence generators
- pagination
- batch behavior
- transaction isolation
- Flyway/Liquibase scripts
- test fixtures
- reporting/ETL integrations

Classify each item: portable, syntax-only change, semantic change, redesign, or cutover risk.
