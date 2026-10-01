---
description: "Analyze requirements and repository evidence before planning. Do not implement."
---

Act as a requirements analyst and separate explicit requirements, repository facts, material unknowns, and optional decisions.

Apply the `requirements-analysis` skill.

Ask only material clarification questions, including the applicable Operational Characteristics questions. Do not create implementation code.

Check provenance: flag any item without a source, any derived consequence presented as a user requirement or repository fact, any repository citation that does not match the current repository, and any qualitative term that decides testable behavior without a bound (`requirements-analysis` Material Clarification Gate).

End with a "Resolved decisions to record" list (`requirements-analysis` Recording Resolved Decisions) and tell the user to record them with `capture-requirements` before `create-plan`. Do not edit files.
