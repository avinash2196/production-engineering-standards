# Messaging Abstraction

## Purpose

Guidance for asynchronous messaging/event boundaries. Use the optional `MessagePublisher` / `MessageSubscriber` contracts when they create a useful boundary; do not require them for every broker integration.

## Required Decisions

For each message flow, establish from requirements and broker semantics:

- event/command ownership and schema compatibility;
- delivery semantics actually provided/required;
- acknowledgement and redelivery behavior;
- idempotency/deduplication requirements based on duplicate-effect risk;
- ordering/partitioning assumptions;
- transaction/outbox consistency needs;
- retry/dead-letter/recovery behavior;
- message size/retention/security constraints;
- tracing/correlation context when operationally useful.

Do not claim exactly-once semantics without end-to-end evidence. Do not default every flow to at-least-once, add `idempotencyKey`/`traceId` fields universally, or invent partition keys.

## Boundary

Keep transport SDK types out of domain/business policy when the project adopts a capability boundary. Handler/application boundaries should make side effects, acknowledgement, and duplicate behavior clear.

For local/CI testing, choose mocks/fakes, Testcontainers, official emulators, approved local adapters, or ephemeral brokers according to fidelity needs. A local adapter is not required for every broker.

## LLM Instructions

- Determine delivery, duplicate, ordering, and consistency requirements before designing the message interface.
- Use the selected broker's actual semantics; do not normalize away important guarantees/failures.
- Add idempotency/correlation fields only when the flow needs them or an established event schema requires them.

## Review Checklist

- [ ] Delivery/ack/redelivery semantics are understood.
- [ ] Duplicate/idempotency behavior matches side-effect risk.
- [ ] Ordering/consistency assumptions are explicit where relevant.
- [ ] Boundary/local-test strategy is justified rather than automatic.
