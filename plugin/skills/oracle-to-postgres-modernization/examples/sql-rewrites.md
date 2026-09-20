# SQL Rewrite Examples

These are examples, not mechanical replacement rules.

## Null handling

```sql
-- Oracle
SELECT NVL(display_name, legal_name) FROM customer;

-- PostgreSQL
SELECT COALESCE(display_name, legal_name) FROM customer;
```

Verify type-resolution behavior.

## Conditional expression

```sql
-- Oracle
SELECT DECODE(status, 'A', 'ACTIVE', 'I', 'INACTIVE', 'UNKNOWN') FROM account;

-- PostgreSQL
SELECT CASE status
         WHEN 'A' THEN 'ACTIVE'
         WHEN 'I' THEN 'INACTIVE'
         ELSE 'UNKNOWN'
       END
FROM account;
```

## Pagination

Do not translate `ROWNUM` blindly. Re-express the intended ordering and pagination using `ORDER BY` plus `LIMIT/OFFSET` or a keyset strategy appropriate to the API.

## Upsert

Do not assume Oracle `MERGE` and a PostgreSQL upsert are behaviorally equivalent. Verify:
- conflict key
- insert/update predicates
- concurrency behavior
- affected-row expectations
