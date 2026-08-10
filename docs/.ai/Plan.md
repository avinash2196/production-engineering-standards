# Plan — Final Consistency Hardening

## Status

Ready for owner review.

## Goal

Make the repository a stable public baseline for two intended uses:

1. guiding real Java Spring Boot and Python FastAPI implementation through the repository lifecycle; and
2. reviewing those changes using applicable standards without checklist inflation.

This is a consistency-hardening pass, not an expansion of the standards catalog.

## Current-State Findings

- The core Prompt-Driven Development standard correctly treats milestones as delivery outcomes and RED/GREEN/Refactor as execution stages inside each implementation milestone, but service-builder guidance still models RED and GREEN as separate milestones.
- General code-review guidance is strong, but the reviewer specification contains older universal-review wording and an overly broad HIPAA trigger.
- Production-readiness review still requires mechanisms too universally instead of determining applicability from the target runtime, dependencies, requirements, and risk.
- Prompt frontmatter validation is dependency-free but does not fully validate the repository-supported YAML shape, allowing malformed list syntax to escape CI.
- The Java template preloads database, messaging, cache, security, observability, storage, and integration-test dependencies even when a service does not use those capabilities.
- The Python template declares production-adapter and observability dependencies that are not part of its implemented base behavior.
- Generated IDE/cache/coverage artifacts are tracked and should not be part of the public baseline.

## Scope

### Milestone 1 — Workflow and Review Consistency

Align service-building, general review, production-readiness review, and agent execution guidance with the existing PDD and applicability-based standards.

### Milestone 2 — Executable Enforcement Hardening

Strengthen prompt-frontmatter validation and add regression tests for malformed list syntax and supported metadata shapes.

### Milestone 3 — Java and Python Template Alignment

Make the Java base template capability-neutral and remove unselected production integrations from the Python base dependency/runtime wiring. Keep local-adapter reference behavior explicit and separately documented.

### Milestone 4 — Public Repository Hygiene and Final Validation

Ignore/remove IDE, Python cache, and coverage artifacts; remove the superseded root `.ai/Plan_to_upgrade.md`; run repository validation and stack-specific checks available in the repository.

## Out of Scope

- Adding new architecture patterns or engineering standards.
- Adding new production adapters.
- Implementing the healthcare platform in this repository.
- Choosing healthcare-specific HIPAA controls without explicit healthcare-service requirements.
- Requiring Kafka, Redis, object storage, OpenTelemetry, Docker, Kubernetes, or any other mechanism universally.
- Broad dependency modernization unrelated to this consistency pass.

## Risks

- Removing preloaded dependencies may expose documentation or examples that implicitly assumed those libraries were always present.
- Tightening prompt validation must not become a general YAML parser or reject valid repository-supported prompt metadata.
- Public hygiene deletion must remove only generated/local artifacts, not intentional repository configuration.

## Success Criteria

- Service milestones describe delivery outcomes; RED/GREEN/Refactor occur inside each implementation milestone.
- Code review loads only applicable standards and can report a concrete correctness defect even when no written standard names it.
- Production-readiness review uses PASS / FAIL / NOT APPLICABLE / NEEDS VERIFICATION based on actual applicability.
- HIPAA-specific review is activated only by explicit HIPAA/PHI/health-data context rather than the generic word `compliance`.
- Malformed prompt list frontmatter is rejected by automated tests and repository validation.
- Java and Python base templates no longer install or configure unselected production capabilities by default.
- Local-only artifacts and generated cache/coverage files are not tracked.
- Repository validator and validator unit tests pass after the final patch.
