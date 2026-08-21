# File Configuration Source

## Purpose

Reference pattern for file-based configuration **when the selected framework or deployment model uses configuration files**. It is not a requirement to add layered files, a custom `ConfigSource`, or a fixed precedence chain to every service.

The canonical policy is [Configuration Management](../../configuration-management.md).

## When to Use

Configuration files are useful for values that are naturally represented by the stack's native format, such as:

- framework settings;
- structured/nested configuration;
- local-development defaults;
- non-secret timeout, pool, logging, or feature settings that are intended to be versioned.

Prefer the framework's standard mechanism. Examples include Spring Boot `application.yml` / profile files or a Python application's existing YAML/TOML/settings model.

## Structure

Use only the files and layering the project needs. For example, a Spring Boot project may use:

```text
src/main/resources/
├── application.yml
└── application-local.yml
```

A production deployment does **not** need a committed `application-production.yml` merely to satisfy this repository. Runtime/platform configuration may supply production-specific values instead.

## Precedence

When files participate in a larger configuration model, use the stack/platform's documented precedence unless the project explicitly defines another order. Record custom precedence and cover it with tests.

## Secrets

Do not commit secret values to version-controlled configuration files. Reference or resolve them through the project's approved secret-management mechanism.

## Reloading

Treat files as static unless the framework and requirements explicitly support safe reload. Do not add a dynamic configuration subsystem just to reload files.

## Example

```yaml
# application-local.yml
server:
  port: 8080
client:
  timeout: 2s
```

The example is illustrative; use names and values from actual requirements.

## LLM Instructions

- Inspect the target stack before choosing YAML, properties, TOML, or another format.
- Do not generate environment/profile files that the project does not need.
- Do not put secrets in committed files.
- Do not introduce a custom file-provider class when native configuration binding is sufficient.

## Review Checklist

- [ ] File format and location match the target stack.
- [ ] Only needed profiles/overlays exist.
- [ ] No secrets are committed.
- [ ] Precedence/reload behavior follows documented framework/project behavior.
- [ ] Configuration values are derived from requirements rather than generic defaults.
