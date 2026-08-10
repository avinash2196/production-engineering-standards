# Workflow: Add a New Endpoint

## Purpose

Add an API endpoint through approved requirements and small PDD milestones so tests, implementation, and optional refactoring remain independently reviewable.

## 1. Review Requirements and Current State

Read:

- `docs/.ai/Plan.md` or source requirement
- existing OpenAPI/API conventions
- related controllers, DTOs, services, domain behavior, repositories, and tests
- authorization/data-classification requirements when applicable

Clarify only material gaps such as validation, success/error behavior, status codes, idempotency, or authorization. Do not invent behavior.

## 2. Update and Review the Plan

Represent behavior-changing endpoint work as separate milestones, for example:

1. Endpoint Contract/Controller Tests — RED
2. Endpoint Minimal Implementation — GREEN
3. Endpoint Refactor — REFACTOR only when justified

If domain/application or persistence behavior is substantial enough to benefit from smaller control boundaries, split it into additional RED/GREEN pairs rather than creating one oversized endpoint milestone.

Each milestone must state its phase, outcome, predecessor, and explicit exclusions. Obtain Plan approval.

## 3. Create the RED Implementation Plan

Create:

```text
docs/.ai/NNN_Implementation_Plan_<Endpoint>_Tests.md
```

Define only:

- exact controller/contract/application/integration test files required by this RED milestone
- approved request/response behavior, validation, error behavior, and authorization cases
- persistence/adapter cases only when required by this milestone
- focused command
- expected RED failures and why they prove the endpoint behavior is missing
- out-of-scope work

Obtain approval, then execute with `/generate-tests`. Confirm valid RED and stop.

## 4. Create the GREEN Implementation Plan

After RED evidence exists, create a separate GREEN Implementation Plan defining only:

- predecessor RED evidence
- exact transport DTO/controller/handler changes
- exact application/domain operation changes
- repository/capability interaction only when required
- approved error mapping, transaction, idempotency, authorization, and observability behavior
- focused and regression commands
- out-of-scope work

Obtain approval, then execute with `/implement-approved-plan`.

Implement only enough approved production behavior to reach GREEN. Do not add unrelated fields, endpoints, infrastructure, tests, or cleanup. Stop after GREEN.

## 5. Optional REFACTOR Milestone

Create a separate REFACTOR milestone only when there is a concrete cleanup/design reason such as duplicated mapping, poor naming, mixed responsibility, or a justified extraction.

Its Implementation Plan must name the verified GREEN baseline, exact structural changes, behavior/contracts that remain unchanged, and before/after test commands.

Execute with `/refactor-code` only after approval.

## 6. Review

- [ ] Contract matches approved requirement
- [ ] RED and GREEN were separate milestones with separate approved Implementation Plans
- [ ] RED evidence is valid and predates GREEN implementation
- [ ] DTO/domain/persistence boundaries are appropriate to service complexity
- [ ] Controller/handler contains no unapproved business policy
- [ ] Authorization and validation are enforced at approved boundaries
- [ ] Transaction/idempotency behavior is explicit where relevant
- [ ] Any REFACTOR milestone was separate and preserved behavior
- [ ] Existing API behavior remains compatible unless an approved breaking change exists
