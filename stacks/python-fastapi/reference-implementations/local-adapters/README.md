# Python Local-Adapter Reference Implementation

This directory is a **reference implementation**, not the canonical Python service starter.

It is intentionally capability-rich so engineers can inspect/test local adapter patterns when a real service requires them. Depending on the version moved here from the prior starter, it may include examples for database/in-memory messaging, file/in-memory cache, local filesystem storage, environment-backed local secrets, adapter selection, and production startup guards.

## Use This Reference When

- an approved Plan introduces one of these capabilities;
- the phase-specific Implementation Plan selects a local adapter for development/test use;
- reduced guarantees are documented and acceptable for that use case.

## Do Not

- copy every adapter into every Python service;
- infer Kafka/Redis/object-storage/secret requirements from the existence of this reference;
- treat local adapter behavior as production degradation/fallback;
- treat local-adapter tests as proof of managed production-service guarantees;
- allow local-only adapters to activate in production.

The canonical minimal starter remains at `../../project-template/`.
