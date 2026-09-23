"""Mutation-style tests for the repository validator.

Unlike test_pdd_controls.py (which asserts properties of the real repo
directly), these tests prove the *validator itself* detects a broken
repository: each test copies the real repo into a temporary directory,
deliberately breaks one thing, and asserts that
`validate_repository(mutated_root)` reports it. A test that only checked
"does the real repo have property X" would pass even if the validator
function that's supposed to check X had a bug, or wasn't wired into
`validate_repository` at all — these tests call the actual top-level API
that CI and the CLI both use, so they can't pass for that reason.
"""

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "tooling" / "scripts" / "validate_repository.py"

_spec = importlib.util.spec_from_file_location("validate_repository", SCRIPT_PATH)
validate_repository_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_repository_module)
validate_repository = validate_repository_module.validate_repository


def _ignore_git(_dir: str, names: list[str]) -> set[str]:
    return {".git"} & set(names)


class ValidatorMutationTestCase(unittest.TestCase):
    """Base class: gives each test its own throwaway copy of the real repo."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name) / "repo"
        shutil.copytree(ROOT, self.repo, ignore=_ignore_git)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def errors(self) -> list[str]:
        return validate_repository(self.repo)

    def assert_error_containing(self, substring: str) -> None:
        errors = self.errors()
        self.assertTrue(
            any(substring in e for e in errors),
            f"expected an error containing {substring!r}, got: {errors}",
        )


class HappyPathTest(ValidatorMutationTestCase):
    def test_unmodified_repository_has_zero_errors(self):
        self.assertEqual(self.errors(), [])


class MissingEnvironmentStructureTest(ValidatorMutationTestCase):
    def test_deleting_claude_skills_tree_fails(self):
        shutil.rmtree(self.repo / ".claude/skills")
        self.assert_error_containing("missing required skill mirror tree: .claude/skills")

    def test_deleting_plugin_skills_tree_fails(self):
        shutil.rmtree(self.repo / "plugin/skills")
        self.assert_error_containing("missing required skill mirror tree: plugin/skills")

    def test_missing_mirror_tree_does_not_silently_skip_validation(self):
        # The old implementation returned early (zero errors) if any mirror
        # tree was absent, instead of failing — deleting a whole environment
        # must be at least as loud as deleting one file inside it.
        shutil.rmtree(self.repo / ".claude/skills")
        self.assertGreater(len(self.errors()), 0)


class SkillSynchronizationTest(ValidatorMutationTestCase):
    def test_deleting_a_mirrored_skill_fails(self):
        shutil.rmtree(self.repo / ".claude/skills/code-review")
        self.assert_error_containing(
            "missing file present in .github/skills/code-review/SKILL.md"
        )

    def test_extra_obsolete_claude_only_skill_fails(self):
        extra = self.repo / ".claude/skills/obsolete-skill"
        extra.mkdir()
        (extra / "SKILL.md").write_text(
            "---\nname: obsolete-skill\ndescription: stale\n---\n", encoding="utf-8"
        )
        self.assert_error_containing("unexpected extra file")

    def test_extra_obsolete_plugin_only_skill_fails(self):
        extra = self.repo / "plugin/skills/obsolete-skill"
        extra.mkdir()
        (extra / "SKILL.md").write_text(
            "---\nname: obsolete-skill\ndescription: stale\n---\n", encoding="utf-8"
        )
        self.assert_error_containing("unexpected extra file")

    def test_altered_mirrored_skill_content_fails(self):
        path = self.repo / ".claude/skills/code-review/SKILL.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nmutated\n", encoding="utf-8")
        self.assert_error_containing("has diverged from")

    def test_happy_path_has_no_sync_errors_as_control(self):
        # Sanity control for the three tests above: confirm the unmutated
        # skill tree really does start with zero sync errors, so those
        # failures are caused by the mutation and not pre-existing drift.
        errors = self.errors()
        sync_errors = [e for e in errors if "code-review" in e]
        self.assertEqual(sync_errors, [])


class CommandCoverageTest(ValidatorMutationTestCase):
    def test_deleting_claude_implement_approved_plan_command_fails(self):
        (self.repo / ".claude/commands/implement-approved-plan.md").unlink()
        self.assert_error_containing(
            "missing required PDD command 'implement-approved-plan'"
        )

    def test_deleting_plugin_implement_approved_plan_command_fails(self):
        (self.repo / "plugin/commands/implement-approved-plan.md").unlink()
        self.assert_error_containing(
            "missing required PDD command 'implement-approved-plan'"
        )

    def test_deleting_claude_create_plan_command_fails(self):
        # A second, different command than implement-approved-plan, to prove
        # command coverage is generic per-operation rather than hard-coded
        # to one filename.
        (self.repo / ".claude/commands/create-plan.md").unlink()
        self.assert_error_containing("missing required PDD command 'create-plan'")

    def test_deleting_github_generate_tests_prompt_fails(self):
        (self.repo / ".github/prompts/generate-tests.prompt.md").unlink()
        self.assert_error_containing("missing required PDD command 'generate-tests'")


class NoBypassControlBlockTest(ValidatorMutationTestCase):
    @staticmethod
    def _strip_block(text: str) -> str:
        return re.sub(
            r"<!-- PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL:START -->"
            r".*?"
            r"<!-- PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL:END -->\n?",
            "",
            text,
            flags=re.DOTALL,
        )

    def test_removing_block_from_copilot_instructions_fails(self):
        path = self.repo / ".github/copilot-instructions.md"
        path.write_text(self._strip_block(path.read_text(encoding="utf-8")), encoding="utf-8")
        self.assert_error_containing(
            "missing or malformed PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL block"
        )

    def test_removing_block_from_claude_md_fails(self):
        path = self.repo / "CLAUDE.md"
        path.write_text(self._strip_block(path.read_text(encoding="utf-8")), encoding="utf-8")
        self.assert_error_containing(
            "missing or malformed PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL block"
        )

    def test_altering_block_content_fails(self):
        # The mutated wording still contains every old loose keyword
        # ("code change", "Implementation Plan", "free-form") but reverses
        # the actual rule — proving canonical-block comparison catches what
        # keyword matching would have missed.
        path = self.repo / ".github/copilot-instructions.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "Every code change must be traceable to a human-approved, "
            "milestone-specific Implementation Plan",
            "Most code changes should ideally reference an Implementation "
            "Plan where a free-form request makes that convenient",
        )
        path.write_text(text, encoding="utf-8")
        self.assert_error_containing(
            "PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL block content diverges"
        )

    def test_malformed_marker_fails(self):
        path = self.repo / "CLAUDE.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "<!-- PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL:END -->", ""
        )
        path.write_text(text, encoding="utf-8")
        self.assert_error_containing(
            "missing or malformed PDD-CONTROL:NO-CODE-CHANGE-WITHOUT-APPROVAL block"
        )


class ValidatorWiringRegressionTest(ValidatorMutationTestCase):
    def test_top_level_validator_catches_oracle_skill_breakage(self):
        # Regression guard for wiring, not logic: if validate_oracle_skill
        # were ever removed from the VALIDATORS list in validate_repository,
        # this is the only test that would notice, because it goes through
        # validate_repository() — the same top-level function CI calls —
        # rather than calling validate_oracle_skill directly.
        (
            self.repo
            / ".github/skills/oracle-to-postgres-modernization/references/assessment.md"
        ).unlink()
        self.assert_error_containing(
            "oracle-to-postgres skill missing: references/assessment.md"
        )


class CliEntryPointTest(ValidatorMutationTestCase):
    # These run the actual script file inside the mutated copy as a
    # subprocess, proving the CLI path (main() -> REPO_ROOT from __file__)
    # is the same code, not a parallel implementation, as what
    # validate_repository() above is tested through.

    def _run_cli(self) -> subprocess.CompletedProcess:
        script = self.repo / "tooling" / "scripts" / "validate_repository.py"
        return subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
        )

    def test_cli_passes_on_unmodified_repository(self):
        result = self._run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Repository validation PASSED", result.stdout)

    def test_cli_fails_and_exits_nonzero_on_broken_repository(self):
        shutil.rmtree(self.repo / "plugin/skills")
        result = self._run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Repository validation FAILED", result.stdout)
        self.assertIn("missing required skill mirror tree: plugin/skills", result.stdout)


if __name__ == "__main__":
    unittest.main()
