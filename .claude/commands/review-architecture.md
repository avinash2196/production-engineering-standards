---
description: "Review architecture boundaries and distributed-system trade-offs."
context: fork
agent: production-engineering-standards:architecture-reviewer
background: false
---

Act as an architecture reviewer.

Plugin files: read this plugin's skills and templates only from `${CLAUDE_PLUGIN_ROOT}`, the installed production-engineering-standards plugin running this command (in drop-in use, where that variable appears unexpanded, this project's `.claude/` folder); never search plugin caches or read files from another installed version.

Apply `architecture-design` and `distributed-systems` where relevant. Evaluate concrete trade-offs; do not require microservices by default. Review architecture boundaries, distributed-system trade-offs, and material design decisions.

This is an intermediate design review, not the Final Review of a work item (`prompt-driven-development` Final Review Authority).
