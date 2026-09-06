# Spring Boot Configuration Example

Representative migration points only; adapt to the project's Spring Boot and Hibernate versions.

## Dependency

Replace the Oracle JDBC dependency with the PostgreSQL JDBC driver through the project's approved dependency-management approach.

## Datasource

Oracle-style configuration:

```properties
spring.datasource.url=jdbc:oracle:thin:@//db-host:1521/SERVICE
spring.datasource.username=app
```

PostgreSQL-style configuration:

```properties
spring.datasource.url=jdbc:postgresql://db-host:5432/appdb
spring.datasource.username=app
```

Credentials should come from the approved secret provider, not source control.

## Identifier generation

Do not blindly preserve an Oracle sequence configuration. Decide whether the PostgreSQL target should use:
- an explicit sequence for compatibility, or
- identity/generated columns for a deliberate target design.

Verify Hibernate allocation size and generated-key behavior with integration tests against PostgreSQL.

## Native queries

Search for:
- `NVL`
- `DECODE`
- `ROWNUM`
- `SYSDATE`
- `CONNECT BY`
- optimizer hints
- Oracle outer-join syntax
- PL/SQL calls

Translate semantics, not tokens.
