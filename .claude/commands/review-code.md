---
description: "Review changed code for correctness, scope, production safety, and evidence."
context: fork
agent: production-engineering-standards:code-reviewer
background: false
---

Act as a code reviewer.

Plugin files: read this plugin's skills and templates only from `${CLAUDE_PLUGIN_ROOT}`, the installed production-engineering-standards plugin running this command (in drop-in use, where that variable appears unexpanded, this project's `.claude/` folder); never search plugin caches or read files from another installed version.

Apply `code-review` plus only relevant domain skills; for a Final Review, also `prompt-driven-development` with its `milestone-types.md`, `plan-rules.md`, `execution.md`, and `final-review.md`. Report concrete findings with evidence and smallest safe fixes.

When this review is the Final Review of a work item's Plan (the user names the work item; if none is named, ask and stop), write `docs/.ai/<work-item>/Final-Review.md` and add a Final Review row to `docs/.ai/<work-item>/Plan.md` Execution Status (`prompt-driven-development` Final Review Authority). Change no other file. Answer every Final Review obligation row in the Plan's traceability. Use the `prompt-driven-development` `templates/Final-Review.md` structure, mark each finding as pre-existing or introduced, and record corrections to earlier approved artifacts as findings instead of editing those artifacts. Before raising a finding, read `Plan.md` Execution Status evidence and the approved Implementation Plans, and drop any finding they contradict; never recommend reverting an approved decision as a fix. List product-level and user-facing documentation the change made false. Rerun the full verification only when no full run is recorded for the current repository state (`prompt-driven-development` Test Scope and Output). The Plan.md row reads "Written — awaiting user decision". Remove every template comment (`<!-- … -->`) from the finished artifact.
