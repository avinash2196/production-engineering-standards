# Integration Dependencies Template

Purpose
- Document external systems, required versions, and acceptable fallback behaviors for integration tests and production.

Placeholders
- Dependency: <NAME>
- Purpose: <what it's used for>
- Required version: <semver or range>
- Production SLA: <durability/availability requirements>

Fallback behavior
- Describe local fallback and its limitations (ordering, durability, consistency).

Config source
- Config keys and provider where connection strings and credentials are read (operator overrides, dynamic config, env).

Infra dependencies
- Include connection ports, schema/migration requirements, and any prerequisites.

Validation
- Integration tests or Testcontainers definitions to validate compatibility.
