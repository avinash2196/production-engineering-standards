---
name: java-spring-boot
description: Use for Java/Spring Boot design, implementation, review, testing, transactions, persistence, concurrency, and production configuration.
---

# Java / Spring Boot

- Prefer constructor injection.
- Keep business logic independent of Spring where practical.
- Make transaction boundaries explicit.
- Avoid remote calls inside long database transactions.
- Understand proxy-based behavior for transactions, async execution, and caching.
- Bound thread pools/queues and propagate cancellation/timeouts deliberately.
- Use repository/ORM abstractions only where their generated behavior is understood.
- Validate production configuration rather than relying on local defaults.
- Test database-specific behavior against the real target database when semantics matter.

