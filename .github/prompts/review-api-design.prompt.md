---
description: "Review an API/OpenAPI contract against the repository's API principles and project-specific conventions; identify compatibility, validation, error, exposure, and security issues without inventing authentication or URI conventions."
agent: "agent"
argument-hint: "OpenAPI YAML/JSON or API contract, plus prior version/project API conventions when available"
tools:
  - codebase
  - readFile
  - searchFiles
  - problems
---

Review the supplied API contract using repository evidence and the project's established API conventions.

## References

- [API design](../../standards/api-design.md)
- [DTO guidelines](../../standards/dto-guidelines.md)
- [Coding/naming standards](../../standards/coding-standards.md)
- [Security engineering](../../standards/security/security-standards.md) when protected/sensitive resources are in scope

## Review Areas

### Contract and Resource Design

- Resource/action semantics are understandable and consistent with the existing API family.
- HTTP methods and status codes match the actual semantics.
- External versioning/compatibility strategy is explicit where the API requires one.
- Request/response schemas do not expose persistence/domain internals accidentally.

Do not force kebab-case, plural nouns, `/api/v1`, `X-Api-Version`, or “no verbs ever” unless those conventions are established by the project/standard for this API.

### Validation and Errors

- Required fields/types/bounds/formats are represented where known.
- Failure responses are structured and machine-readable according to the project's error contract.
- Error details do not leak sensitive/internal information.

Do not invent one exact JSON error schema or map every business rule to a universal status code when the project contract differs.

### Schema and Naming

- Naming is consistent with the target stack/contract and existing clients.
- Timestamps, enums, nullable/optional semantics, and descriptions are unambiguous.
- Breaking schema changes are identified.

### Security and Data Exposure

- Apply authentication/authorization only to resources established as protected.
- Explicitly public resources must not be marked defective solely for lacking authentication.
- Sensitive credentials/data are not placed in unsafe URL/query/loggable positions according to project policy.

### Compatibility (when a previous contract is available)

Flag changes that can break existing consumers, including removal/renaming, new required input, incompatible type/enum/semantic changes, response/status changes, or security-scheme changes. Distinguish definitely breaking changes from changes that need consumer evidence.

## Output

```markdown
## API Design Review: <scope>

### Verdict
PASS / NEEDS CHANGES / NEEDS VERIFICATION

### Findings
| # | Severity | Location | Evidence / Rule | Finding | Remediation |
|---|---|---|---|---|---|

### Compatibility Changes
- <breaking / potentially breaking / none identified>

### Open Decisions
- <only material unresolved contract decisions>

### Strengths
- <evidence-based positives>
```
