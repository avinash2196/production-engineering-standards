---
description: "Capture or update a requirements artifact without planning or implementation."
argument-hint: "work item; requirement source, change request, or user-provided requirements"
agent: "planner"
tools:
  - read
  - search
  - edit
---
Apply `requirements-analysis` and `prompt-driven-development`.

Work item: operate only on the work-item folder the user names (`prompt-driven-development` Work-Item Folders). If no work item is named, ask and stop.

Act as a requirements analyst and capture only the requirements explicitly provided by the user or confirmed by repository evidence.

If a material unresolved decision exists, ask focused clarification questions and stop. Do not create or finalize the requirements artifact until the blocking questions are resolved.

Inspect the repository before stating any repository fact or asking any question. Apply `requirements-analysis` Requirements Capture.

Before finalizing, apply the `requirements-analysis` Operational Characteristics check: ask the user about each applicable characteristic that neither the user nor repository evidence has answered, and stop until answered. Record only answers given by the user or established by the repository, including explicit "not required" exclusions the user confirms. Never answer a characteristic yourself.

Create or update only the work item's `docs/.ai/<work-item>/requirements.md`, creating the work-item folder if it does not exist. Do not edit the product-level `docs/requirements.md`.

Do not create Plan.md, an API/external contract, an Implementation Plan, tests, or production code.
