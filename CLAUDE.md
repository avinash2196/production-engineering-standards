# Repository-Wide Claude Code Instructions

This repository provides production-engineering customizations. Apply these rules unless a more specific path instruction narrows them.

## Control Boundaries

- Do not invent requirements, non-functional requirements, business rules, validation rules, or architecture decisions when material behavior is unclear.
- Do not mark a Plan, API/external contract, or Implementation Plan approved on behalf of a human reviewer.
- Do not claim tests, commands, validators, migrations, builds, or deployments passed unless they were actually executed or evidence was supplied.
- Keep behavior-changing RED, GREEN, and optional REFACTOR phases separate when the adopting project uses the PDD workflow.
- Prefer the smallest safe change that satisfies the approved scope.
- Preserve public contracts unless an approved plan explicitly changes them.
- Do not pull future milestone work into the current task.
- Do not rewrite approved project artifacts merely to make them match an implementation.
<!-- PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL:START -->
- Every code change must be traceable to a human-approved, phase-specific Implementation Plan — this applies regardless of which command, prompt, or free-form request produced the change. Do not modify production source, tests, configuration, dependencies, schemas, migrations, scripts, or other executable repository artifacts from a free-form request, review finding, failing test, or inferred fix alone.
- If no approved Implementation Plan authorizes the requested change, do not implement it; route the work through the appropriate PDD planning and human-review boundary first.
- The size and detail of an Implementation Plan should be proportional to the change — small changes may use a very small Implementation Plan, but they do not bypass human approval. This applies to all code changes, not only behavior-changing ones.
- Documentation-only changes clearly outside executable/code artifacts may follow the project's normal documentation workflow; do not invent exceptions to the above for source, tests, configuration, dependencies, or other executable artifacts.
<!-- PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL:END -->

## Clarification Before Action

Do not invent, assume, or silently resolve material information that is not explicitly provided by the user, established by an approved project artifact, or confirmed by repository evidence.

Before creating or modifying an artifact:

1. Read the declared inputs and relevant approved artifacts.
2. Identify missing, ambiguous, contradictory, or materially incomplete information.
3. Determine whether the unresolved information affects the correctness or scope of the current task.
4. If it does, ask the minimum focused clarification questions required.
5. Stop and wait for the user's response before creating or updating the requested artifact.

Do not:

- choose between material alternatives on the user's behalf;
- convert material ambiguity into a default or assumption;
- place a material ambiguity only in an Open Questions section and continue;
- treat a technically reasonable default as authorization to proceed.

Non-blocking decisions may remain explicitly unresolved when they do not affect the correctness or scope of the current task.

When clarification is required, this rule takes precedence over instructions to create a file, update milestone status, or return a completion message.

## Engineering Baseline

- Treat correctness, data integrity, security, observability, and operability as design concerns, not post-processing.
- Prefer explicit dependency boundaries and dependency injection.
- Never log secrets, tokens, credentials, or sensitive payloads without an approved reason and protection.
- Handle errors deliberately; do not silently swallow failures.
- Add or update tests for approved behavior changes.
- Make degraded behavior explicit, observable, testable, and unable to activate silently when degradation is part of the approved scope.
- Separate local-development adapters from production degradation strategies.
- Use idempotency where approved behavior may be retried or duplicate delivery can repeat side effects.
- Document material trade-offs instead of presenting one architecture choice as universally correct.

Engineering guidance is a review and design lens, not authorization to expand approved scope.

Do not introduce security features, observability, resilience mechanisms, dependencies, infrastructure, performance work, or other non-functional requirements unless they are required by approved scope or necessary to implement an already-approved requirement correctly.

If such a concern materially affects correctness but is unresolved, surface it for clarification rather than silently expanding the milestone.

## Skills

Use a skill when specialized knowledge is relevant. Do not load every skill for every task.

Examples:

- requirements review or planning → requirements-analysis
- PDD workflow → prompt-driven-development
- architecture/distributed-system work → architecture-design and distributed-systems
- Spring Boot work → java-spring-boot
- API changes → api-design
- failure handling → resilience-and-degradation
- Oracle → PostgreSQL modernization → oracle-to-postgres-modernization

## Human Review

Human review remains required for requirement interpretation, Plan approval, API/external contract approval, Implementation Plan approval, architecture trade-offs, production-readiness decisions, and exceptions.

A completed phase does not authorize the next phase unless the workflow explicitly says so.

## Java Files

**Applies to:** `**/*.java`, `**/pom.xml`, `**/build.gradle`, `**/build.gradle.kts`

- Prefer constructor injection for required dependencies.
- Keep framework concerns at the application boundary; keep domain logic testable without a Spring container where practical.
- Use immutable request/response models where appropriate.
- Do not block reactive execution paths with blocking I/O.
- Bound executors and queues deliberately; do not introduce unbounded concurrency.
- Preserve transaction boundaries explicitly and avoid hidden remote calls inside database transactions.
- Add tests for changed behavior and failure paths.
- Apply the `java-spring-boot` skill for Spring-specific design and review.

## Python Files

**Applies to:** `**/*.py`, `**/pyproject.toml`, `**/requirements*.txt`

- Prefer explicit types at public boundaries.
- Separate transport/framework code from domain behavior.
- Do not perform blocking I/O on an async event loop.
- Validate external input at the boundary.
- Keep dependency sets minimal and pinned through the adopting project's approved process.
- Add tests for changed behavior and failure paths.
- Apply the `python-fastapi` skill for FastAPI-specific design and review.

## SQL and Migration Files

**Applies to:** `**/*.sql`, `**/db/**`, `**/migrations/**`

- Treat schema changes as production changes with rollback/recovery considerations.
- Make data-type, nullability, default, sequence/identity, index, and constraint behavior explicit.
- Do not assume Oracle and PostgreSQL semantics are equivalent.
- Verify generated SQL and ORM behavior against the target database.
- For Oracle → PostgreSQL work, apply the `oracle-to-postgres-modernization` skill.
