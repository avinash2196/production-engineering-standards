# Local Standards Template

## Purpose

Define local-development constraints that complement central standards without creating production requirements.

## Local Toolchain

- Runtime(s): <versions>
- Formatter/linter: <commands>
- Test command: <command>

## Local Dependency Strategy

For each external capability needed locally, document the selected approach and why it is appropriate:

| Capability | Local approach | Selection/config | Reduced guarantees |
|---|---|---|---|
| <messaging/cache/storage/etc.> | <container/emulator/fake/local adapter> | <setting> | <differences> |

Do not create a local adapter merely because the standards repository contains one.

## Local Configuration

Document the convention actually used by the stack/project. Examples include Spring `application-local.yml`, `.env.local`, or another project-defined settings source. Local files containing credentials must be ignored by version control and excluded from production artifacts.

## Validation

List the real local commands developers should run before committing, for example:

```text
<unit-test command>
<integration-test command when applicable>
<repository validation command when available>
```
