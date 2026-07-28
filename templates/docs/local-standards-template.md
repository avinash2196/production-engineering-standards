# Local Standards Template

Purpose
- Define local development standards and constraints that complement central `standards/` — e.g., linting, formatters, and fallbacks allowed for dev.

Placeholders
- Local toolchain: e.g., Java 17, Python 3.11, Docker Desktop
- Formatters: e.g., `mvn fmt`, `black`, `ruff`

Fallback definitions
- Explicitly list which fallbacks are acceptable for local dev and their env toggles (e.g., `MESSAGING_ADAPTER=db`, `CACHE_ADAPTER=jsonfile`).
- Local storage paths and cleanup guidance.

Config sources in local dev
- Local config files allowed: `application.local.yml`, `settings.local.yaml` (must be gitignored and excluded from builds).

Infra dependencies
- List local-only dependencies and how to start them (docker-compose commands). Provide alternatives using fallbacks.

Validation
- Local dev must run `tooling/scripts/validate-repo-structure.ps1` and `pytest`/`mvn test` before committing.
