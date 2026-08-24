# Python Local-Adapter Reference Implementation

This directory is a **reference implementation**, not the canonical Python service starter.

It demonstrates explicit local-development/test adapters for:

- database-backed or in-memory message publishing;
- JSON-file or in-memory caching;
- local filesystem object storage;
- environment-backed local secrets;
- typed adapter selection and production startup guards.

## Run the Reference

From this directory, install this reference implementation's dependencies and run:

```bash
PYTHONPATH=. uvicorn app.main:app --reload
```

The checked-in defaults deliberately select zero-infrastructure local adapters (`inmemory`, `inmemory`, `local`, and `env`) so the reference can start without Kafka, Redis, object storage, or a secret manager. Selecting a production adapter remains an explicit project decision, and the reference does not pretend to implement those managed adapters.

## Use This Reference When

- an approved Plan introduces one of these capabilities;
- the phase-specific Implementation Plan selects a local adapter for development/test use;
- the reduced guarantees are documented and acceptable for that use case.

## Do Not

- copy every adapter into every Python service;
- infer Kafka, Pub/Sub, Redis, object-storage, or secret-manager requirements from this reference;
- treat local adapter behavior as production degradation/fallback;
- treat these tests as proof of managed production-service guarantees;
- allow local-only adapters to activate in production.

Production adapters are intentionally absent. The factories fail with an actionable planning error until an approved milestone adds the selected production adapter.

The canonical minimal starter remains at `../../project-template/` and deliberately contains none of these capability packages.
