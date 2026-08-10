# Minimal FastAPI Project Template

This is the canonical starter for a new Python/FastAPI service.

It is intentionally small. Copying the starter must **not** preselect persistence, messaging, cache, object storage, authentication, authorization, distributed tracing, or a production deployment platform.

## Included

- Python 3.12+
- FastAPI application factory/lifecycle
- Pydantic/Pydantic Settings
- minimal startup/shutdown logging foundation
- standard-library unit tests
- Ruff and mypy development configuration

## Deliberately Not Included

Add these only through an approved phase-specific Implementation Plan when the service actually requires them:

- SQLAlchemy / database drivers / migrations
- Kafka / Pub/Sub / queues
- Redis or another cache
- S3 / GCS / other object storage
- OAuth/OIDC/JWT/security-provider SDKs
- OpenTelemetry / Prometheus / tracing exporters
- Testcontainers/emulators
- local-adapter implementations

Reference local adapters are preserved separately under:

`../reference-implementations/local-adapters/`

Those examples demonstrate capability boundaries and reduced local guarantees; they are not the default architecture for every Python service.

## Run

After installing the dependencies:

```bash
PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```

## Test

```bash
PYTHONPATH=. python -m unittest discover -s tests -p 'test_*.py'
```

## PDD Rule

Do not add service behavior directly to this starter without the normal repository workflow:

Requirements -> Plan -> RED milestone/IP -> review -> valid RED -> GREEN milestone/IP -> review -> minimal GREEN -> optional separately planned Refactor.
