---
name: architecture-design
description: Use when designing or reviewing module/service boundaries, dependency direction, capability abstractions, data ownership, or material architecture trade-offs.
---

# Architecture Design

Prefer boundaries based on business capability, ownership, change rate, scaling need, reliability isolation, and data responsibility—not fashionable topology.

Evaluate:
- modular monolith vs service split
- synchronous vs asynchronous interaction
- transaction boundaries
- dependency direction
- data ownership
- extensibility vs accidental abstraction
- operational cost

Read `references/capability-boundaries.md` when abstracting external infrastructure capabilities.

