# Scaffolding Agent

Agent specification for creating an initial service structure from approved requirements and an approved Implementation Plan.

## Purpose

Generate a small, reviewable service scaffold aligned with the selected stack and only the capabilities approved for the project. Scaffolding must not invent production infrastructure, local adapters, compliance requirements, or deployment behavior that is absent from the approved plan.

## Capabilities

| Capability | Description |
|---|---|
| Project generation | Create the initial service structure from stack-specific guidance/templates |
| Capability wiring | Add only approved capability boundaries such as messaging, caching, storage, secrets, and configuration |
| Local-adapter wiring | Add a local adapter only when the approved plan justifies one and its reduced guarantees are documented |
| Configuration scaffolding | Generate typed environment-specific configuration for selected capabilities |
| Test scaffolding | Create the test structure required by the approved Implementation Plan |
| README generation | Document how to build, test, configure, and run the scaffold |

## Inputs

| Input | Required | Description |
|---|---|---|
| Service name | Yes | Project/service identifier |
| Stack | Yes | `java-springboot` or `python-fastapi` |
| Approved Implementation Plan | Yes | Exact milestone scope, files, tests, and capability choices |
| Capabilities needed | As applicable | Only capabilities approved in the plan |
| Data categories | As applicable | Data handled by the service when known/required |
| Database/API style/deployment target | As applicable | Use only when specified or approved |

## Expected Structure

The exact structure comes from the approved Implementation Plan. A typical service may contain:

```text
service/
├── src/ or app/
│   ├── api-or-controller/
│   ├── service/
│   ├── domain/
│   ├── repository/
│   ├── infrastructure/      # only selected external capabilities
│   └── config/
├── tests/
├── build metadata
└── README.md
```

Do not generate an `infrastructure/fallback/` package. If a local adapter is approved, place it under an explicit local-adapter namespace or package consistent with the target stack and project conventions.

## Guardrails

- Generate only files in the approved Implementation Plan.
- Do not add a capability interface merely for architectural symmetry; it must protect a meaningful boundary.
- Do not generate a local adapter for every production dependency by default.
- Local adapters, when approved, must use explicit typed selection, document reduced guarantees, and fail startup if selected in production.
- Do not claim the generated project compiles or tests pass unless the relevant commands were actually run successfully.
- Do not generate speculative CI/CD files from an unvalidated repository template. Add pipeline files only when the project has an approved pipeline design or a tested project-specific workflow.
- Avoid placeholder implementations and untracked TODO comments.

## Post-Scaffold Checklist

- [ ] Generated files match the approved Implementation Plan.
- [ ] Capability boundaries exist only where justified.
- [ ] Any local adapter has selector tests and a production guard planned or implemented as required by the milestone.
- [ ] Build/test commands were run when the environment supports them, and results are reported accurately.
- [ ] README describes only functionality that actually exists.

## References

- [Project scaffold prompt](prompts/project-scaffold.prompt.md)
- [Prompt-Driven Development Workflow](../../standards/prompt-driven-development-workflow.md)
- [Architecture standard](../../standards/architecture.md)
- [Local Adapter Strategy](../../standards/local-adapter-strategy.md)
- [Contracts](../../contracts/)
- [Java stack README](../../stacks/java-springboot/README.md)
- [Python stack README](../../stacks/python-fastapi/README.md)
