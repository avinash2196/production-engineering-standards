# Plan: Enforceable Engineering Standards Repository Update

**Date:** 2026-07-27
**Requested by:** Update all necessary repository files while preserving the author's practical fallback experience and enforcing the workflow Plan → Implementation Plan → Implementation → Test → Code → Refactor.
**Scope:** Repository instructions, standards, prompts, playbooks, templates, validation tooling, CI, examples, and configuration templates. No application-specific business functionality is added.

## Context Gathered

- The repository already contains partial changes separating local adapters from production degradation.
- CI calls a validator filename that does not exist.
- The validator currently reports broken internal references and detects its own placeholder-pattern constants.
- The deleted generator is still referenced by documentation.
- Python settings lost infrastructure connection fields while adapter enums were introduced.
- Existing prompts mix planning and implementation and do not enforce a separate implementation-plan review gate.
- Existing test generation guidance does not explicitly require RED confirmation before production code.

## Outcomes

1. Establish one documented Prompt-Driven Development workflow.
2. Require separate Plan and Implementation Plan artifacts for qualifying implementation work.
3. Require tests to be written and confirmed RED before production code.
4. Require minimal implementation to GREEN before refactoring.
5. Preserve explicit local-adapter and production-degradation engineering decisions.
6. Add executable repository tests and CI validation.
7. Remove broken links, stale generator references, and unsupported claims.

## Steps

- [x] 1. Create the detailed implementation plan.
- [x] 2. Add validator tests before changing validator implementation.
- [x] 3. Refactor and complete repository validation tooling.
- [x] 4. Add PDD workflow standard and reusable Plan/Implementation Plan templates.
- [x] 5. Add and update Copilot prompts to separate planning, implementation planning, testing, implementation, and refactoring.
- [x] 6. Update agent specifications and playbooks to follow RED → GREEN → REFACTOR.
- [x] 7. Align README, master instructions, architecture, fallback, coding, and definition-of-done documents.
- [x] 8. Standardize Java/Python adapter configuration without removing required connection settings.
- [x] 9. Repair internal links and relabel non-runnable examples honestly.
- [x] 10. Run tests and validator, refactor issues found, and package the updated repository.

## Rollback Notes

All work is contained in the extracted repository copy. Revert modified files or discard the generated ZIP to roll back.

## Completion Evidence

- Repository validator tests were written before the completed validator and observed failing for missing behavior.
- Python provider-selection and local-storage safety tests were added before implementation and observed RED.
- The minimum validator, typed settings, local adapters, production guards, actionable adapter loading, activation warnings, and path-safety code reached GREEN.
- Documentation, composition code, and review prompts were refactored after GREEN to remove contradictions and generic absolute rules.
- Final verification commands and results are recorded in the Implementation Plan.
