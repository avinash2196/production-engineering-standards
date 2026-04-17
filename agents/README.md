# Agents

Specifications and prompts for Copilot-style agents used for scaffolding, compliance reviews, and lifecycle tasks.

## Overview

Agents are LLM-driven automation units that perform recurring engineering tasks by referencing this repository's standards, abstractions, and templates. Each agent has:

- **`spec.md`** — Purpose, capabilities, inputs/outputs, guardrails, and tool access.
- **`prompts/`** — Reusable prompt templates the agent consumes.

## Available Agents

| Agent | Purpose | Trigger |
|-------|---------|--------|
| [Scaffolding Agent](scaffolding-agent/spec.md) | Generate new services from templates with correct abstractions | New project request |
| [Compliance Review Agent](compliance-review-agent/spec.md) | Audit architecture artifacts against HIPAA and security checklists | PR review, pre-launch |
| [Lifecycle Agent](lifecycle-agent/spec.md) | Dependency updates, observability gaps, deprecation scanning | Scheduled / on-demand |

## Agent Design Principles

1. **Standards-grounded:** Every agent references this repo's standards as its source of truth.
2. **Deterministic outputs:** Agents produce structured outputs (checklists, scaffolds, reports) not open-ended prose.
3. **Human-in-the-loop:** Agents propose changes; humans approve and merge.
4. **Auditable:** All agent actions are logged with inputs, outputs, and the standards version referenced.
5. **Composable:** Agents can call each other (e.g., scaffolding agent invokes compliance review on the generated code).

## Creating a New Agent

1. Create a directory under `agents/{agent-name}/`.
2. Write `spec.md` following the template structure (see existing specs).
3. Add prompt templates under `prompts/`.
4. Register the agent in this README.
5. Test the agent against at least 3 representative scenarios.

## References

- [Core principles](../core/principles.md)
- [Workflow: compliance review](../workflows/compliance-review/procedure.md)
