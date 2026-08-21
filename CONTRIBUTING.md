# Contributing

Guidelines for contributing to the Production Engineering Standards repository.

## Getting Started

1. Fork or clone the repository.
2. Create a branch from `main` (`feature/<short-description>` or `fix/<short-description>`).
3. Make the smallest change that addresses the identified gap or correction.
4. Run repository validation before opening a pull request.
5. Open a pull request against `main`.

## What Belongs Here

| Content type | Location | Examples |
|---|---|---|
| Engineering standards | `standards/` | Architecture, reliability, testing, security |
| Repository decisions | `docs/decisions/` | ADRs about this standards repository |
| Stack-specific guidance | `stacks/` | Java/Spring Boot and Python/FastAPI guidance |
| GitHub Copilot custom agents | `.github/agents/` | Specialist review and implementation roles |
| Agent Skills | `.github/skills/` | Task-specific reusable capabilities |
| Prompt files | `.github/prompts/` | Reusable explicit workflows |
| Workflow procedures | `playbooks/` | Local development, review, release |
| Reusable templates | `templates/` | Plan, Implementation Plan, ADR, infrastructure docs |
| Reference examples | `examples/` | Architecture and behavior walkthroughs |
| Meta-documentation | `docs/` | Overview, glossary, enforcement matrix |

## Conventions

### File Format

- Use Markdown for standards, playbooks, Copilot customizations, and repository documentation.
- Use ATX headings (`#`, `##`, `###`).
- Prefer one sentence per line where it improves diffs and reviewability.
- Code blocks should specify a language when one applies.
- File and directory names use `kebab-case` unless a tool or framework requires another convention.

### Standards Content

Standards should state their purpose, normative rules or decision guidance, LLM guidance where applicable, and review criteria. Use defaults and anti-pattern sections only when they add useful information. Do not invent universal numeric thresholds where the correct value depends on service requirements, workload, risk, or operating context.

### Copilot Customizations

Custom agents belong in `.github/agents/` and use the `.agent.md` suffix with valid YAML frontmatter. Agent Skills belong in `.github/skills/<skill-name>/SKILL.md` and must use a lowercase hyphenated name matching the directory. Prompt files belong in `.github/prompts/`. Do not create a second top-level `agents/` specification hierarchy. See [Copilot Customization Model](docs/copilot-customizations.md).

### Evidence and Claims

- Describe a rule as **enforced** only when an executable mechanism blocks the violation.
- Do not claim tests, validators, builds, scans, or reviews passed unless they were actually run.
- Compliance-oriented material must distinguish engineering guidance from legal certification and must not turn organization-specific choices into universal regulatory requirements.

## Pull Request Process

1. **Title:** use an area prefix when useful, for example `[standards] Clarify cache degradation guidance`.
2. **Description:** explain the motivation, what changed, and whether enforcement behavior changed.
3. **Checklist:**
   - [ ] Relative links are valid.
   - [ ] No placeholder implementation or stale terminology was introduced.
   - [ ] Relevant tests/validators were run and results are reported accurately.
   - [ ] New standards or files are linked from the appropriate index/documentation when needed.
4. **Review:** contributions from others should receive maintainer review before merge. For solo maintenance, run repository validation and complete a documented self-review. Standards changes should explain their rationale and any change in enforcement behavior.

## Validation

```bash
python -m unittest discover -s tooling/tests -p 'test_*.py'
python tooling/scripts/validate_repository.py
PYTHONPATH=stacks/python-fastapi/project-template \
  python -m unittest discover \
  -s stacks/python-fastapi/project-template/tests \
  -p 'test_*.py'
```

## Issues

Use the [issue template](.github/ISSUE_TEMPLATE.md) for gaps, corrections, and proposals.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
