# Workflow: Add a New Endpoint

## Purpose

Add an API endpoint through an approved contract and a test-first milestone without mixing unrelated implementation or refactoring.

## 1. Review Requirements and Current State

Read:

- `docs/.ai/Plan.md` or source requirement
- existing OpenAPI/API conventions
- related controllers, DTOs, services, domain behavior, repositories, and tests
- authorization and data-classification requirements

Clarify only material gaps such as validation, status codes, idempotency, or authorization. Do not invent behavior.

## 2. Update and Review the Plan

Add the endpoint milestone to `docs/.ai/Plan.md` with:

- resource and business outcome
- supported operation
- validation and business rules
- success and error behavior
- explicit exclusions

Obtain approval.

## 3. Create the Endpoint Implementation Plan

Create:

```text
docs/.ai/NNN_Implementation_Plan_<Endpoint>.md
```

Define exact changes for:

- request/response or event contracts
- controller/API tests
- application/domain tests
- persistence/adapter tests only if required
- expected RED failures
- minimal controller, service, domain, and repository changes
- authorization, transaction, idempotency, error mapping, and observability decisions
- refactoring allowed after GREEN

Obtain approval before editing tests or production source.

## 4. RED — Write Tests First

Recommended order:

1. contract/controller tests for validation, mapping, status codes, and authorization
2. application/domain tests for positive and negative business behavior
3. integration tests only for new persistence or adapter behavior

Run the smallest relevant command. Confirm the failure is caused by the missing endpoint behavior, not invalid setup.

## 5. GREEN — Minimal Implementation

Implement only what the approved tests require:

- transport DTOs and validation
- thin controller/handler
- application/domain operation
- repository or capability interaction when required
- explicit error mapping

Do not add unrelated fields, endpoints, infrastructure, or cleanup.

Run focused tests and relevant regression tests.

## 6. REFACTOR

After GREEN:

- improve names and mapping boundaries
- remove duplication
- extract cohesive validation or domain concepts
- preserve API, status codes, error payloads, and persistence behavior

Run tests after each meaningful refactor.

## 7. Review

- [ ] Contract matches approved requirement
- [ ] DTOs are separate from domain/persistence models where appropriate
- [ ] Controller/handler contains no business policy
- [ ] Authorization and validation are enforced at correct boundaries
- [ ] Transaction/idempotency behavior is explicit where relevant
- [ ] RED → GREEN → REFACTOR evidence is recorded
- [ ] Existing API behavior remains compatible unless an approved breaking change exists
