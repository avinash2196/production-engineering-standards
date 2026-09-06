# Customization Model

The repository deliberately uses a small number of concepts.

The goal is to avoid creating multiple overlapping taxonomies for the same engineering knowledge.

## Instructions

Instructions contain standing rules that should be available without a task-specific decision.

Examples:

* do not commit secrets;
* do not claim tests passed unless they were executed;
* preserve approved scope;
* require human approval between PDD authorization phases;
* apply Java-specific rules to Java paths.

Repository-wide instructions belong in:

```text
.github/copilot-instructions.md
```

Path-specific rules belong in:

```text
.github/instructions/
```

Instructions should remain concise enough to be useful as persistent context.

Detailed domain knowledge should not be copied into always-on instructions.

## Skills

Skills are the primary home for reusable engineering and domain knowledge.

A skill represents a capability or area of expertise that may be needed only for particular tasks.

A skill may own:

```text
SKILL.md
references/
templates/
checklists/
examples/
scripts/
```

Examples include:

```text
architecture-design
distributed-systems
api-design
testing
resilience-and-degradation
observability
security
production-readiness
java-spring-boot
python-fastapi
oracle-to-postgres-modernization
```

This is why architecture standards, stack knowledge, playbooks, contract patterns, migration guidance, and supporting templates do not need separate top-level directories.

The skill owns the knowledge required to perform that capability.

## Agents

Agents represent durable responsibilities.

Examples:

```text
planner
test-engineer
implementation-engineer
refactoring-engineer
code-reviewer
architecture-reviewer
production-readiness-reviewer
```

Do not create a new agent simply because a technical topic is specialized.

For example:

```text
Oracle → PostgreSQL
```

is expertise used by planning, implementation, testing, and review.

It therefore belongs in a skill.

The responsibility remains with the agent performing the current phase.

A useful distinction is:

> **Agent = who is responsible for the work**
> **Skill = what expertise that responsibility needs**

## Prompts

Prompts are explicit user-invoked workflow entry points.

They are useful when a repeatable task should be easy to start deliberately.

Examples:

```text
/create-plan
/create-implementation-plan
/generate-tests
/implement-approved-plan
/refactor-code
/review-code
/migrate-oracle-to-postgres
```

Prompts should remain thin.

They should delegate:

```text
responsibility → agent
expertise → skills
persistent rules → instructions
verification → tooling/tests
```

Large bodies of engineering knowledge should not be duplicated inside prompt files.

Prompt files are a workflow convenience rather than the only source of governance.

## Tooling

Tooling sits outside `.github` because it is not prompt context.

It executes checks.

Examples:

```text
tooling/scripts/
tooling/tests/
```

This is the boundary between guidance and enforcement.

A Markdown statement that says:

```text
Every skill must contain valid frontmatter.
```

is guidance.

A repository test that fails when the frontmatter is invalid is enforcement.

The repository should avoid describing a rule as enforced unless an executable mechanism can fail on violation.

## Application-Specific Context

An adopting application should own its own:

```text
.github/copilot-instructions.md
```

That file should contain stable facts about the application itself, such as:

* runtime and framework versions;
* module or architectural boundaries;
* production database;
* migration framework;
* API compatibility expectations;
* build and verification commands;
* application-specific conventions.

It should not copy the full standards repository into the application's persistent context.

Reusable knowledge remains in externally available skills.

## PDD Artifacts

Task-specific artifacts belong to the application performing the work.

Examples:

```text
docs/.ai/Plan.md
docs/.ai/001_Implementation_Plan_RED.md
docs/.ai/002_Implementation_Plan_GREEN.md
docs/.ai/003_Implementation_Plan_REFACTOR.md
```

These artifacts represent the scope and authorization of a specific change.

They are not reusable standards and therefore do not belong inside skills.

## Examples

Skill-specific examples belong inside the relevant skill:

```text
.github/skills/<skill-name>/examples/
```

Root-level examples are reserved for real whole-project demonstrations.

A whole-project example should be:

* runnable;
* buildable;
* testable;
* representative of actual adoption;
* large enough to demonstrate interaction between instructions, agents, skills, prompts, and application-owned PDD artifacts.

Do not create placeholder example directories merely to show what folders an application might contain.

If no meaningful whole-project example exists, the repository should have no root-level `examples/` directory.

A future end-to-end example may also live in a separate GitHub repository when demonstrating external consumption of the standards repository is part of the goal.

## Docs

Docs exist for human onboarding and architecture explanation.

Examples include:

```text
getting-started.md
customization-model.md
migration-from-v1.md
```

Docs should explain how to use the repository.

They should not become another copy of the engineering knowledge already owned by skills.

A useful rule is:

```text
How to use the standards system
    → docs

The engineering knowledge itself
    → skills
```

## Surface Support

Prompt files are explicit workflow conveniences and should not be treated as the cross-surface source of truth.

Persistent governance and reusable engineering knowledge should remain in:

```text
instructions
skills
agents
tooling
```

Prompts provide convenient entry points where the current IDE or Copilot surface supports them.

## Summary

The repository uses the following model:

| Concern                      | Primitive                    |
| ---------------------------- | ---------------------------- |
| Persistent rule              | Instruction                  |
| Specialized knowledge        | Skill                        |
| Durable responsibility       | Agent                        |
| Explicit workflow entry      | Prompt                       |
| Executable validation        | Tooling                      |
| Application-specific context | Application instruction file |
| Task-specific authorization  | Application PDD artifacts    |
| Human onboarding             | Docs                         |

This keeps the repository small enough to understand while allowing individual skills to contain deep engineering knowledge when a task actually requires it.
