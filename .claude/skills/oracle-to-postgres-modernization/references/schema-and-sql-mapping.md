# Schema and SQL Mapping

Treat mappings as design decisions, not blind conversions.

| Oracle | PostgreSQL consideration |
|---|---|
| `NUMBER(p,0)` | `integer`/`bigint`/`numeric` based on actual range |
| `NUMBER(p,s)` | `numeric(p,s)` |
| `VARCHAR2` | `varchar`/`text` based on constraints/usage |
| `DATE` | Oracle DATE includes time; choose `timestamp` or `date` intentionally |
| `TIMESTAMP WITH TIME ZONE` | evaluate `timestamptz` semantics |
| `CLOB` | usually `text`, verify size/access pattern |
| `BLOB` | `bytea` or large-object approach based on usage |
| sequence + trigger | identity or sequence depending on compatibility |
| `NVL` | often `COALESCE`, verify typing |
| `SYSDATE` | choose PostgreSQL time function based on transaction/statement semantics |
| `DECODE` | usually `CASE` |
| `ROWNUM` | usually `LIMIT`/window/query rewrite |
| `MERGE` | use PostgreSQL-supported merge/upsert pattern appropriate to target version |
| empty string | PostgreSQL does not automatically treat `''` as `NULL` |

Also verify:
- identifier case/quoting
- null ordering
- string concatenation and implicit casts
- date arithmetic
- regex/functions
- locking clauses
- optimizer hints (do not copy)
- index strategy using PostgreSQL plans, not Oracle assumptions
