# Spring Boot Migration

## Dependencies and configuration
- replace Oracle JDBC driver with PostgreSQL JDBC driver
- remove Oracle-specific Hibernate dialect/config where modern Hibernate can detect PostgreSQL or set the approved PostgreSQL dialect
- update datasource URL, credentials, SSL, pool validation, and health checks
- review HikariCP sizing using PostgreSQL connection limits and workload

## Persistence
- review `@SequenceGenerator`, identity strategy, allocation size, and generated-key behavior
- find native SQL and Oracle functions
- verify pagination and locking
- verify boolean/enum/UUID/JSON handling
- verify batch inserts/updates and generated IDs
- review transaction isolation assumptions

## Migrations
Prefer versioned Flyway/Liquibase scripts for target schema. Keep Oracle and PostgreSQL migration histories separated or explicitly conditioned during coexistence; do not create ambiguous scripts that are valid for neither database.

## Testing
Use PostgreSQL integration tests for database-specific behavior. H2 is not evidence that Oracle-to-PostgreSQL semantics are correct.
