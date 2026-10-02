---
description: "Capture or update a requirements artifact without planning or implementation."
---

Apply `requirements-analysis` and `prompt-driven-development`.

Work item: operate only on the work-item folder the user names (`prompt-driven-development` Work-Item Folders). If no work item is named, ask and stop.

Act as a requirements analyst and capture only the requirements explicitly provided by the user or confirmed by repository evidence.

If a material unresolved decision exists, ask focused clarification questions and stop. Do not create or finalize the requirements artifact until the blocking questions are resolved.

Inspect the repository before stating any repository fact or asking any question. Apply `requirements-analysis` Requirements Capture.

Before finalizing, apply the `requirements-analysis` Operational Characteristics check: ask the user about each applicable characteristic that neither the user nor repository evidence has answered, and stop until answered. Record only answers given by the user or established by the repository, including explicit "not required" answers the user confirms. Never answer a characteristic yourself.

Before finalizing, ask the user to confirm every derived consequence, then apply the `requirements-analysis` provenance check: every item names its source, every repository citation was verified against the current repository during this capture, and nothing is copied from another work item's artifacts.

Create or update only the work item's `docs/.ai/<work-item>/requirements.md`, creating the work-item folder if it does not exist, using the `prompt-driven-development` skill's `templates/requirements.md` structure — including its Relationship to Product-Level Requirements, Operational Characteristics, and Provenance Check sections. Do not edit the product-level `docs/requirements.md`.

When updating an existing requirements artifact, treat it as a revision (`requirements-analysis` Revise the whole artifact): no statement the change contradicts may remain, and the Provenance Check is re-derived, not restated. Continue clarification numbering from the artifact's Clarification Log and record every new question and answer there. Remove every template comment (`<!-- … -->`) from the finished artifact.

Do not create Plan.md, an API/external contract, an Implementation Plan, tests, or production code.
