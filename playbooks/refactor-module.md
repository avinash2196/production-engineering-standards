# Workflow: Refactor Module

## Purpose

Step-by-step procedure for safely restructuring a module or component to align with enterprise-ai-engineering standards, preserving all external behavior.

## Prerequisites

- Identified module that violates standards (from codebase-analyst or code-reviewer findings)
- Existing test suite (or willingness to create one first)
- Clear refactoring goal (e.g., extract business logic from controller, introduce abstraction)

## Steps

### 1. Assess Current State

Invoke **codebase-analyst** agent (or review manually):

- What standards does this module violate?
- How tightly coupled is it to other modules?
- What is the blast radius if something breaks?
- What tests currently cover this module?

Document: current structure, violations, and target structure.

### 2. Ensure Test Coverage

**Before any refactoring:**

- Run existing tests — they must pass as-is
- If test coverage is insufficient for the refactoring scope, generate tests first using **test-engineer** agent patterns
- Tests must cover: happy paths, primary error paths, and any edge cases visible in the current implementation
- These tests become the safety net — they must not change during refactoring

### 3. Plan Incremental Steps

Break the refactoring into small, independently reviewable steps. Each step must:

- Be a single, focused change (extract class, move method, introduce interface)
- Keep all tests passing after application
- Not combine with feature changes or bug fixes

Example plan for "extract business logic from controller":
1. Create service class with empty methods matching controller logic signatures
2. Move logic from controller methods into service methods (copy, don't delete yet)
3. Update controller to delegate to service
4. Delete duplicated logic from controller
5. Add service-layer tests for extracted logic

### 4. Execute Each Step

For each planned step:

1. Make the change
2. Run all tests — must pass
3. If tests fail, fix the refactoring (not the tests)
4. Commit the step: `refactor(<module>): <what this step does>`

### 5. Introduce Abstractions (if applicable)

If the refactoring involves replacing direct SDK usage with capability abstractions:

1. Define the interface (e.g., `CacheProvider`)
2. Create an adapter wrapping the existing implementation
3. Swap the direct reference to use the interface
4. Create the fallback adapter with env toggle
5. Run tests at each sub-step

Reference: `standards/fallback-strategy.md`, relevant abstraction in `core/contracts/`

### 6. Verify Completeness

After all steps:

- [ ] All original tests pass without modification
- [ ] New tests added for extracted/restructured components
- [ ] No external behavior changed (API contracts, message schemas, DB schema)
- [ ] Module now aligns with target standards
- [ ] No orphaned code left behind

### 7. Review

Invoke **architecture-reviewer** agent on the refactored module:

- [ ] Layered architecture correct
- [ ] Dependency direction clean
- [ ] Abstraction boundaries enforced
- [ ] Naming follows domain conventions

### 8. Final Commit

If individual steps were committed, verify the full sequence. Summary commit message:

`refactor(<module>): align with enterprise standards — extract service layer, introduce CacheProvider abstraction`
