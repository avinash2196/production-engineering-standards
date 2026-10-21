---
description: "Review architecture boundaries and distributed-system trade-offs."
argument-hint: "design, Plan, ADR, or changed architecture"
agent: "architecture-reviewer"
tools:
  - read
  - search
---
Run this command in the `architecture-reviewer` custom agent as a subagent (`prompt-driven-development` Fresh Context). Pass it only the work item and the rest of this command's text (everything after this paragraph), and nothing from this conversation. Relay its report unchanged.

Apply `architecture-design` and `distributed-systems` where relevant. Evaluate concrete trade-offs; do not require microservices by default. Review architecture boundaries, distributed-system trade-offs, and material design decisions.

This is an intermediate design review, not the Final Review of a work item (`prompt-driven-development` Final Review Authority).
