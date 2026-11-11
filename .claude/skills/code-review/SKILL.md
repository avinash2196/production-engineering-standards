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
11. Apply `code-quality` for size, naming, reuse, comments, severity, and the finding format.

## Review Scope

| ID | Rule | Severity |
| --- | --- | --- |
| RV1 | PR size. Above 400 changed lines (or the `docs/code-standards.md` value), excluding tests, generated files, and lock files, warn and suggest a split. Count from git's normalized diff, so line endings alone do not inflate it. In PDD, a PR is one milestone or one related set of milestones of one work item. | Medium |
| RV2 | Related changes only. In PDD, a file outside the Implementation Plan's file list is High. Outside PDD, unrelated refactors and drive-by changes are Medium. | High in PDD; else Medium |
| RV3 | Leftovers. Docs, configuration, and references made stale by the change, including statements in approved artifacts, are updated in the same PR. | Medium |
| RV4 | Business domains. When one PR touches more than one business domain (bounded context or top-level domain package), warn and ask for the reason. | Medium |
| RV5 | Check layering against LY1–LY4 and API conventions against AP1–AP5, and check implemented endpoints against the approved contract. A mismatch with the contract is High. | As listed |
| RV6 | Every finding gives the rule ID, `file:line`, severity, the failure scenario, and the recommended fix, ordered High, Medium, Low. | — |
