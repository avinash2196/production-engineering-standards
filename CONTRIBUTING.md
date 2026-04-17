# Contributing

Guidelines for contributing to the enterprise-ai-engineering repository.

## Getting Started

1. Fork or clone the repository.
2. Create a branch from `main` (`feature/<short-description>` or `fix/<short-description>`).
3. Make your changes following the conventions below.
4. Open a pull request against `main`.

## What Belongs Here

| Content Type | Location | Example |
|-------------|----------|---------|
| Architecture decisions | `core/` | Layer responsibilities, principles |
| Cross-cutting standards | `standards/` | Coding standards, DTO guidelines |
| Stack-specific guides | `stacks/` | Java Spring Boot integration guide |
| Agent specifications | `agents/` | Scaffolding agent spec + prompts |
| Workflow procedures | `playbooks/` | Release process, local dev setup |
| Reusable templates | `templates/` | ADR template, design doc template |
| Working examples | `examples/` | Minimal microservice demos |
| Meta-documentation | `docs/` | Glossary, overview |

## Conventions

### File Format

- All documents are **Markdown** (`.md`).
- Use ATX headings (`#`, `##`, `###`).
- One sentence per line (for clean diffs).
- Code blocks must specify a language: ` ```java `, ` ```python `, ` ```yaml `, etc.

### Standards File Structure

All files under `standards/` must follow this structure:

1. **Purpose** — one paragraph.
2. **Mandatory Rules** — numbered rules (`MUST`, `MUST NOT`).
3. **Defaults** — table of default values.
4. **Anti-patterns** — table of bad practices to avoid.
5. **LLM Instructions** — structured guidance for agents.
6. **Review Checklist** — items for PR reviewers to verify.

### Agent Spec Structure

All files under `agents/*/spec.md` must follow this structure:

1. **Purpose** — one paragraph.
2. **Capabilities** — table with capability, description, trigger.
3. **Inputs** — table with field, type, required status.
4. **Outputs** — structured report format.
5. **Guardrails** — constraints and boundaries.
6. **Tool Access** — what the agent can read/write.
7. **Invocation** — example CLI or CI commands.
8. **References** — links to related standards.

### Naming

- File names: `kebab-case.md` (e.g., `coding-standards.md`).
- Directories: `kebab-case/` (e.g., `compliance-review-agent/`).
- No spaces in file or directory names.

## Pull Request Process

1. **Title:** `[area] Brief description` (e.g., `[standards] Add caching TTL defaults`).
2. **Description:** Link to the issue or motivation. Summarize what changed.
3. **Checklist:**
   - [ ] Follows the correct file structure for its section.
   - [ ] Cross-references are valid (check relative links).
   - [ ] No broken Markdown formatting.
   - [ ] Added to the relevant README index if it's a new file.
4. **Review:** Minimum 1 approval required. Standards changes require 2 approvals.

## Issues

Use the [issue template](.github/ISSUE_TEMPLATE.md) for reporting:

- **Gaps** — missing standards, guides, or examples.
- **Corrections** — factual errors or outdated information.
- **Proposals** — new standards, agents, or workflows.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
