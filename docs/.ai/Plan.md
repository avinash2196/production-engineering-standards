# Plan — Final Repository Convergence

## Status

Completed on 2026-08-23; final owner review remains the publication gate.

## Goal

Converge the repository on one stable GitHub Copilot customization and engineering-governance model, remove legacy semantics and broken references, strengthen executable regression checks, and verify the distributable repository from a clean extraction before publication.

The repository keeps the canonical lifecycle:

> **Requirements → Plan → Human Review → Implementation Plan → Human Review → RED Tests → GREEN Code → Refactor → Final Review**

This convergence does not add a new engineering architecture or compliance requirement. It aligns existing artifacts with the already-approved model.

## Frozen Customization Model

| Construct | Responsibility |
|---|---|
| `.github/copilot-instructions.md` | Repository-wide stable guidance |
| `.github/instructions/*.instructions.md` | Automatic path/file-specific guidance only |
| `.github/prompts/*.prompt.md` | Explicit reusable tasks on supported VS Code local-agent surfaces |
| `.github/agents/*.agent.md` | Specialized roles with their own tool boundaries |
| `.github/skills/*/SKILL.md` | Reusable capabilities loaded/invoked when relevant |
| `standards/` | Normative engineering principles and decision rules |
| `playbooks/` | Procedures for applying standards |
| `templates/` | Starting structures, not mandatory architecture |
| `examples/` and reference implementations | Demonstrations, not universal defaults |

## Convergence Scope

1. Audit active Copilot customizations for malformed frontmatter, obsolete tool identifiers, legacy paths, task-vs-path instruction misuse, and blanket standards application.
2. Bind specialist prompt files to the matching custom agents and keep the tool boundary in the agent profile.
3. Preserve requirement/risk/applicability-driven behavior in codebase, maintenance, distributed-systems, production-readiness, and compliance reviews.
4. Prevent generated ADRs/document workflows from inventing approval or bypassing PDD gates.
5. Make the Python local-adapter reference independently runnable with safe zero-infrastructure local defaults and explicit production guards.
6. Extend the dependency-free validator and repository semantic tests so these regressions fail CI.
7. Align README, customization documentation, contributing guidance, glossary, and enforcement matrix with the implemented behavior.
8. Produce a clean package without Git metadata, IDE state, bytecode, or test caches and re-run validation after extraction.

## Out of Scope

- Adding new agents, skills, capability contracts, production adapters, deployment platforms, or compliance regimes.
- Claiming that adopting services are production-ready merely because they use this repository.
- Replacing project-specific security scanning, dependency scanning, architecture tests, service tests, or operational validation.
- Introducing technology choices not justified by an adopting project's requirements and approved design.

## Acceptance Criteria

- No obsolete top-level `agents/` hierarchy.
- No task-specific globally applied `.instructions.md` file.
- All prompt/agent/skill/instruction frontmatter parses as YAML and follows the repository-supported conventions.
- Prompt files contain no known legacy VS Code tool identifiers and custom-agent prompt bindings resolve.
- No active customization uses blanket `apply all standards` semantics or stale root-agent references.
- HIPAA/compliance review establishes applicability before applying controls and does not claim certification.
- ADR/document workflows do not invent approval, deciders, policy, or silent authorization.
- The canonical Python starter remains capability-minimal.
- The local-adapter reference starts with checked-in defaults, declares its own runtime dependencies, and rejects local-only selections in production.
- Repository validator and all repository/starter/reference tests pass from a clean extracted package.
- README accurately limits the production claim: this repository supports governed production engineering; it does not make generated applications automatically production-ready.
