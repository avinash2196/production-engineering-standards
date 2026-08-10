# Python Microservice Reference Architecture

This directory is a documentation-only reference for a Python/FastAPI service. It is **not runnable** because it contains no application source or dependency manifest.

Use the minimal executable starter under `stacks/python-fastapi/project-template/` only after a Plan and the current phase-specific Implementation Plan have defined the required behavior and files. Add persistence or infrastructure packages only when that milestone requires them.
## Intended Workflow

1. Approve the service Plan with separate RED and GREEN milestones and an optional REFACTOR milestone when justified.
2. Approve the RED milestone Implementation Plan, add the focused test/check only, confirm valid RED, record evidence, and stop.
3. Approve the GREEN milestone Implementation Plan only after the predecessor RED evidence is reviewed; implement the minimum FastAPI/application behavior required for GREEN, run regression checks, record evidence, and stop.
4. When concrete cleanup is justified, approve a separate REFACTOR milestone Implementation Plan, preserve behavior, keep tests GREEN, and stop.
5. Do not auto-advance between phase milestones or authorize multiple phases from one Implementation Plan.
## Suggested Structure

```text
app/
  api/                 routers, validation, response mapping
  service/             application/use-case orchestration
  domain/              business rules and value objects where needed
  repository/          persistence ports/implementations as appropriate
  infrastructure/      vendor and local adapters
  config/              typed settings and composition
```
## Optional Local-Adapter Reference

When an approved service design needs a local adapter, use the separate reference implementation under `stacks/python-fastapi/reference-implementations/local-adapters/` as a pattern. Do not copy every adapter into the service by default.

Local adapters are explicitly selected development/test mechanisms with reduced guarantees; they are not production fallback/degradation behavior.

## References

- [Python/FastAPI standards](../../stacks/python-fastapi/python-backend.md)
- [Minimal Python starter](../../stacks/python-fastapi/project-template/)
- [Local-adapter reference](../../stacks/python-fastapi/reference-implementations/local-adapters/)
- [Prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md)
- [Local adapter strategy](../../standards/local-adapter-strategy.md)
