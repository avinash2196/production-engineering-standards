import importlib.util
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]

_SCRIPT_PATH = ROOT / "tooling" / "scripts" / "validate_repository.py"
_spec = importlib.util.spec_from_file_location("validate_repository", _SCRIPT_PATH)
validate_repository_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_repository_module)


class PddControlsTest(unittest.TestCase):
    def test_required_pdd_prompts_exist(self):
        required = [
            "capture-requirements.prompt.md",
            "create-plan.prompt.md",
            "create-api-contract.prompt.md",
            "create-implementation-plan.prompt.md",
            "generate-tests.prompt.md",
            "implement-approved-plan.prompt.md",
            "refactor-code.prompt.md",
            "review-code.prompt.md",
        ]
        for name in required:
            self.assertTrue((ROOT / ".github/prompts" / name).is_file(), name)

    def test_pdd_skill_preserves_authorization_boundaries(self):
        raw = (
            ROOT / ".github/skills/prompt-driven-development/SKILL.md"
        ).read_text(encoding="utf-8")
        # Normalize spacing around "/" so "API / External Contract" and
        # "API/External Contract" both satisfy the same token check.
        text = re.sub(r"\s*/\s*", "/", raw)

        for token in [
            "Requirements",
            "Plan",
            "API/External Contract",
            "RED",
            "GREEN",
            "REFACTOR",
            "Human Review",
            "Artifact Authority",
        ]:
            self.assertIn(token, text)

        self.assertIn("separate authorization boundaries", text)

    def test_pdd_skill_has_adaptive_milestone_decomposition(self):
        text = (
            ROOT / ".github/skills/prompt-driven-development/SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Adaptive Milestone Decomposition", text)
        self.assertIn("one pair per class/layer", text)

    def test_adaptive_decomposition_not_duplicated_as_exhaustive_list(self):
        # The full boundary catalog (persistence/domain/service/controller/
        # validation/concurrency/...) belongs only in getting-started.md as
        # illustrative documentation — runtime prompts should reference the
        # skill's rule, not redefine an exhaustive list of their own.
        exhaustive_markers = ["concurrency,", "migration,", "infrastructure/configuration"]
        runtime_files = [
            ".github/prompts/create-plan.prompt.md",
            ".claude/commands/create-plan.md",
            "plugin/commands/create-plan.md",
            ".github/agents/planner.agent.md",
            ".claude/agents/planner.md",
            "plugin/agents/planner.md",
            ".github/skills/prompt-driven-development/templates/Plan.md",
        ]
        for rel in runtime_files:
            text = (ROOT / rel).read_text(encoding="utf-8")
            found = [m for m in exhaustive_markers if m in text]
            self.assertEqual(
                found,
                [],
                f"{rel} still duplicates the exhaustive boundary list: {found}",
            )

    def test_pdd_skill_forbids_red_production_scaffolding(self):
        skill_texts = "\n".join(
            (ROOT / rel).read_text(encoding="utf-8")
            for rel in [
                ".github/skills/prompt-driven-development/SKILL.md",
                ".github/skills/implementation-planning/SKILL.md",
                ".github/agents/test-engineer.agent.md",
                ".github/prompts/generate-tests.prompt.md",
            ]
        )

        self.assertIn("do not propose production implementation", skill_texts.lower())
        self.assertIn("scaffolding", skill_texts.lower())
        self.assertNotIn("Skeleton Implementation Plan", skill_texts)

    def test_pdd_skill_copies_are_synchronized(self):
        canonical_root = ROOT / ".github/skills"
        mirror_roots = [ROOT / ".claude/skills", ROOT / "plugin/skills"]

        for canonical_file in canonical_root.rglob("*"):
            if not canonical_file.is_file():
                continue
            rel = canonical_file.relative_to(canonical_root)
            canonical_text = canonical_file.read_text(encoding="utf-8")

            for mirror_root in mirror_roots:
                mirror_file = mirror_root / rel
                self.assertTrue(mirror_file.is_file(), f"missing {mirror_file}")
                self.assertEqual(
                    canonical_text,
                    mirror_file.read_text(encoding="utf-8"),
                    f"{mirror_file} has diverged from {canonical_file}",
                )

    def test_no_code_change_bypass_control_blocks_match_canonical(self):
        # This is the global control that closes the free-form-prompt
        # bypass: a real incident applied unreviewed code changes via a
        # prompt that never invoked any named PDD command, so this must
        # live in the always-loaded instruction files, not only inside
        # command prompts. Compared as a canonical block (single source of
        # truth in the validator module), not loose keywords — keyword
        # presence can pass even if a file asserts the opposite of the rule.
        m = validate_repository_module
        canonical = m._normalize_control_block(m.CANONICAL_NO_CODE_CHANGE_BLOCK)

        for rel in m.NO_CODE_CHANGE_REQUIRED_FILES:
            text = (ROOT / rel).read_text(encoding="utf-8")
            block = m._extract_control_block(text, m.NO_CODE_CHANGE_CONTROL_ID)
            self.assertIsNotNone(block, f"{rel}: missing PDD-CONTROL block")
            self.assertEqual(
                m._normalize_control_block(block),
                canonical,
                f"{rel}: PDD-CONTROL block diverges from the canonical rule",
            )

    def test_requirements_skill_has_blocking_clarification_gate(self):
        text = (
            ROOT / ".github/skills/requirements-analysis/SKILL.md"
        ).read_text(encoding="utf-8").lower()

        for token in [
            "material unresolved",
            "clarification",
            "stop",
            "wait",
        ]:
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
