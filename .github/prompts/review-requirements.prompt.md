---
description: "Analyze requirements and repository evidence before planning. Do not implement."
argument-hint: "requirement, issue, or change request"
agent: "planner"
tools:
  - read
  - search
---
Apply the `requirements-analysis` skill. Separate explicit requirements, repository facts, material unknowns, and optional decisions. Ask only material clarification questions. Do not create implementation code.

End with a "Resolved decisions to record" list (`requirements-analysis` Recording Resolved Decisions) and tell the user to record them with `capture-requirements` before `create-plan`. Do not edit files.
