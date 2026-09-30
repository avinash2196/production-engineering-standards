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

Capture only the requirements explicitly provided by the user or confirmed by repository evidence.

If a material unresolved decision exists, ask focused clarification questions and stop. Do not create or finalize the requirements artifact until the blocking questions are resolved.

Before finalizing, apply the `requirements-analysis` Operational Characteristics check and record every answer, including explicit "not required" exclusions.

Create or update only the work item's `docs/.ai/<work-item>/requirements.md`, creating the work-item folder if it does not exist. Do not edit the product-level `docs/requirements.md`.

Do not create Plan.md, an API/external contract, an Implementation Plan, tests, or production code.
