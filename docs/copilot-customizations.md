# GitHub Copilot Customization Model

This repository uses GitHub Copilot customization mechanisms in their native repository locations. Engineering standards remain ordinary versioned documents; Copilot customizations decide when and how those standards are applied.

## Customization Types

| Mechanism | Repository location | Trigger | Use in this repository |
|---|---|---|---|
| Repository instructions | `.github/copilot-instructions.md` | Automatic | Stable workflow, anti-invention, architecture, safety, and evidence rules |
| Path-specific instructions | `.github/instructions/*.instructions.md` | Automatic when the path matches | Language, stack, or file-path guidance only |
| Prompt files | `.github/prompts/*.prompt.md` | Manual | Repeatable single tasks such as planning, RED tests, reviews, and refactoring |
| Custom agents | `.github/agents/*.agent.md` | Manually selected in supported Copilot surfaces | Specialized roles with scoped behavior and tool access |
| Agent Skills | `.github/skills/<skill-name>/SKILL.md` | Loaded by Copilot when relevant | Detailed reusable capabilities such as requirements analysis and code review |

## Custom Agents

Custom agents are native GitHub Copilot agent profiles. Each profile in `.github/agents/` uses YAML frontmatter with at least a `description`, followed by Markdown instructions.

This repository uses the `.agent.md` suffix because it is explicit in VS Code while remaining compatible with GitHub's custom-agent model.

The current agents are:

- `architecture-reviewer`
- `backend-service-engineer`
- `code-reviewer`
- `codebase-analyst`
- `compliance-reviewer`
- `distributed-systems-reviewer`
- `hipaa-reviewer`
- `maintenance-reviewer`
- `production-readiness-reviewer`
- `refactoring-engineer`
- `test-engineer`

Repository agents are configured for manual invocation (`disable-model-invocation: true`) so a specialized role is not silently selected by the cloud agent. Human review gates in the PDD workflow still apply.

Read-only/review agents receive read/search/execute capabilities. Agents that intentionally change tests or implementation receive edit access as well. A profile must not claim access to an external registry, vulnerability database, CI system, or MCP tool unless that capability is actually configured.


## Activation and Portability Contract

Every custom agent contains an `On Activation` section in its Markdown body. This is a repository convention, not a custom YAML property. It makes startup behavior explicit: identify scope, inspect evidence, apply only relevant standards, verify prerequisites, and stop or report missing evidence before crossing the agent's responsibility boundary.

This repository is designed to remain portable across developer machines:

- Agent and skill definitions must not contain developer-specific absolute filesystem paths.
- Links from an agent or skill to files in this standards repository use paths relative to the definition file.
- Paths such as the adopting project's `docs/.ai/Plan.md` are intentionally project-relative and are labeled as adopting-project artifacts.
- When these customizations are registered outside an application repository, configure the supported IDE/Copilot surface to discover **both** `.github/agents/` and `.github/skills/`. Discovering an agent directory does not by itself guarantee that a separate skill directory is discoverable.
- Keep machine-specific checkout locations in user/personal IDE configuration, not in this repository. JetBrains IDEs expose workspace and personal customizations through the Agent Customizations editor; VS Code also supports user-level agents/skills and additional discovery locations.

A submodule is therefore optional rather than required. Use one only when an application intentionally needs the complete standards repository inside its workspace and wants Git to pin the standards revision.

## Agent Skills

Agent Skills are not agent personas. They are task-specific instruction bundles that Copilot can load when the skill description matches the current work.

Each project skill lives in:

```text
.github/skills/<skill-name>/SKILL.md
```

The `SKILL.md` file contains YAML frontmatter with a lowercase hyphenated `name` and a `description` explaining both what the skill does and when to use it.

Current skills:

- `requirements-analysis` — guards the Requirements → Plan boundary and prevents missing information from being invented.
- `code-review` — provides evidence-based production code-review behavior when relevant.

Skills may reference standards, scripts, examples, or other resources, but they should remain useful without requiring a user to manually select a custom agent.

## Prompt Files

Prompt files are explicit reusable tasks stored under `.github/prompts/`. In current VS Code they are invoked manually in local extension-host chat sessions; VS Code Agent Host sessions do not consume prompt files. Workflows that must also work through Copilot cloud agent, CLI, or other agent surfaces therefore rely on repository instructions, Agent Skills, custom agents, and ordinary standards rather than assuming prompt-file availability.

When a prompt has a matching specialist custom agent, this repository binds the prompt to that agent by name and lets the agent profile own its tool boundary. Other prompts use current VS Code tool-set aliases such as `read`, `search`, `edit`, and `execute`.

## What Is Not Used

The repository intentionally does **not** use a top-level `agents/` directory or an `agents/<name>/spec.md` convention as an executable Copilot mechanism. Those were repository-local conventions and are not needed now that the same responsibilities are represented by native custom-agent profiles, prompt files, skills, standards, and playbooks.

Do not reintroduce a second agent-specification hierarchy outside `.github/agents/`.

## Validation

`tooling/scripts/validate_repository.py` validates repository customizations that can be checked deterministically, including:

- required customization directories;
- prompt frontmatter, custom-agent references, and legacy tool identifiers;
- path-specific instruction frontmatter and repository-wide `applyTo` misuse;
- custom-agent profile naming/frontmatter/tool-list structure;
- Agent Skill directory/name/frontmatter structure;
- internal Markdown links and selected literal customization references.

The validator checks structure, not whether Copilot will make a correct engineering decision. Context-sensitive behavior remains subject to human review.

## References

- [GitHub Copilot customization cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)
- [GitHub custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [Adding Agent Skills for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
