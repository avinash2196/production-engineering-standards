---
applyTo: "**/*.java,**/pom.xml,**/build.gradle,**/build.gradle.kts"
---
# Java Instructions

- Prefer constructor injection for required dependencies.
- Keep framework concerns at the application boundary; keep domain logic testable without a Spring container where practical.
- Use immutable request/response models where appropriate.
- Do not block reactive execution paths with blocking I/O.
- Bound executors and queues deliberately; do not introduce unbounded concurrency.
- Preserve transaction boundaries explicitly and avoid hidden remote calls inside database transactions.
- Add tests for changed behavior and failure paths.
- Apply the `java-spring-boot` skill for Spring-specific design and review.
