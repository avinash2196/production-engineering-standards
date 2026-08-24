# Engineering Standards Enforcement Matrix

This matrix separates executable enforcement from AI-assisted review and advisory guidance.

A rule is described as **enforced** only when the automated-enforcement column names a mechanism that fails on violation.

| Standard | Guidance source | Review workflow | Automated enforcement | Status |
|---|---|---|---|---|
| Required standards-repository structure | `README.md` | Repository review | `validate_repository.py` and CI | Enforced |
| Active internal Markdown links resolve | Documentation guidance | Documentation review | `validate_repository.py` and CI | Enforced |
| Prompt files use supported repository frontmatter subset, current tool identifiers, and valid custom-agent bindings | Copilot customization model | Prompt review | `validate_repository.py` and CI | Enforced |
| Path-specific instructions use `.instructions.md`, include `applyTo`, and do not masquerade as repository-wide task instructions | Copilot customization model | Instruction review | `validate_repository.py` and CI | Enforced |
| Active Copilot customizations do not reintroduce blanket `apply all standards` or legacy root-agent references | Copilot customization model | Customization review | `validate_repository.py`, `test_copilot_customization_semantics.py`, and CI | Enforced |
| GitHub Copilot custom agents use `.github/agents/*.agent.md` with required metadata | Copilot customization model | Agent-profile review | `validate_repository.py` and CI | Enforced |
| Legacy top-level `agents/` hierarchy is absent | Copilot customization model | Repository review | `validate_repository.py` and CI | Enforced |
| Agent Skills use required structure and metadata | Requirements/review skills | Skill review | `validate_repository.py` and CI | Enforced |
| Packaged repository excludes IDE/Python cache artifacts | Repository hygiene | Repository review | `validate_repository.py` and CI (`PYTHONDONTWRITEBYTECODE=1`) | Enforced in this repository |
| Known placeholder implementations are rejected | Definition of Done | Code review | `validate_repository.py` and CI | Enforced |
| Plan and Implementation Plan templates exist | PDD workflow | Planning review | Required-path validator | Enforced in this repository |
| RED/GREEN/optional-REFACTOR remain separate phase milestones in active guidance | PDD workflow | Planning/code review | `test_pdd_workflow_semantics.py` and CI | Enforced in this repository |
| Plan precedes Implementation Plan | PDD workflow | Human approval gate | Workflow/prompt behavior; project CI not yet implemented | Reviewed |
| Tests precede production implementation | PDD workflow | Implementation review | Service-specific CI and commit history evidence | Project responsibility |
| Python local-adapter reference defaults to runnable zero-infrastructure local adapters and rejects those adapters in production | Local adapter strategy | Production-readiness review | `test_app.py`, `test_settings.py`, `test_local_adapter_reference_semantics.py`, and CI | Enforced for reference implementation |
| Adopting-service local-only adapters cannot run in production | Local adapter strategy | Production-readiness review | Startup configuration validation and tests in each service | Project responsibility |
| Dependency failure behavior is documented | Degradation strategy | Distributed-systems review | No generic static check | Reviewed |
| Domain/application boundaries are respected | Architecture standard | Architecture/code review | ArchUnit or import-boundary tests recommended per project | Project responsibility |
| No committed secrets | Security standards | Security review | Secret scanner recommended per project | Project responsibility |
| External calls have timeouts | Resiliency standard | Distributed-systems review | Stack-specific static or integration checks where available | Reviewed |
| Method/class size guidance | Coding standards | Code review | Not a blocking numeric gate | Advisory |
| Local-adapter activation warning | Local adapter strategy | Production-readiness review | Python provider-selection tests in CI | Enforced for Python reference implementation |
| Local-adapter/degradation metrics and recovery telemetry | Local adapter and degradation standards | Production-readiness review | Service-specific metrics/integration tests | Project responsibility |

## Classification Used in Review Reports

- `AUTOMATED` — a test, validator, static check, or CI gate fails on violation.
- `REVIEWED` — engineering judgment and evidence are required.
- `ADVISORY` — a recommended default with justified exceptions.

## Planned Evolution

Potential future enforcement should be added only when the check is reliable and does not reward superficial compliance:

- Java ArchUnit dependency-boundary tests
- Python import-linter rules
- secret and dependency scanning
- adapter production-guard contract tests
- plan/implementation-plan schema validation
- service-specific API and event contract tests
