# Deployment Modes Template

Purpose
- Describe supported deployment modes (dev/local, staging, production, canary) and the differences in config, fallbacks, and infra.

Modes
- Local (developer): fallbacks enabled, local-only config files allowed, secrets via env.
- Staging: production-like infra, fallbacks disabled, pre-production config, short-lived test data.
- Production: no fallbacks, secrets via SecretProvider, monitoring and SLOs enforced.
- Canary: controlled production rollout with feature toggles and metrics-based promotion.

Config sources per mode
- Local: env → local files → build defaults
- Staging/Canary/Production: operator overrides → dynamic config → env → build defaults

Fallback definitions
- Clearly list which fallbacks are permitted per mode and how they are enabled/disabled.

Infra dependencies
- Map services to modes: e.g., Kafka required in staging/production; local fallback allowed only in Local.

Validation
- Deployment manifests for each mode; health checks and smoke tests must run post-deploy.
