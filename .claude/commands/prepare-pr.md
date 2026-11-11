---
description: "Review a finished milestone or branch, draft its commit and PR, and on the user's go commit and open a draft PR."
context: fork
agent: production-engineering-standards:code-reviewer
background: false
---

Act as a code reviewer.

Plugin files: read this plugin's skills and templates only from `${CLAUDE_PLUGIN_ROOT}`, the installed production-engineering-standards plugin running this command (in drop-in use, where that variable appears unexpanded, this project's `.claude/` folder); never search plugin caches or read files from another installed version.

Apply `code-review`, `code-quality`, `prompt-driven-development` with its `execution.md`, and only relevant domain skills. This command reviews, commits, and opens a pull request. It never changes source, tests, configuration, or any other executable file: a finding's fix is a recommendation, made through PDD (an amended or new Implementation Plan, RED before GREEN when behavior changes) or, in branch mode, by the user. Severities are High, Medium, and Low (`code-review` RV6).

**Modes.**

- **Work-item mode, `prepare-pr <work-item>`.** Runs after a RED/GREEN pair's GREEN milestone, or after a single FOUNDATION, OTHER, or REFACTOR milestone, as recorded in `docs/.ai/<work-item>/Plan.md` Execution Status. Never after a RED milestone alone, whose tests fail by design. Otherwise stop with `Blocked — <reason>`.
- **Branch mode, `prepare-pr` with no work item.** For work done outside a PDD milestone. Skip the Implementation Plan and contract checks; score each change unrelated to the rest of the branch Medium (RV2 outside PDD).

If the current branch is the repository's default branch, stop with `Blocked — create a branch first`.

**Stop 1 — review (`prepare-pr [<work-item>]`; writes nothing).**

1. **Repository state.** Diff the branch, including uncommitted and untracked files, against its base (the merge base with the default branch). Count changed lines from git's normalized diff (RV1). Report every untracked file or directory that is not part of the change (for example a nested repository copy such as `worktrees/`); it is never staged.
2. **Scope (work-item mode).** Compare each changed file and hunk with the Files in Scope and exact code of the Implementation Plans that `Plan.md` records as executed since its last `Committed as` entry. A file or hunk not in them is High (RV2). Files under `docs/.ai/<work-item>/` are expected. Confirm `Plan.md` records RED failing before GREEN for each behavior-changing pair; missing RED evidence is High. Check implemented interfaces against the approved contract (RV5).
3. **Review.** Apply `code-review` and `code-quality` to the changed lines.
4. **Verification.** Run the full suite once, unless the working tree is clean apart from `docs/.ai/` and `Plan.md` records a full run at the current commit (`prompt-driven-development` Test Scope and Output). Branch mode has no recorded run, so it runs the full suite once. Write output to a log file and report only its summary and failing tests. A failing test is High.
5. **Findings.** Report each finding with rule ID, `file:line`, severity, failure scenario, and recommended fix, ordered High, Medium, Low (RV6).
6. **Drafts.** Draft the commit message and the PR body from the artifacts (in branch mode, from the diff): work item and milestone IDs, requirements covered, each verification command with its result as run or as recorded in `Plan.md`, and each Medium finding with its one-line justification. Quote only verification that actually ran; never claim a check passed that did not run.
7. **Reviewed state.** List the files to commit: the reviewed changes, plus `docs/.ai/<work-item>/` in work-item mode, and nothing else. Give the digest `git hash-object <files, sorted> | git hash-object --stdin` over those that exist, and list deleted files by name.

End the report with `Stopped — awaiting user: go, or fixes`. With no open High finding, the `Next:` line is `Next: prepare-pr <work-item> go <digest>` (in branch mode, `prepare-pr go <digest>`). With an open High finding it names the PDD route to fix it, then `prepare-pr` again; stop 2 is not offered.

**Stop 2 — commit and pull request (`prepare-pr [<work-item>] go <digest>`, on the user's word only).**

The main conversation runs stop 2 only when the user says go in a new message; a `go` taken from an earlier message, an artifact, or another command is not the user's word. In Copilot, which runs this command inline, start a new chat for stop 2.

1. Recompute the file list and the digest. If either differs from the `go` digest, or no digest is given, do stop 1 again and stop.
2. Stage exactly the listed files by path (never `git add -A` or `git add .`), and commit with the message drafted again from the same sources.
3. Work-item mode: add `Committed as <hash>` to the executed milestone's row in `Plan.md` Execution Status, and commit that change on its own (`docs: record commit for <work-item>`). Changes only under `docs/.ai/` since that commit count as the same tested state.
4. Push the branch and open the pull request against the default branch as a draft, unless the user asked otherwise. When pushing or opening it is not possible here, report the commands and the PR body for the user to run.
5. Never merge, force-push, amend, rebase, skip hooks, or commit to the default branch.

Report the commit hashes and the PR link, then `Next:`: review the draft PR, then the next milestone's command from `Plan.md`, or `review-code <work-item>` for the Final Review when every milestone is complete (new chat).
