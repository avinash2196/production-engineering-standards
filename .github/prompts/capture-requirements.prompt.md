---
description: "Capture or update a requirements artifact without planning or implementation."
argument-hint: "work item; requirement source, change request, or user-provided requirements"
agent: "planner"
tools:
  - read
  - search
  - edit
---

Plugin files: read this plugin's skills and templates only from the installed production-engineering-standards plugin running this command; never search plugin caches or read files from another installed version.

Apply `requirements-analysis` and `prompt-driven-development`.

Work item: operate only on the work-item folder the user names (`prompt-driven-development` Work-Item Folders). If no work item is named, ask and stop.

Act as a requirements analyst and capture only the requirements explicitly provided by the user or confirmed by repository evidence.

If a material unresolved decision exists, ask focused clarification questions and stop. Do not create or finalize the requirements artifact until the blocking questions are resolved.

Inspect the repository before stating any repository fact or asking any question. Apply `requirements-analysis` Requirements Capture.

Ask the `requirements-analysis` Business Intent questions first, in the same round as any other clarification: every point the brief, the repository, and the product-level requirements do not answer. Record the answers in Business Context and Scenarios.

For a fix work item (`prompt-driven-development` Fix Work Items), the requirements are the defect, the expected behavior, and how to reproduce it. The approved requirements of the work item that holds the defect answer the Business Intent points they cover; cite them as `[Artifact: …]` and ask only the rest. Apply `requirements-analysis` Diagnosis Before a Fix and say which path (quick or diagnosis) was taken and why.

Before finalizing, apply the `requirements-analysis` Operational Characteristics check: ask the user about each applicable characteristic that neither the user nor repository evidence has answered, and stop until answered. Record only answers given by the user or established by the repository, including explicit "not required" answers the user confirms. Never answer a characteristic yourself.

Apply `requirements-analysis` Real-System Verification for each external system the work item calls, in the same round, and stop until question 1 is answered for each.

Before finalizing, ask the user to confirm every derived consequence, then apply the `requirements-analysis` provenance check: every item names its source, every repository citation was verified against the current repository during this capture, no two statements contradict each other, and nothing is copied from another work item's artifacts.

Create or update only the work item's `docs/.ai/<work-item>/requirements.md`, creating the work-item folder if it does not exist, using the `prompt-driven-development` skill's `templates/requirements.md` structure — including its Relationship to Product-Level Requirements, Business Context, Scenarios, Operational Characteristics, and Provenance Check sections. Do not edit the product-level `docs/requirements.md`.

When updating an existing requirements artifact, treat it as a revision (`requirements-analysis` Revise the whole artifact): no statement the change contradicts may remain, and the Provenance Check is re-derived, not restated. Continue clarification numbering from the artifact's Clarification Log and record every new question and answer there. Remove every template comment (`<!-- … -->`) from the finished artifact.

Do not create Plan.md, an API/external contract, an Implementation Plan, tests, or production code. End the report with the `prompt-driven-development` `Next:` line: approval of `requirements.md`, then `create-plan <work-item>`. Do not continue into planning in this conversation.
