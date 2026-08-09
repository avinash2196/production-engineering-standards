# Deployment Modes Template

Purpose
- Describe supported deployment modes (dev/local, staging, production, canary) and the differences in configuration, local adapters, production failure behavior, and infrastructure.

Modes
- Local (developer): approved local adapters may be selected explicitly; local-only config files may be allowed; secrets may use an approved local provider.
- Staging: production-like infrastructure and production adapter values unless an explicitly approved test mode says otherwise.
- Production: approved production adapter values only; local-only values are rejected; production dependency failure behavior is explicit and observable.
- Canary: controlled production rollout with feature toggles and metrics-based promotion.

Config sources per mode
- Local: env → local files → build defaults
- Staging/Canary/Production: operator overrides → dynamic config → env → build defaults

Local Adapter and Failure-Behavior Definitions
- List which local adapters are implemented and permitted per non-production mode, and document production dependency failure behavior separately.

Infra dependencies
- Map services to modes: e.g., Kafka required in staging/production; a local adapter may be allowed only in approved non-production modes.

Validation
- Deployment manifests for each mode; health checks and smoke tests must run post-deploy.
