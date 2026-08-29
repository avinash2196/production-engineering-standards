---
name: code-review
description: Use when reviewing pull requests, code changes, or completed implementation milestones for correctness and production safety; apply only engineering standards relevant to the changed execution path, stack, scope, and risk.
---

# Code Review

Use this skill for repository code review, including Copilot pull-request review.

## Governing Behavior

When available, read and follow:

- [review-code prompt](../../prompts/review-code.prompt.md) for the canonical review structure when that prompt is available;
- the approved Plan and milestone Implementation Plan when the adopting project uses PDD;
- only standards relevant to the changed execution path.

## Review Rules

1. Prioritize correctness and production safety over style.
2. Understand enough surrounding source, tests, contracts, configuration, migrations, and planning context to validate the changed behavior.
3. Do not manufacture findings to satisfy a checklist or apply unrelated standards merely to increase coverage.
4. A concrete correctness defect may be reported even when no written standard explicitly names it. Explain the exact scenario and risk.
5. Reference the applicable requirement, contract, Plan, Implementation Plan, or standard when one exists.
6. Distinguish `AUTOMATED`, `REVIEWED`, and `ADVISORY` findings.
7. Use severity based on concrete impact and likelihood, not the number of standards involved.
8. Propose the smallest safe fix rather than an unrelated redesign.
9. Use `NEEDS VERIFICATION` when evidence is insufficient. State exactly what evidence is missing instead of guessing.
10. Do not infer HIPAA or another compliance regime from industry vocabulary alone; apply compliance-specific checks only when explicitly adopted or confirmed by project evidence.
11. Do not claim tests, validators, static checks, or commands passed unless they were actually run or their results were supplied.

## PDD/TDD Integrity

When the project has adopted this workflow, verify the high-level lifecycle:

**Requirements → Plan → Human Review → Implementation Plan → Human Review → RED Tests → GREEN Code → Refactor → Final Review**

For behavior-changing work, also verify the repository's phase-specific control model:

- RED and GREEN are separate Plan milestones.
- The RED milestone has its own approved Implementation Plan and valid RED evidence.
- The GREEN milestone has its own separately approved Implementation Plan and references the predecessor RED evidence.
- Refactoring, when present, is a separate justified REFACTOR milestone with its own approved Implementation Plan and a verified GREEN baseline.
- Completion of one phase did not automatically authorize the next phase.

A missing artifact is a finding only when the project has adopted the workflow for the reviewed change.

## Review Checklist

- [ ] Changed execution path and relevant context were understood.
- [ ] Only applicable standards were used.
- [ ] Findings have concrete evidence and risk.
- [ ] Governing evidence is cited when it exists.
- [ ] Uncertainty is labeled rather than guessed through.
- [ ] No finding exists only to fill a review category.
- [ ] CRITICAL/HIGH findings are not silently approved.
