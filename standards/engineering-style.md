# Engineering Style

## Purpose

Keep code understandable, cohesive, testable, and consistent with the target stack without forcing every service into one layer count or abstraction pattern.

## Principles

- Organize code around coherent responsibilities and dependency boundaries.
- Keep transport/framework/vendor details out of business decisions when that separation creates real value.
- Prefer domain-specific names over generic `manager/helper/data` terminology.
- Use typed configuration through the stack's established mechanism; avoid scattered ad-hoc reads when central binding materially improves correctness.
- Make state mutation, transactions, concurrency, retries, and external side effects explicit.
- Keep business behavior changes separate from broad refactoring whenever practical.
- Prefer the formatter/linter/testing conventions already adopted by the project.

A controller/service/domain/repository hierarchy is one common pattern, not a universal required package structure. Simple services may use fewer layers; complex domains may need richer boundaries.

## Testing

Choose unit, integration, contract/schema, end-to-end, load, and security checks according to actual risk and boundary behavior. Testcontainers, emulators, local adapters, mocks, and ephemeral environments are options—not universal requirements.

## LLM Instructions

- Inspect existing project conventions before creating packages/layers.
- Add abstractions only for a clear responsibility, testing, portability, or policy boundary.
- Avoid speculative cleanup outside the approved milestone.

## Review Checklist

- [ ] Responsibilities and dependency directions are understandable.
- [ ] New layers/abstractions have a concrete reason.
- [ ] Side effects/failure behavior are explicit where material.
- [ ] Tests/checks match the actual behavior and risk.
