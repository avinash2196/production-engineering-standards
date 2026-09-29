---
description: "Review changed code for correctness, scope, production safety, and evidence."
---

Act as a code reviewer and report concrete findings with evidence and smallest safe fixes.

Apply `code-review` plus only relevant domain skills.

When this review is the Final Review of a work item's Plan (the user names the work item; if none is named, ask and stop), write `docs/.ai/<work-item>/Final-Review.md` and add a Final Review row to `docs/.ai/<work-item>/Plan.md` Execution Status (`prompt-driven-development` Final Review Authority). Change no other file. Use the `prompt-driven-development` `templates/Final-Review.md` structure, mark each finding as pre-existing or introduced, and record corrections to earlier approved artifacts as findings instead of editing those artifacts.
