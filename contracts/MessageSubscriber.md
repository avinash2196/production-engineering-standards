# MessageSubscriber

## Purpose

Define the consume-side contract for messages while keeping application handlers independent of broker-specific records and acknowledgement APIs.

## Contract Decisions

The approved plan must define:

- topic/subscription and schema;
- handler input and context;
- acknowledgement/commit point;
- idempotency or deduplication strategy;
- retryable versus terminal failures;
- dead-letter/quarantine behavior;
- ordering scope and concurrency;
- shutdown, replay, and recovery expectations.

At-least-once delivery requires idempotent handling or a durable deduplication strategy. Do not assume every broker or local adapter has equivalent delivery semantics.

## Processing Rule

A message is acknowledged only after the required business transaction succeeds. If a duplicate is safely recognized, acknowledge it without repeating the side effect.

## Production and Local Differences

Production broker consumers may support partitions, consumer groups, checkpoints, rebalancing, dead-letter routing, and multi-instance processing. A database-table poller may provide inspectability and persistence but not equivalent partition/rebalance semantics. An in-memory consumer is process-local and ephemeral.

## Failure and Observability

- Bound retries and avoid retry storms.
- Preserve the original failure context without logging sensitive payloads.
- Track received, processed, duplicate, retry, failure, dead-letter, and processing-duration signals as applicable.
- Continue trace/correlation context across the handler.

## Test-First Requirements

Add tests before implementation for:

- successful processing and acknowledgement;
- transaction failure with no premature acknowledgement;
- duplicate delivery;
- retry and terminal/dead-letter behavior;
- ordering/concurrency assumptions where material;
- graceful shutdown and redelivery;
- local selector and production guard behavior.

## Review Checklist

- [ ] Acknowledgement point is explicit
- [ ] Idempotency/deduplication has an owner and durable strategy where required
- [ ] Retry and terminal failure behavior are bounded
- [ ] Local adapter limitations are documented
- [ ] Tests cover duplicates and failed transactions

## References

- [MessagePublisher](MessagePublisher.md)
- [Messaging abstraction](../standards/messaging-abstraction.md)
