# Naming

Purpose
- Provide consistent, discoverable naming conventions across services, packages, classes, DTOs, and configuration keys.

Mandatory Rules
- Use domain-driven, descriptive names (e.g., `InvoiceService`, `CustomerRepository`).
- Configuration keys use dot-separated lower-case (`service.timeout.ms`).
- DTOs: suffix request/response objects with `Request`/`Response` (e.g., `CreateOrderRequest`).

Defaults
- Java package naming: reverse-domain (e.g., `com.acme.orders`).
- Python modules: snake_case; classes: PascalCase.

Anti-patterns
- Abbreviated, ambiguous names (e.g., `Srv`, `Mgr`).
- Mixing naming styles within a module or package.

LLM instructions
- When generating code, follow stack-specific naming conventions and apply suffixes for DTOs and interfaces.
- If unsure about domain vocabulary, ask a single clarifying question limited to domain term definitions.

Review checklist
- [ ] Packages/modules follow team naming conventions.
- [ ] DTOs suffixed correctly.
- [ ] Configuration keys follow dot-separated lower-case format.
