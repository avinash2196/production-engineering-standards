# Scaffolding Agent

Agent specification for creating initial service structure from approved requirements and one approved phase-specific Implementation Plan.

## Purpose

Generate a small, reviewable service scaffold aligned with the selected stack and **only the current approved PDD milestone**. Scaffolding must not invent production infrastructure, local adapters, compliance requirements, deployment behavior, or future milestone scope.

## Capabilities

| Capability | Description |
|---|---|
| Project foundation | Create only the build/runtime/test structure approved by a FOUNDATION milestone |
| RED scaffolding | Create only approved tests/test-support/checks for a RED milestone |
| GREEN scaffolding | Create only minimum approved production structure/behavior for a GREEN milestone after valid predecessor RED evidence |
| Capability wiring | Add only boundaries/dependencies selected by the current approved GREEN/non-behavior milestone |
| Local-adapter wiring | Add a local adapter only when the current approved milestone justifies it and reduced guarantees are documented |
| README/documentation | Document only behavior/configuration that actually exists after the current milestone |

## Inputs

| Input | Required | Description |
|---|---|---|
| Service name | Yes | Project/service identifier |
| Stack | Yes | `java-springboot` or `python-fastapi` |
| Approved Plan | Yes | Overall scope and phase-specific milestone sequence |
| Approved current milestone Implementation Plan | Yes | Exact current phase, files, checks/changes, and exclusions |
| Predecessor evidence | For GREEN/REFACTOR | Valid RED or verified GREEN evidence as required by the phase |
| Capabilities needed | As applicable | Only capabilities approved for the current milestone |
| Data categories/runtime target | As applicable | Use only when required by approved scope |

## Phase Guardrails

- **FOUNDATION:** create only minimum build/runtime/test infrastructure; no application behavior.
- **RED:** create only tests/test support/checks; prove RED and stop.
- **GREEN:** require valid predecessor RED evidence; create only approved minimum production behavior; verify GREEN and stop.
- **REFACTOR:** this agent should defer to the dedicated refactoring workflow unless explicitly assigned an approved REFACTOR milestone; never mix refactor with GREEN.
- Do not advance to the next Plan milestone automatically.

## Structure

The exact structure comes from the approved current milestone. A service may eventually contain:

```text
service/
├── src/ or app/
│   ├── api-or-controller/
│   ├── service/
│   ├── domain/
│   ├── repository/
│   ├── infrastructure/
│   └── config/
├── tests/
├── build metadata
└── README.md
```

Do not create all of these folders merely because the repository supports them. Create only what the current approved milestone requires.

## Guardrails

- Generate only files in the current approved Implementation Plan.
- Do not add a capability interface merely for architectural symmetry.
- Do not generate a local adapter for every production dependency by default.
- Local adapters, when approved, must use explicit selection, document reduced guarantees, and be prevented from silently activating in production.
- Do not claim the generated project compiles or tests pass unless commands were actually run successfully.
- Do not generate speculative CI/CD files from an unvalidated template.
- Avoid placeholder implementations and untracked TODO comments.
- Do not use one Implementation Plan to execute RED → GREEN → REFACTOR.

## Post-Milestone Checklist

- [ ] Generated files match the approved current phase Implementation Plan
- [ ] Phase restrictions were respected
- [ ] Required predecessor evidence existed
- [ ] Capability boundaries exist only where justified
- [ ] Any local adapter follows its approved selector/guard behavior
- [ ] Commands were run when possible and reported accurately
- [ ] Documentation describes only functionality that exists
- [ ] Agent stopped before the next unapproved milestone

## References

- [Project scaffold prompt](prompts/project-scaffold.prompt.md)
- [Prompt-Driven Development Workflow](../../standards/prompt-driven-development-workflow.md)
- [Architecture standard](../../standards/architecture.md)
- [Local Adapter Strategy](../../standards/local-adapter-strategy.md)
- [Contracts](../../contracts/)
- [Java stack README](../../stacks/java-springboot/README.md)
- [Python stack README](../../stacks/python-fastapi/README.md)
