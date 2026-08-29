# Implementation Plan — Agent Activation and Portability Hardening

## Status

Completed — owner-approved publication hardening on 2026-08-29.

## Milestone Description

Harden the existing GitHub Copilot custom-agent and Agent Skill model for public reuse without changing the repository's engineering architecture, PDD lifecycle, Java/Python guidance, or standards content.

The approved scope is limited to naming consistency, explicit agent activation behavior, portable internal references, external-use documentation, and regression checks.

## Files Updated

- `.github/agents/*.agent.md`
- `.github/prompts/implement-approved-plan.prompt.md`
- `.github/prompts/maintenance-check.prompt.md`
- `.github/skills/code-review/SKILL.md`
- `README.md`
- `docs/copilot-customizations.md`
- `tooling/tests/test_copilot_customization_semantics.py`
- historical `.ai` references affected by the final agent names

## Naming Convergence

Use responsibility-oriented names that match the executable filenames and frontmatter:

- `backend-service-builder` → `backend-service-engineer`
- `lifecycle-reviewer` → `maintenance-reviewer`

Update prompt bindings and documentation so there is one canonical name for each agent. No additional agent hierarchy is introduced.

## Activation Contract

Add an `## On Activation` section to every custom agent. This is Markdown operating guidance, not a non-standard YAML field. Each agent must, as appropriate:

1. identify the requested scope/phase;
2. inspect adopting-project evidence before applying standards;
3. determine relevant stack/risk/applicability;
4. use relevant skills when available without assuming skill discovery;
5. verify required approvals/evidence;
6. stop or report missing evidence instead of inventing decisions;
7. remain inside the agent's tool and responsibility boundary.

## Portability Contract

- Do not store developer-specific absolute paths in agent or skill definitions.
- Use definition-file-relative Markdown links for resources that live in this standards repository.
- Clearly label paths such as `docs/.ai/Plan.md` as adopting-project paths rather than standards-repository resources.
- External IDE/user configuration may point to a local checkout, but that machine-specific location must stay outside source control.
- When using external/personal customizations, agents and skills must both be registered/discoverable; agent discovery alone does not imply skill discovery.
- A Git submodule remains optional and is only needed when a consuming project intentionally wants the full standards repository in its workspace and pinned by Git.

## Verification

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tooling/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python tooling/scripts/validate_repository.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=stacks/python-fastapi/project-template \
  python -m unittest discover \
  -s stacks/python-fastapi/project-template/tests \
  -p 'test_*.py'
```

Additional semantic checks verify:

- every active custom agent has `## On Activation`;
- agent names match filenames through repository validation;
- renamed prompt bindings resolve;
- agent/skill definitions contain no machine-specific absolute paths;
- internal Markdown links continue to resolve.

## Out of Scope

- Adding new agents or Agent Skills.
- Converting the repository to an Agent Plugin.
- Requiring a submodule in consuming applications.
- Requiring a consuming application to add `.github/copilot-instructions.md`.
- Duplicating the full standards library inside each skill.
- Changing production engineering standards or stack implementation guidance.

## Success Criteria

- Existing repository structure is preserved.
- Canonical agent names are consistent across filenames, frontmatter, prompts, tests, and documentation.
- Agent startup behavior is explicit and responsibility-bounded.
- Standards-repository internal links are portable across checkout locations.
- The repository can be packaged without Git metadata, IDE state, bytecode, or test caches.
- Repository and starter validation pass.
