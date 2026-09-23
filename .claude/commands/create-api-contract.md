---
description: "Create or update an API/external contract from an approved Plan and requirements."
---

Act as an API designer and create or update the requested API/external contract.

Apply `api-design`, `requirements-analysis`, and `prompt-driven-development`.

Read the approved requirements and Plan before defining the contract.

This command executes the CONTRACT milestone recorded in the approved `Plan.md`. If the Plan records no CONTRACT milestone, or its predecessor is not satisfied, stop and surface that for human review. Resolve every decision the Plan assigns to the CONTRACT milestone; do not add scope the Plan does not assign.

Every contract capability must be traceable to approved requirements or Plan scope.

Do not invent endpoints, fields, validations, errors, status codes, compatibility behavior, or implementation details.

If material contract behavior is unresolved, ask focused clarification questions and stop. Do not finalize the contract until the blocking questions are resolved.

Do not create production code, tests, controllers, services, repositories, database schema, or implementation plans.

Do not approve the contract yourself.
