---
name: code-review
description: Use when reviewing code or a completed implementation milestone for correctness, scope, production safety, and evidence.
---

# Code Review

1. Understand the changed execution path.
2. Apply only relevant skills.
3. Prioritize correctness and production risk over style.
4. Verify plan/scope alignment when PDD artifacts exist.
5. Distinguish evidence from inference.
6. Propose the smallest safe fix as a recommendation for human decision — do not apply it directly. A finding that adds or changes behavior or validation requires a new Implementation Plan and RED before GREEN, per Final Review Authority in `prompt-driven-development`.
7. Do not manufacture findings to fill categories. Before raising a finding, check the recorded verification evidence and approved plans; drop a finding they contradict. Never recommend reverting an approved decision as a fix — raise it as a question. Give a severity only with a concrete failure scenario.
8. Check user-facing documentation (for example README files and product docs) for statements the change made false.
9. Do not infer a compliance regime from business vocabulary alone.
10. Never claim tests or validators passed without evidence.

