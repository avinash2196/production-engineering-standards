# Engineering Principles

This document captures the non-negotiable engineering principles for systems that live in this repository. These principles are mandatory for any team scaffolding services from the `enterprise-ai-engineering` templates.

1. Configuration-First
- All runtime behavior must be configurable. Hardcoded values for feature toggles, endpoints, timeouts, or credentials are disallowed.
- Configuration sources follow the precedence and separation defined in `rule-precedence.md`.

2. Explicit Fallbacks
- For every external dependency (messaging, cache, storage, secrets) provide at least one documented fallback implementation usable in local/dev mode.
- Fallbacks are enabled explicitly by environment variables (e.g., `FALLBACK_KAFKA=db`, `FALLBACK_CACHE=jsonfile`) and must never be implicitly used in production.

3. Capability Abstractions
- Depend on abstractions (MessagePublisher, CacheProvider, ObjectStorageProvider, SecretProvider, ConfigProvider). Implementations are pluggable.

4. Layered Architecture
- Enforce controller → service → domain → repository layering. Controllers only orchestrate request validation and mapping to service calls.

5. Distributed-Ready by Default
- Implement retries, timeouts, idempotency keys, and clear async/sync boundaries. Avoid assumptions of single-node behavior.

6. Observability and Telemetry
- All services must emit structured logs, metrics (latency, error, saturation), and traces with propagated correlation IDs.

7. Security and Compliance
- No hardcoded secrets. Prefer secret managers with env fallbacks for local dev. Implement audit logging for operations involving sensitive data.

8. Performance & Testability
- Design for batching, caching, and efficient DB access. Provide unit, integration, and contract tests for critical flows.

9. Cloud-Local Parity
- Cloud integrations must have local-safe fallbacks so the service runs in development without cloud accounts.

10. Agent Interaction
- Agents must ask targeted questions only when the repository's defined defaults cannot safely resolve design choices. See `questioning-policy.md` for rules.
