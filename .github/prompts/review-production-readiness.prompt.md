---
description: "Review evidence for safe production rollout and recovery."
argument-hint: "release, milestone, or deployment scope"
agent: "production-readiness-reviewer"
tools:
  - read
  - search
  - edit
---
Run this command in the `production-readiness-reviewer` custom agent as a subagent (`prompt-driven-development` Fresh Context). Pass it only the work item and the rest of this command's text (everything after this paragraph), and nothing from this conversation. Relay its report unchanged.

Apply `production-readiness` and relevant domain skills. Distinguish verified evidence, missing evidence, assumptions, and residual risk.

When this review is the Final Review of a work item's Plan (the user names the work item; if none is named, ask and stop), apply `prompt-driven-development` Final Review Authority: evaluate every Final Acceptance Criterion against recorded evidence, answer every Final Review obligation row in the Plan's traceability, write `docs/.ai/<work-item>/Final-Review.md` using `templates/Final-Review.md`, and add only the Final Review row to `docs/.ai/<work-item>/Plan.md` Execution Status. Change no other file. Never approve deployment or the work item; that is the user's decision.

Otherwise, do not edit files.
