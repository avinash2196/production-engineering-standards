# Plan — Final PDD Requirements Gate and Agent Skills

## Status

Ready for owner review.

## Goal

Finalize the repository as the v1 baseline before using it to build real Java Spring Boot and Python FastAPI services by strengthening the **Requirements → Plan** boundary and making the same non-assumptive behavior available through GitHub Copilot Agent Skills.

Preserve the published PDD lifecycle:

> **Requirements → Plan → Human Review → Implementation Plan → Human Review → RED Tests → GREEN Code → Refactor → Final Review**

This change adds a requirements-analysis gate inside the existing Requirements → Plan transition. It does not add another required planning artifact or change the RED/GREEN/refactor model.

## Current-State Summary

- The core PDD workflow already requires Plan and Implementation Plan approval, test-first RED, minimal GREEN, separate refactoring, and final review.
- Java and Python base templates are capability-minimal; integrations are selected by approved milestones rather than preloaded universally.
- General code review and production-readiness review are already applicability/risk based.
- A dedicated requirements-analysis skill is not yet present under `.github/skills/`.
- `create-plan.prompt.md` asks when a material requirement is unclear but does not yet use a shared requirements-analysis evidence model.
- `standards/questioning-policy.md` still contains an arbitrary question-count cap and legacy wording that can encourage defaults instead of surfacing material ambiguity.
- The current `review-code.prompt.md` contains malformed YAML list markers even though the repository validator correctly rejects that syntax.
- The repository validator does not yet validate Agent Skill structure/frontmatter.

## Scope

### Milestone 1 — Requirements Analysis Gate

- Add a repository `requirements-analysis` Agent Skill.
- Add `/review-requirements` as an explicit review-only workflow.
- Update always-on Copilot guidance and `/create-plan` so material ambiguity causes numbered questions and stops Plan creation.
- Replace the questioning policy with a materiality-based policy: ask the smallest set of current-boundary questions; do not invent or prematurely decide later-milestone behavior.
- Align the backend service builder with the same gate.

### Milestone 2 — Review Skill and Prompt Correctness

- Add a `code-review` Agent Skill that reinforces the existing evidence-based reviewer behavior.
- Fix `review-code.prompt.md` frontmatter without changing its substantive review philosophy.

### Milestone 3 — Executable Skill Validation and Public Documentation

- Add validator tests for Agent Skill structure/frontmatter before validator implementation.
- Validate required skill metadata and directory/name consistency.
- Update README and enforcement status to describe skills accurately.
- Add repository hygiene ignore rules if not already present.

## Out of Scope

- Healthcare-platform feature code.
- Inventing healthcare-specific HIPAA, PHI, retention, authorization, or SLO requirements.
- New architecture patterns, production adapters, persistence technologies, cloud platforms, or deployment targets.
- Rewriting already-correct code-review, production-readiness, Java-template, or Python-template guidance.
- Changing the public PDD lifecycle or creating a mandatory Requirements document artifact beyond the input already supplied by a project.

## Risks

- Requirements analysis could become bureaucratic if agents ask questions that are irrelevant to the current milestone; the policy must use materiality and defer later decisions.
- Skills are contextually loaded by Copilot, so anti-invention rules must remain in always-on instructions and explicit prompts rather than relying on skills alone.
- Skill validation must remain a dependency-free check of the repository-supported metadata shape, not pretend to implement a full YAML parser.

## Success Criteria

- Planning never silently resolves a material requirement gap from framework defaults, industry conventions, or likely architecture choices.
- When material current-scope information is missing or contradictory, the workflow asks numbered clarification questions and stops before Plan creation.
- When information belongs to a later milestone, the workflow records/defer it instead of interrogating the user early.
- `/review-requirements`, `/create-plan`, the service builder, questioning policy, and requirements-analysis skill express the same rule.
- Code review remains evidence-based, applicability-scoped, and capable of reporting concrete correctness defects without checklist inflation.
- `review-code.prompt.md` uses valid supported frontmatter.
- Agent Skill structure and metadata are covered by executable validator tests.
- README and enforcement documentation accurately describe the new skills and checks.
- No healthcare-specific behavior or technical dependency is invented by this repository-level change.
