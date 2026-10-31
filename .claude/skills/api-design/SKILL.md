---
name: api-design
description: Use when creating or changing HTTP/API contracts, DTOs, validation, errors, pagination, versioning, or compatibility.
---

# API Design

- Keep transport models explicit.
- Validate input at the boundary.
- Use stable error contracts where clients depend on them.
- Distinguish absent, null, empty, and default semantics.
- Preserve backward compatibility unless an approved plan changes it.
- Make pagination, idempotency, retryability, and concurrency semantics explicit where relevant.
- Avoid leaking persistence entities directly as public API contracts.

## Contract Completeness

An API/external contract is complete only when it answers each question below for every operation where the question applies. Tests are written directly from the contract, so an unanswered question becomes a guess in the tests.

1. **Input parsing:** response to malformed or unreadable input (a request body, message, or RPC request), and to path, query, or field values of the wrong type or format.
2. **Absent, null, empty, and blank values:** how each is treated for every input field and parameter.
3. **Read-only and unknown request fields:** whether server-assigned or derived fields, and fields the contract does not define, are rejected or ignored when supplied.
4. **Numeric semantics:** type, precision, scale, and rounding for decimal, monetary, or computed numeric values, including how derived values are calculated.
5. **Collections:** ordering of returned collections, or an explicit statement that ordering is unspecified; empty-result behavior; any limit.
6. **Matching and filtering:** exact or partial match and case sensitivity for every filter or lookup.
7. **Error responses:** the error signal per failure condition (HTTP status, close or termination code, or RPC status), the error shape, and which parts of it clients may rely on versus informative text.
8. **Identity and existence:** behavior for unknown identifiers, and how that differs from malformed identifiers, for every interface kind.
9. **Mutation semantics:** replacement versus partial update, immutable fields, and what the response returns after a change.
10. **Internal consistency:** no statement contradicts another statement, the approved requirements, or the approved Plan.
11. **Authority:** the contract governs externally observable behavior only; the approved Plan remains authoritative for scope and milestones.

Every answer must come from approved requirements, the approved Plan, or the task prompt. When none of them answers a material question, ask a focused clarification question and stop — do not choose a default on the user's behalf and do not omit the question silently. The one exception is a decision the approved requirements or Plan explicitly defer to the contract: the contract proposes a resolution, labelled `Proposed — deferred by <source>` in Decisions Resolved, and the user's contract approval accepts it. When requirements exclude a capability (for example sorting or pagination), state the externally observable consequence explicitly. Mark a question not applicable only when the API genuinely has no such behavior.

When changing an existing contract, start from the verified current contract as the baseline (`prompt-driven-development` Changed Contracts). Answers carried over unchanged from the baseline come from that baseline; only new or changed answers need a source in the current requirements, Plan, or task prompt. A change to carried-over behavior is a compatibility decision and needs explicit approval.
