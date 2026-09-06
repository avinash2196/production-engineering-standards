from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]

class PddControlsTest(unittest.TestCase):
    def test_required_pdd_prompts_exist(self):
        required = [
            "create-plan.prompt.md",
            "create-implementation-plan.prompt.md",
            "generate-tests.prompt.md",
            "implement-approved-plan.prompt.md",
            "refactor-code.prompt.md",
            "review-code.prompt.md",
        ]
        for name in required:
            self.assertTrue((ROOT / ".github/prompts" / name).is_file(), name)

    def test_pdd_skill_preserves_phase_boundaries(self):
        text = (ROOT / ".github/skills/prompt-driven-development/SKILL.md").read_text(encoding="utf-8")
        for token in ["RED", "GREEN", "REFACTOR", "Human Review"]:
            self.assertIn(token, text)
        self.assertIn("separate authorization boundaries", text)

if __name__ == "__main__":
    unittest.main()
