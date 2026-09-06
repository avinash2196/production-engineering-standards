---
name: prompt-driven-development
description: Use when planning or delivering behavior-changing work through explicit human-reviewed Plan, Implementation Plan, RED, GREEN, optional REFACTOR, and final-review boundaries.
---

# Prompt-Driven Development

Use this skill when the adopting repository explicitly follows the PDD/TDD lifecycle.

## Lifecycle

**Requirements → Plan → Human Review → Implementation Plan → Human Review → RED → GREEN → optional REFACTOR → Final Review**

## Controls

- Plan defines **what** is delivered and the milestone sequence.
- Each repository-changing milestone gets its own Implementation Plan defining **how that milestone only** is executed.
- RED, GREEN, and REFACTOR are separate authorization boundaries.
- RED writes tests/checks only.
- GREEN implements the smallest production change needed for approved RED evidence.
- REFACTOR is optional and behavior-preserving.
- A completed phase never implies approval of the next phase.

Use the templates in `templates/` when the adopting project does not already define compatible artifacts.

