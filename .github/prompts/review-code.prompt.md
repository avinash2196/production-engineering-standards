---
description: "Review changed code for correctness, scope, production safety, and evidence."
argument-hint: "files, PR, or completed milestone"
agent: "code-reviewer"
tools:
  - read
  - search
  - edit
---
Apply `code-review` plus only relevant domain skills. Report concrete findings with evidence and smallest safe fixes.

When this review is the Final Review of a work item's Plan (the user names the work item; if none is named, ask and stop), write `docs/.ai/<work-item>/Final-Review.md` and add a Final Review row to `docs/.ai/<work-item>/Plan.md` Execution Status (`prompt-driven-development` Final Review Authority). Change no other file.
