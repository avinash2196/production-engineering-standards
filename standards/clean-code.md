# Clean Code

Purpose
- Enforce readable, maintainable, and testable code across stacks; minimize cognitive load for reviewers and maintainers.

Mandatory Rules
- Single responsibility per module/class; functions under ~40 lines where practical.
- Avoid hidden side-effects; methods should be explicit about state mutations.
- Document non-obvious invariants with ADRs or code comments near the declaration (not in business logic lines).

Defaults
- Favor immutability for value objects (use `final` in Java, frozen dataclasses in Python when applicable).
- Prefer small helper functions over long inline blocks.

Anti-patterns
- Large god classes, deep nested conditionals, and long parameter lists.

LLM instructions
- When refactoring, preserve public API shapes and tests, and propose small, incremental changes.
- Ask a clarifying question only if a suggested refactor might change system semantics or performance characteristics.

Review checklist
- [ ] Code adheres to single-responsibility principle.
- [ ] No god classes detected.
- [ ] Tests cover refactored behavior.
