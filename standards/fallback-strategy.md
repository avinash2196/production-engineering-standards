# Production Dependency Failure and Degradation Strategy

## Required Decision

For every critical external dependency, document which behavior applies when the dependency becomes unavailable:

- fail fast
- fail closed
- retry with bounded backoff
- circuit break
- queue for later processing
- serve stale data
- bypass a non-critical capability
- provide reduced functionality

## Decision Factors

- Could continuing cause incorrect business results?
- Could data be lost?
- Is ordering required?
- Is duplicate processing acceptable?
- Is stale data safer than unavailable data?
- Does the dependency protect authorization, secrets, or compliance?
- Can the operation be replayed safely?
- How will operators know degraded mode is active?

## Examples

### Messaging unavailable

For non-loss-tolerant events, persist the event and business update in the same transaction through an outbox pattern. Do not silently replace durable messaging with an in-memory queue.

### Cache unavailable

Treat Redis as optional only when the system of record can safely handle the additional load. Bypass the cache and emit telemetry. Do not fail open when cached values are used for authorization, rate limits, locks, or correctness-sensitive coordination.

### Secret provider unavailable

Fail closed. Do not fall back to insecure or stale credentials in production.

### Object storage unavailable

Reject the upload or persist a durable pending record. Do not report success before durable storage is confirmed unless the API explicitly defines asynchronous acceptance.
