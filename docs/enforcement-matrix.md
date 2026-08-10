# Engineering Standards Enforcement Matrix

This matrix separates executable enforcement from AI-assisted review and advisory guidance.

A rule is described as **enforced** only when the automated-enforcement column names a mechanism that fails on violation.

| Standard | Guidance source | Review workflow | Automated enforcement | Status |
|---|---|---|---|---|
| Required standards-repository structure | `README.md` | Repository review | `validate_repository.py` and CI | Enforced |
| Active internal Markdown links resolve | Documentation guidance | Documentation review | `validate_repository.py` and CI | Enforced |
| Prompt files use supported frontmatter | Agent execution standard | Prompt review | `validate_repository.py` and CI | Enforced |
| Agent Skills use required structure and metadata | Requirements/review skills | Skill review | `validate_repository.py` and CI | Enforced |
| Known placeholder implementations are rejected | Definition of Done | Code review | `validate_repository.py` and CI | Enforced |
| Plan and Implementation Plan templates exist | PDD workflow | Planning review | Required-path validator | Enforced in this repository |
| Plan precedes Implementation Plan | PDD workflow | Human approval gate | Workflow/prompt behavior; project CI not yet implemented | Reviewed |
| Tests precede production implementation | PDD workflow | Implementation review | Service-specific CI and commit history evidence | Project responsibility |
| Python template local-only adapters cannot run in production | Local adapter strategy | Production-readiness review | `Settings` startup validation plus `test_settings.py` in CI | Enforced for Python template |
| Adopting-service local-only adapters cannot run in production | Local adapter strategy | Production-readiness review | Startup configuration validation and tests in each service | Project responsibility |
| Dependency failure behavior is documented | Degradation strategy | Distributed-systems review | No generic static check | Reviewed |
| Domain/application boundaries are respected | Architecture standard | Architecture/code review | ArchUnit or import-boundary tests recommended per project | Project responsibility |
| No committed secrets | Security standards | Security review | Secret scanner recommended per project | Project responsibility |
| External calls have timeouts | Resiliency standard | Distributed-systems review | Stack-specific static or integration checks where available | Reviewed |
| Method/class size guidance | Coding standards | Code review | Not a blocking numeric gate | Advisory |
| Local-adapter activation warning | Local adapter strategy | Production-readiness review | Python provider-selection tests in CI | Enforced for Python template |
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
