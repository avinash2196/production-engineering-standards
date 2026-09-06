# Migration from the Previous Repository Structure

The previous structure exposed multiple parallel knowledge taxonomies:

```text
standards/
playbooks/
stacks/
contracts/
templates/
```

The new structure folds them into skill-owned knowledge.

| Previous concept | New home |
|---|---|
| standards | relevant `.github/skills/<skill>/` or standing instructions |
| playbooks | skill workflow or explicit `.github/prompts/` entry point |
| stacks | `java-spring-boot`, `python-fastapi`, or path instructions |
| contracts | `architecture-design/references/` |
| templates | owning skill's `templates/` |
| compliance standards | `compliance-engineering` skill |
| local adapter/fallback docs | `resilience-and-degradation` skill |
| PDD workflow/templates | `prompt-driven-development` skill |

`tooling/`, `examples/`, and minimal human-facing `docs/` remain at the root because they serve concerns that are not Copilot domain knowledge.
