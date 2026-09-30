# API Contract

## Contract Scope

Describe only externally visible behavior authorized by approved requirements and Plan scope.

This contract governs externally observable behavior only. The approved Plan remains the single source of truth for scope, milestones, and requirement ownership.

## Out of Scope

List behaviors, endpoints, validations, integrations, or implementation details that are explicitly excluded.

## Requirement Traceability

Map each API capability to the approved requirement or Plan item that authorizes it.

| Capability | Requirement / Plan Reference |
| --- | --- |
|  |  |

## API Capabilities

For each API capability include:

### <Capability Name>

- Purpose:
- Related requirement:
- Endpoint:
- HTTP method:
- Required inputs:
- Optional inputs:
- Success status code:
- Success response body:
- Failure status codes:
- Failure response body:
- Validation rules:
- Identity / existence behavior (unknown vs malformed identifiers), where applicable:
- Mutation semantics (replacement vs partial, immutable fields), where applicable:

Do not invent fields, validations, errors, status codes, or compatibility behavior that are not authorized by approved requirements or Plan scope.

If material contract behavior is unresolved, stop and ask for clarification before finalizing this contract.

## Contract-Wide Rules

Record rules that apply to every capability, answering each applicable `api-design` Contract Completeness question once here instead of per capability:

- Input parsing and type errors:
- Absent / null / empty / blank values:
- Read-only and unknown request fields:
- Numeric semantics (precision, scale, rounding, derived values):
- Collection ordering, empty results, limits:
- Matching and filtering semantics:
- Error response shape and which parts are normative:

State "not applicable" with a reason where the API has no such behavior.

## Decisions Resolved

List every decision the Plan assigns to this contract and how it was resolved, citing the requirement, Plan item, or task-prompt decision that authorizes it.

| Decision | Resolution | Source |
| --- | --- | --- |
|  |  |  |

## Compatibility Notes

Include only compatibility requirements that are explicitly approved or repository-confirmed.

## Contract Review Status

- Status: Draft
- Human review required before implementation planning that depends on this contract.
