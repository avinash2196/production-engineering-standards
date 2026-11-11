"""0.16.0 step 5: prepare-pr (brief D PR1-PR6), committed artifacts and the
repository-state check (C35), and the plan scope guard hook (P2)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TREES = [".github", ".claude"]
PAIR = [".github/prompts/prepare-pr.prompt.md", ".claude/commands/prepare-pr.md"]
GUARD = ROOT / ".claude/hooks/plan_scope_guard.py"


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class PreparePrCommandTest(unittest.TestCase):
    def test_both_modes_and_two_stops(self):
        for rel in PAIR:
            text = read(rel)
            for phrase in [
                "**Work-item mode, `prepare-pr <work-item>`.**",
                "**Branch mode, `prepare-pr` with no work item.**",
                "Never after a RED milestone alone",
                "**Stop 1 — review (`prepare-pr [<work-item>]`; writes nothing).**",
                "**Stop 2 — commit and pull request",
                "on the user's word only",
                "start a new chat for stop 2",
                "Never merge, force-push, amend, rebase, skip hooks, or commit to the default branch.",
                "as a draft",
            ]:
                self.assertIn(phrase, text, rel)

    def test_reviews_and_recommends_only(self):
        for rel in PAIR:
            text = read(rel)
            self.assertIn("It never changes source, tests, configuration, or any other executable file", text, rel)
            self.assertIn("A file or hunk not in them is High (RV2).", text, rel)
            self.assertIn("missing RED evidence is High", text, rel)
            self.assertIn("never claim a check passed that did not run", text, rel)

    def test_reviewed_state_and_commit(self):
        for rel in PAIR:
            text = read(rel)
            self.assertIn("git hash-object <files, sorted> | git hash-object --stdin", text, rel)
            self.assertIn("If either differs from the `go` digest, or no digest is given, do stop 1 again and stop.", text, rel)
            self.assertIn("never `git add -A` or `git add .`", text, rel)
            self.assertIn("plus `docs/.ai/<work-item>/` in work-item mode", text, rel)
            self.assertIn("add `Committed as <hash>`", text, rel)

    def test_rerun_only_when_not_recorded_at_this_commit(self):
        for rel in PAIR:
            text = read(rel)
            self.assertIn(
                "unless the working tree is clean apart from `docs/.ai/` and `Plan.md` records a full run at the current commit",
                text,
                rel,
            )
            self.assertIn("Branch mode has no recorded run, so it runs the full suite once.", text, rel)

    def test_code_reviewer_may_commit_for_prepare_pr(self):
        for rel in [".github/agents/code-reviewer.agent.md", ".claude/agents/code-reviewer.md"]:
            self.assertIn("`prepare-pr` stop 2 may also stage and commit the reviewed files", read(rel), rel)


class RepositoryStateTest(unittest.TestCase):
    def test_pdd_skill_checks_state_and_records_commits(self):
        for tree in TREES:
            pdd = read(f"{tree}/skills/prompt-driven-development/SKILL.md")
            self.assertIn("**Check the repository state first.** Every command, planning included", pdd, tree)
            self.assertIn("stop and report it", pdd, tree)
            self.assertIn("add `Committed as <hash>` to its row", pdd, tree)
            self.assertIn("| `prepare-pr` | The full suite once", pdd, tree)
            self.assertIn("| `prepare-pr` | Plan, contract, the Implementation Plans executed since the last commit", pdd, tree)
            self.assertIn("prepare-pr: review → Human go → commit and draft pull request", pdd, tree)

    def test_docs_name_prepare_pr(self):
        readme = read("README.md")
        self.assertIn("prepare-pr: review → Human go → commit and draft pull request", readme)
        self.assertIn("/prepare-pr order-cancellation", readme)
        self.assertIn("run `/prepare-pr <work-item>`", read("docs/getting-started.md"))


PLAN = """# Implementation Plan

## Files in Scope

### Files to Create

- `src/new_module.py`

### Files to Modify

- `src/app.py`
- `.github/workflows/ci.yml`

### Files to Delete

None.

## Human Review

{status}
"""


class PlanScopeGuardTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name).resolve()
        (self.repo / ".git").mkdir()
        self.plans = self.repo / "docs/.ai/order-cancellation"
        self.plans.mkdir(parents=True)

    def tearDown(self):
        self._tmp.cleanup()

    def write_plan(self, name: str, status: str) -> None:
        (self.plans / name).write_text(PLAN.format(status=status), encoding="utf-8")

    def run_guard(self, target: Path, tool: str = "Edit") -> subprocess.CompletedProcess:
        key = "notebook_path" if tool == "NotebookEdit" else "file_path"
        payload = {"tool_name": tool, "cwd": str(self.repo), "tool_input": {key: str(target)}}
        return subprocess.run(
            [sys.executable, str(GUARD)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_blocks_file_outside_the_active_plan(self):
        self.write_plan("002_Implementation_Plan_GREEN.md", "Approved by Avi on 2026-11-10.")
        result = self.run_guard(self.repo / "src/other.py", "Write")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("src/other.py is not in the Files in Scope", result.stderr)

    def test_allows_files_in_scope_and_work_item_artifacts(self):
        self.write_plan("002_Implementation_Plan_GREEN.md", "Approved by Avi on 2026-11-10.")
        for rel in ["src/app.py", "src/new_module.py", ".github/workflows/ci.yml", "docs/.ai/order-cancellation/Plan.md"]:
            self.assertEqual(self.run_guard(self.repo / rel).returncode, 0, rel)

    def test_paired_plan_after_red_is_still_active(self):
        self.write_plan(
            "002_Implementation_Plan_RED_GREEN.md",
            "RED executed — see Plan.md; GREEN approved, not yet executed",
        )
        self.assertEqual(self.run_guard(self.repo / "src/other.py").returncode, 2)

    def test_allows_when_no_plan_is_active(self):
        self.write_plan("001_Implementation_Plan_RED.md", "Approved by Avi on 2026-11-09. Executed — see Plan.md.")
        self.write_plan("002_Implementation_Plan_GREEN.md", "Awaiting human review.")
        self.assertEqual(self.run_guard(self.repo / "src/other.py").returncode, 0)

    def test_allows_when_several_plans_are_active(self):
        self.write_plan("002_Implementation_Plan_GREEN.md", "Approved by Avi on 2026-11-10.")
        self.write_plan("003_Implementation_Plan_OTHER.md", "Approved by Avi on 2026-11-10.")
        self.assertEqual(self.run_guard(self.repo / "src/other.py").returncode, 0)

    def test_allows_files_outside_the_repository(self):
        self.write_plan("002_Implementation_Plan_GREEN.md", "Approved by Avi on 2026-11-10.")
        with tempfile.TemporaryDirectory() as outside:
            self.assertEqual(self.run_guard(Path(outside) / "notes.md", "Write").returncode, 0)

    def test_notebook_edit_is_checked(self):
        self.write_plan("002_Implementation_Plan_GREEN.md", "Approved by Avi on 2026-11-10.")
        self.assertEqual(self.run_guard(self.repo / "analysis.ipynb", "NotebookEdit").returncode, 2)

    def test_hooks_json_runs_the_guard_on_every_edit_tool(self):
        group = json.loads(read(".claude/hooks/hooks.json"))["hooks"]["PreToolUse"][0]
        self.assertEqual(set(group["matcher"].split("|")), {"Edit", "Write", "MultiEdit", "NotebookEdit"})
        command = group["hooks"][0]["command"]
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/hooks/plan_scope_guard.py", command)
        self.assertIn("Python not found", command)


if __name__ == "__main__":
    unittest.main()
