# Customization Model

The repository deliberately uses a small number of concepts.

## Instructions

Standing rules that should be available without a task-specific decision. Keep them short enough to remain useful as persistent context.

## Skills

Skills are the primary home for reusable engineering knowledge.

A skill may own:
- `SKILL.md`
- references
- templates
- checklists
- examples
- small helper scripts

This is why architecture standards, stack knowledge, playbooks, contract patterns, and migration guidance no longer need separate top-level directories.

## Agents

Agents represent durable responsibilities such as planning, testing, implementation, refactoring, code review, and architecture review.

Do not create an agent just because a topic is specialized. For example, Oracle → PostgreSQL is expertise used by several agents, so it is a skill.

## Prompts

Prompts are explicit user-invoked workflow entry points. They should delegate responsibility to an agent and domain knowledge to skills rather than duplicating large bodies of guidance.

## Tooling

Tooling is outside `.github` because it is not prompt context. It executes checks. This is the boundary between guidance and enforcement.

## Examples

Root examples are whole-project demonstrations only. Skill-specific examples belong with the skill.

## Docs

Docs exist for human onboarding and architecture explanation. Domain knowledge belongs in skills instead of being duplicated here.


## Surface Support

Prompt files are an explicit local-workflow convenience and are not the cross-surface source of truth. Current VS Code documentation notes that Agent Host does not consume prompt files. Therefore, governance and reusable domain knowledge must remain in instructions, skills, agents, and executable validation rather than existing only in prompts.

Skills are the durable cross-surface capability layer; prompts are optional entry points where the IDE supports them.
