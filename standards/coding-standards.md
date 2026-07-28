# Coding Standards

## Purpose

Provide consistent, readable defaults while avoiding brittle numeric rules that reward superficial compliance.

## Naming

| Element | Java | Python | Example |
|---|---|---|---|
| Types | PascalCase | PascalCase | `OrderService` |
| Methods/functions | camelCase | snake_case | `createOrder`, `create_order` |
| Variables | camelCase | snake_case | `orderId`, `order_id` |
| Constants | UPPER_SNAKE_CASE | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Database columns | snake_case | snake_case | `created_at` |
| REST resource paths | kebab-case nouns | kebab-case nouns | `/api/v1/order-items` |
| Environment variables | UPPER_SNAKE_CASE | UPPER_SNAKE_CASE | `MESSAGING_ADAPTER` |

Names must reflect domain intent. Avoid vague terms such as `data`, `info`, `manager`, or `helper` when a precise name exists.

## Focused Methods

### Default

A method should represent one coherent responsibility and one level of abstraction.

### Review Signals

Review methods that:

- exceed roughly 30–40 lines
- contain multiple unrelated branches or side effects
- mix transport, business, persistence, and provider logic
- are difficult to test without extensive setup

A threshold is not an automatic failure. Cohesive parsing, mapping, transaction orchestration, or performance-sensitive algorithms may be clearer when kept together.

## Focused Classes and Modules

Review classes/modules that:

- exceed roughly 300 lines
- own multiple unrelated reasons to change
- inject many dependencies with no cohesive use case
- combine API, business, persistence, and infrastructure concerns

Split only when the extracted responsibility has a meaningful name and boundary. Do not fragment cohesive behavior into tiny indirections.

## Parameters

More than four parameters is a review signal, not an automatic violation. Use a value object or request object when parameters form a coherent concept. Do not hide unrelated dependencies inside a generic context object.

## Control Flow

- use guard clauses when they make preconditions clear
- avoid deep nesting when named operations improve readability
- do not extract trivial methods that obscure a straightforward algorithm
- make concurrency, transaction, and retry behavior explicit

## Error Handling

- use domain/application-specific exceptions where callers need distinct handling
- translate exceptions at transport boundaries
- do not swallow failures
- preserve root cause when wrapping
- avoid retrying validation, authorization, or other non-transient failures

## Comments and Documentation

- comments explain **why**, trade-offs, or non-obvious constraints
- remove commented-out code
- TODOs include an issue/ticket reference when used in production code
- public contracts document behavior, errors, and important guarantees

## Imports and Dependencies

- no wildcard imports
- remove unused dependencies and imports
- group imports according to stack tooling
- avoid direct vendor SDK imports in application/domain code when a capability boundary is required

## Formatting and Tooling

Prefer the formatter and linter already configured by the project. Repository defaults:

- Java: formatter + Checkstyle/SpotBugs or equivalent project tools
- Python: Ruff formatting/linting and mypy where configured

Do not create large formatting-only diffs during feature implementation.

## LLM Instructions

- Treat line, parameter, and class-size numbers as review signals.
- Explain the concrete readability, cohesion, maintenance, or testability problem before proposing extraction.
- Prefer domain-specific names and exceptions.
- Do not add speculative abstractions or fragment cohesive logic to satisfy a metric.
- Keep refactoring separate from behavior changes.

## Review Checklist

- [ ] Names express domain intent
- [ ] Methods and classes are cohesive
- [ ] Numeric thresholds were used as signals, not automatic failures
- [ ] Transport, business, persistence, and provider concerns are not mixed without rationale
- [ ] Error handling preserves useful context
- [ ] Comments explain non-obvious reasoning
- [ ] No unrelated formatting or cleanup expanded the change

## References

- [Architecture](architecture.md)
- [DTO Guidelines](dto-guidelines.md)
- [Java Stack](../stacks/java-springboot/java-spring.md)
- [Python Stack](../stacks/python-fastapi/python-backend.md)
