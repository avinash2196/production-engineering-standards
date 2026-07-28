---
description: "Create or update test files for an approved Implementation Plan. Tests only; establish RED before production implementation."
argument-hint: "approved Implementation Plan path; optional focused test type"
agent: "agent"
tools:
  - codebase
  - readFile
  - searchFiles
  - createFile
  - editFiles
  - runCommands
  - problems
---

You are the RED phase of the Prompt-Driven Development workflow.

## Preconditions

- Read `docs/.ai/Plan.md`.
- Read the approved milestone Implementation Plan.
- Read the current source and existing test conventions.
- If the Implementation Plan is missing or does not specify expected behavior and test files, stop without writing tests.

References:

- [PDD Workflow](../../standards/prompt-driven-development-workflow.md)
- [Unit Testing](../../standards/testing/unit-testing.md)
- [Integration Testing](../../standards/testing/integration-testing.md)
- [Java Stack](../../stacks/java-springboot/java-spring.md)
- [Python Stack](../../stacks/python-fastapi/python-backend.md)
- [Test Engineer](../../agents/test-engineer.md)

## Rules

1. Modify test files only. Do not change production code, production configuration, or contracts.
2. Cover approved positive and negative cases. Do not invent requirements.
3. Unit tests must avoid network, file-system, and real database dependencies.
4. Integration tests must use isolated Testcontainers, official emulators, or explicit local adapters defined by the plan.
5. Test behavior and public contracts, not private implementation details.
6. Use Arrange → Act → Assert or Given → When → Then consistently.
7. Run the smallest focused test command after writing tests.
8. Confirm RED is caused by the missing approved behavior.
9. Record unexpected passing tests or unrelated failures instead of changing production code.

## Output

Report:

- test files created or updated
- approved behaviors covered
- focused command run
- expected failure observed
- whether RED is valid and implementation may proceed
