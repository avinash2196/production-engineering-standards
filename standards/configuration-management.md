# Configuration Management

Purpose
- Define configuration hierarchy, separation of static vs dynamic config, and secrets handling.

Mandatory Rules
- Use `ConfigProvider` abstraction to centralize config resolution.
- Separate static config (deploy-time), dynamic config (runtime/config service), and secrets.
- Enforce precedence: Operator overrides → Dynamic config service → Environment variables → Local files → Build defaults. See `rule-precedence.md` for full rules.

Defaults
- Use environment variables for simple local overrides, and a dynamic config service for runtime tuning.
- Local config files allowed only for dev/test and must be excluded from production bundles.

Anti-patterns
- Ad-hoc `System.getenv`/`os.environ` scattered across the codebase; mixed direct reads with dynamic providers.

LLM instructions
- When generating config wiring, produce a `ConfigProvider` adapter that reads from prioritized sources and emits typed config objects.
- If the user requests direct environment reads, advise and ask a single question about whether this is for local dev only.

Review checklist
- [ ] `ConfigProvider` implemented and used across modules.
- [ ] Config sources and precedence documented.
- [ ] Local files excluded from production builds.
