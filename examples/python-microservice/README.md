# Python Microservice Reference Architecture

This directory is a documentation-only reference for a Python/FastAPI service. It is **not runnable** because it contains no application source or dependency manifest.

Use the executable template under `stacks/python-fastapi/project-template/` only after a plan and implementation plan have defined the required behavior and files.

## Intended Workflow

1. Approve the service plan.
2. Approve a repository-aware implementation plan.
3. Add a focused test and confirm it fails for the expected reason.
4. Implement the minimum FastAPI/application behavior needed for green.
5. Run regression checks and refactor without changing behavior.

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

## Typed Local Adapter Selection

```python
from app.config.settings import MessagingAdapter, Settings

settings = Settings(
    environment="local",
    messaging_adapter=MessagingAdapter.DB,
)
```

The database outbox retains messages across process restarts and can be inspected with SQL. It does not reproduce Kafka partitions, consumer groups, rebalancing, or production backpressure. The in-memory option is suitable only when those lost guarantees are acceptable.

## References

- [Python/FastAPI standards](../../stacks/python-fastapi/python-backend.md)
- [Executable Python template](../../stacks/python-fastapi/project-template/)
- [Prompt-driven development workflow](../../standards/prompt-driven-development-workflow.md)
- [Local adapter strategy](../../standards/local-adapter-strategy.md)
