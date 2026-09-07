---
description: "Create or update an API/external contract from an approved Plan and requirements."
argument-hint: "approved Plan and contract scope"
agent: "planner"
tools:
  - read
  - search
  - edit
---
Apply `api-design`, `requirements-analysis`, and `prompt-driven-development`.

Read the approved requirements and Plan before defining the contract.

Create or update only the requested API/external contract artifact.

Every contract capability must be traceable to approved requirements or Plan scope.

Do not invent endpoints, fields, validations, errors, status codes, compatibility behavior, or implementation details.

If material contract behavior is unresolved, ask focused clarification questions and stop. Do not finalize the contract until the blocking questions are resolved.

Do not create production code, tests, controllers, services, repositories, database schema, or implementation plans.
